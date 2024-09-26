import cv2
import tobii_research as tr
import threading
import math
import time
from collections import deque

# 使うやつ
SPEED_THRESHOLD = 1000  # 視線の変化量に基づく残像の調整に使用するスレッショルド（ピクセル単位）1000:残像ほぼなし，100:残像あり
LOW_PASS_FILTER_ALPHA = 0.6  # ローパスフィルターのαパラメータ（0 < α < 1）0:おっそい，1:生データ
CIRCLE_COLOR = (0, 0, 255)  # 赤色 (BGR)
CIRCLE_RADIUS = 15  # 円の半径
CIRCLE_THICKNESS = 3  # 円の線の太さ

# パラメータ設定
FADE_FACTOR = 0.5  # 残像のフェードファクター
MAX_HISTORY_SIZE = 30  # 視線データの保持フレーム数
TARGET_FPS = 60  # 目標とするFPS
ENABLE_TRAILS = True  # 残像機能を有効にするかどうか

# MacBookの画面解像度
MACBOOK_SCREEN_WIDTH = 2560  # MacBook Pro 14インチの解像度（例）
MACBOOK_SCREEN_HEIGHT = 1600  # MacBook Pro 14インチの解像度（例）

global_gaze_data = None
gaze_data_lock = threading.Lock()

# 過去の視線データを保持するためのdeque
gaze_history = deque(maxlen=MAX_HISTORY_SIZE)
last_gaze_point = None
filtered_gaze_point = None

def gaze_data_callback(gaze_data):
    global global_gaze_data
    with gaze_data_lock:
        global_gaze_data = gaze_data

def subscribe_to_gaze_data(eyetracker):
    eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

def gaze_data_thread(eyetracker):
    subscribe_to_gaze_data(eyetracker)

def capture_camera_feed(camera_index=0):
    cap = cv2.VideoCapture(camera_index)
    return cap

def resize_frame(frame, width, height):
    return cv2.resize(frame, (width, height))

def compute_gaze_change(current_gaze, previous_gaze):
    if previous_gaze is None:
        return 0
    dx = current_gaze[0] - previous_gaze[0]
    dy = current_gaze[1] - previous_gaze[1]
    return math.sqrt(dx ** 2 + dy ** 2)

def apply_low_pass_filter(current_gaze, previous_filtered_gaze, alpha):
    if previous_filtered_gaze is None:
        return current_gaze
    # 各成分を個別に処理
    x_filtered = (1 - alpha) * previous_filtered_gaze[0] + alpha * current_gaze[0]
    y_filtered = (1 - alpha) * previous_filtered_gaze[1] + alpha * current_gaze[1]
    return (x_filtered, y_filtered)

