from ctypes.wintypes import tagRECT
import cv2
import tobii_research as tr
import threading
import math
import time
from collections import deque
import csv
import datetime
import os

# パス名を確認してプログラムを実行する
dirPath = "/Users/sanolab/this mac/大学/研究室/M2/SI2024/pre/tobiitest/4"

# 設定パラメータ
SPEED_THRESHOLD = 1000
LOW_PASS_FILTER_ALPHA = 0.6
CIRCLE_COLOR = (0, 0, 255)
CIRCLE_RADIUS = 15
CIRCLE_THICKNESS = 3
FADE_FACTOR = 0.5
MAX_HISTORY_SIZE = 30
TARGET_FPS = 20
ENABLE_TRAILS = False

# MacBookの画面解像度
MACBOOK_SCREEN_WIDTH = 1280
MACBOOK_SCREEN_HEIGHT = 800

os.makedirs(dirPath, exist_ok=True)

global_gaze_data = None
gaze_data_lock = threading.Lock()

# 過去の視線データを保持するためのdeque
gaze_history = deque(maxlen=MAX_HISTORY_SIZE)
last_gaze_point = None
filtered_gaze_point = None

# 記録用変数
is_recording = False
recorded_data = []  # (timestamp, gaze_x, gaze_y)
record_count = 0  # 録画回数を追跡する変数
video_writer_expert = None
video_writer_beginner = None

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
    x_filtered = (1 - alpha) * previous_filtered_gaze[0] + alpha * current_gaze[0]
    y_filtered = (1 - alpha) * previous_filtered_gaze[1] + alpha * current_gaze[1]
    return (x_filtered, y_filtered)

def overlay_gaze_on_frame(frame, gaze_data):
    global gaze_history, last_gaze_point, filtered_gaze_point, is_recording, recorded_data

    if gaze_data:
        gaze_point = gaze_data['left_gaze_point_on_display_area']
        x, y = gaze_point[0], gaze_point[1]
        if not (math.isnan(x) or math.isnan(y)):
            x = int(x * frame.shape[1])
            y = int(y * frame.shape[0])
            current_gaze_point = (x, y)
            
            filtered_gaze_point = apply_low_pass_filter(current_gaze_point, filtered_gaze_point, LOW_PASS_FILTER_ALPHA)
            if filtered_gaze_point is None:
                filtered_gaze_point = current_gaze_point

            if 0 <= filtered_gaze_point[0] < frame.shape[1] and 0 <= filtered_gaze_point[1] < frame.shape[0]:
                if ENABLE_TRAILS:
                    if last_gaze_point:
                        gaze_change = compute_gaze_change(filtered_gaze_point, last_gaze_point)
                        num_trails = max(1, min(10, int((gaze_change / SPEED_THRESHOLD) * 10)))
                        gaze_history = deque(gaze_history, maxlen=num_trails)
                    gaze_history.append(filtered_gaze_point)
                    last_gaze_point = filtered_gaze_point

                x, y = filtered_gaze_point
                x, y = int(x), int(y)
                cv2.circle(frame, (x, y), CIRCLE_RADIUS, CIRCLE_COLOR, CIRCLE_THICKNESS)

                if ENABLE_TRAILS:
                    for i, (x, y) in enumerate(gaze_history):
                        alpha = (i + 1) / len(gaze_history)
                        if 0 <= x < frame.shape[1] and 0 <= y < frame.shape[0]:
                            x, y = int(x), int(y)
                            cv2.circle(frame, (x, y), CIRCLE_RADIUS, CIRCLE_COLOR, CIRCLE_THICKNESS)

                # 記録中の場合、データを保存
                if is_recording:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                    recorded_data.append((timestamp, x, y))

            else:
                filtered_gaze_point = None
                gaze_history.clear()
                last_gaze_point = None
        else:
            filtered_gaze_point = None
            gaze_history.clear()
            last_gaze_point = None
    else:
        filtered_gaze_point = None
        gaze_history.clear()
        last_gaze_point = None
    
    return frame

def main():
    global is_recording, recorded_data, record_count, video_writer_expert, video_writer_beginner
    frame_time = 1.0 / TARGET_FPS

    camera_feed = capture_camera_feed()
    
    # カメラのフレームレートを取得
    actual_fps = camera_feed.get(cv2.CAP_PROP_FPS)
    print(actual_fps)
    if actual_fps == 0:
        # フレームレートの取得に失敗した場合、デフォルト値を設定
        actual_fps = TARGET_FPS

    found_eyetrackers = tr.find_all_eyetrackers()
    if not found_eyetrackers:
        print("アイトラッカーが見つかりませんでした。接続を確認してください。")
        return
    
    eye_tracker = found_eyetrackers[0]

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

            frame_resized = resize_frame(frame, MACBOOK_SCREEN_WIDTH, MACBOOK_SCREEN_HEIGHT)

            with gaze_data_lock:
                gaze_data = global_gaze_data

            frame_with_gaze = overlay_gaze_on_frame(frame_resized.copy(), gaze_data)
            
            # 録画中の場合、フレームを書き込み
            if is_recording:
                video_writer_expert.write(frame_resized)
                video_writer_beginner.write(frame_with_gaze)

            # 映像表示
            cv2.imshow("expert", frame_resized)
            cv2.imshow("beginner", frame_with_gaze)

            elapsed_time = time.time() - frame_start_time
            wait_time = frame_time - elapsed_time
            if wait_time > 0:
                time.sleep(wait_time)

            frame_count += 1

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):  # 's'キーで記録開始/停止
                if is_recording:
                    # 録画停止
                    print("Recording stopped.")
                    
                    # ビデオライターをリリース
                    video_writer_expert.release()
                    video_writer_beginner.release()
                    
                    # CSVファイルに記録を保存
                    if recorded_data:
                        with open(exportPath, 'w', newline='') as csvfile:
                            csv_writer = csv.writer(csvfile)
                            csv_writer.writerow(['timestamp', 'x', 'y'])
                            csv_writer.writerows(recorded_data)
                        print(f"Gaze data saved to {exportPath}.")
                        print(f"expert video saved to {video_path_expert}.")
                        print(f"beginner video saved to {video_path_beginner}.")
                        recorded_data = []
                    
                    is_recording = False
                else:
                    # 録画開始
                    record_count += 1
                    print(f"------------------{record_count}-------------------")
                    print("Recording started.")
                    
                    # 録画ファイルのパスを設定
                    video_path_expert = os.path.join(dirPath, f"expert_{record_count}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
                    video_path_beginner = os.path.join(dirPath, f"beginner_{record_count}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
                    exportPath = dirPath + "/" + f'gaze_data_{record_count}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
                    
                    # ビデオライターを初期化
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    video_writer_expert = cv2.VideoWriter(video_path_expert, fourcc, TARGET_FPS, (MACBOOK_SCREEN_WIDTH, MACBOOK_SCREEN_HEIGHT))
                    video_writer_beginner = cv2.VideoWriter(video_path_beginner, fourcc, TARGET_FPS, (MACBOOK_SCREEN_WIDTH, MACBOOK_SCREEN_HEIGHT))
                    
                    is_recording = True
                    recorded_data = []

    except KeyboardInterrupt:
        pass

    camera_feed.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