def overlay_gaze_on_frame(frame, gaze_data):
    global gaze_history, last_gaze_point, filtered_gaze_point

    if gaze_data:
        gaze_point = gaze_data['left_gaze_point_on_display_area']
        x, y = gaze_point[0], gaze_point[1]
        if not (math.isnan(x) or math.isnan(y)):
            x = int(x * frame.shape[1])
            y = int(y * frame.shape[0])
            current_gaze_point = (x, y)
            
            # ローパスフィルターを適用
            filtered_gaze_point = apply_low_pass_filter(current_gaze_point, filtered_gaze_point, LOW_PASS_FILTER_ALPHA)
            if filtered_gaze_point is None:
                filtered_gaze_point = current_gaze_point

            # 視線が画面内にある場合のみ処理を続ける
            if 0 <= filtered_gaze_point[0] < frame.shape[1] and 0 <= filtered_gaze_point[1] < frame.shape[0]:
                if ENABLE_TRAILS:
                    if last_gaze_point:
                        gaze_change = compute_gaze_change(filtered_gaze_point, last_gaze_point)
                        # 視線の変化量に基づいて残像の数を線形に変化させる
                        num_trails = max(1, min(10, int((gaze_change / SPEED_THRESHOLD) * 10)))
                        gaze_history = deque(gaze_history, maxlen=num_trails)
                    gaze_history.append(filtered_gaze_point)
                    last_gaze_point = filtered_gaze_point

                x, y = filtered_gaze_point
                # 座標が整数であることを確認
                x, y = int(x), int(y)
                # デバッグ用出力
                cv2.circle(frame, (x, y), CIRCLE_RADIUS, CIRCLE_COLOR, CIRCLE_THICKNESS)

                # 残像が有効な場合のみ過去の視線データを描画
                if ENABLE_TRAILS:
                    for i, (x, y) in enumerate(gaze_history):
                        alpha = (i + 1) / len(gaze_history)  # 古いデータほど薄くする
                        # 座標が整数であることを確認
                        if 0 <= x < frame.shape[1] and 0 <= y < frame.shape[0]:
                            x, y = int(x), int(y)
                            # デバッグ用出力
                            cv2.circle(frame, (x, y), CIRCLE_RADIUS, CIRCLE_COLOR, CIRCLE_THICKNESS)
            else:
                # 画面外に出たら視線データをリセット
                filtered_gaze_point = None
                gaze_history.clear()
                last_gaze_point = None
        else:
            # 無効なデータの場合もリセット
            filtered_gaze_point = None
            gaze_history.clear()
            last_gaze_point = None
    else:
        # データがない場合もリセット
        filtered_gaze_point = None
        gaze_history.clear()
        last_gaze_point = None
    
    return frame

def main():
    frame_time = 1.0 / TARGET_FPS  # 各フレームにかかる時間

    camera_feed = capture_camera_feed()
    
    # 接続されているアイトラッカーを表示
    found_eyetrackers = tr.find_all_eyetrackers()
    if not found_eyetrackers:
        print("アイトラッカーが見つかりませんでした。接続を確認してください。")
        return
    
    for idx, tracker in enumerate(found_eyetrackers):
        print('------------------------------------------')
        print(f"Connected eye tracker: {idx}, {tracker.address}, {tracker.model}")

    # 最初のアイトラッカーを使用
    eye_tracker = found_eyetrackers[0]
    print(f"Eye tracker to be used: {eye_tracker.address}")
    print('------------------------------------------')

    # 別スレッドで視線データのサブスクライブを開始
    gaze_thread = threading.Thread(target=gaze_data_thread, args=(eye_tracker,))
    gaze_thread.daemon = True
    gaze_thread.start()

    frame_count = 0
    start_time = time.time()

    global last_gaze_point, filtered_gaze_point
    last_gaze_point = None
    filtered_gaze_point = None

    try:
        while True:
            frame_start_time = time.time()

            ret, frame = camera_feed.read()
            if not ret:
                break

            # カメラ映像をMacBookの画面サイズに合わせてリサイズ
            frame_resized = resize_frame(frame, MACBOOK_SCREEN_WIDTH, MACBOOK_SCREEN_HEIGHT)

            # グローバル変数の視線データを取得
            with gaze_data_lock:
                gaze_data = global_gaze_data
            
            # A側のディスプレイに元の映像を表示
            cv2.imshow("expert", frame_resized)
            
            # B側のディスプレイに視線情報を重畳した映像を表示
            frame_with_gaze = overlay_gaze_on_frame(frame_resized.copy(), gaze_data)
            cv2.imshow("beginner", frame_with_gaze)

            # FPSをコントロールするために、次のフレームまでの待機時間を計算
            elapsed_time = time.time() - frame_start_time
            wait_time = frame_time - elapsed_time
            if wait_time > 0:
                time.sleep(wait_time)

            frame_count += 1

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except KeyboardInterrupt:
        # プログラムの停止時にFPSを表示
        end_time = time.time()
        total_time = end_time - start_time
        actual_fps = frame_count / total_time
        print(f"\nKeyboardInterrupt >> stop mainloop, FPS: {actual_fps:.2f}")

    finally:
        camera_feed.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()