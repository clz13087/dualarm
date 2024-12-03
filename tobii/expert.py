import cv2
import tobii_research as tr
import threading
import datetime
import csv
import os
import time
import math
import socket
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)

# -------------------------------------------------------- 　入力　　-----------------------------------------------------------------
dirPath = "/Users/sanolab/this mac/大学/研究室/M2/SI2024/test/3"
os.makedirs(dirPath, exist_ok=True)

MACBOOK_SCREEN_WIDTH = 1280
MACBOOK_SCREEN_HEIGHT = 720

is_exportdata = False
scale_factor = 2  # 倍率を指定（例: 2倍）
video_fps = 10  # 録画するフレームレート
desired_fps = 10 #プログラムのfps

using_tobii = False

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.bind(('133.68.108.26', 8000))
# -----------------------------------------------------------------------------------------------------------------------------------


is_recording = False
recorded_data = []  # (timestamp, gaze_x, gaze_y)
record_count = 0  # 録画回数を追跡する変数
s_flag = 0

video_writer_beginner = None  # 視線重畳の映像
video_writer_expert = None  # 生の映像

global_gaze_data = None
gaze_data_lock = threading.Lock()
s_switch_lock = threading.Lock()
last_time = time.time()

def receive_s_switch():
    global s_flag
    while True:
        try:
            udp_data, addr = udp_sock.recvfrom(1024)
            with s_switch_lock:  # ロックを取得
                if udp_data == b's':
                    s_flag = 1
        except BlockingIOError:
            pass

# 再生速度の計算とフレームレート固定
def fix_framerate(process_duration, looptime):
    sleeptime = looptime - process_duration
    if sleeptime > 0:
        time.sleep(sleeptime)

# 1秒ごとにFPSを出力する関数
def output_fps():
    global frame_count, last_time
    current_time = time.time()
    if current_time - last_time > 1.0:
        fps = frame_count/(current_time - last_time)
        logging.info(f"FPS: {fps:.2f}")
        frame_count = 0
        last_time = current_time

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

def overlay_gaze_on_frame(frame, gaze_data):
    if gaze_data:
        gaze_point = gaze_data['left_gaze_point_on_display_area']
        x, y = gaze_point[0], gaze_point[1]
        if not (math.isnan(x) or math.isnan(y)):
            x = int(x * frame.shape[1])
            y = int(y * frame.shape[0])

            if 0 <= x < frame.shape[1] and 0 <= y < frame.shape[0]:
                cv2.circle(frame, (x, y), 10, (0, 0, 255), 2)

                # 録画中の場合、データを保存
                if is_recording:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                    recorded_data.append((timestamp, x, y))

    return frame

def apply_zoom(frame, scale_factor):
    # カメラ映像のズーム処理
    center_x, center_y = frame.shape[1] // 2, frame.shape[0] // 2  # フレームの中心座標
    zoom_width, zoom_height = frame.shape[1] // scale_factor, frame.shape[0] // scale_factor  # ズーム後のサイズ
    x1 = max(center_x - zoom_width // 2, 0)
    y1 = max(center_y - zoom_height // 2, 0)
    x2 = min(center_x + zoom_width // 2, frame.shape[1])
    y2 = min(center_y + zoom_height // 2, frame.shape[0])

    # ズーム領域の切り抜き
    zoomed_frame = frame[y1:y2, x1:x2]

    # ズーム後のフレームをディスプレイサイズにリサイズ
    zoomed_frame_resized = cv2.resize(zoomed_frame, (MACBOOK_SCREEN_WIDTH, MACBOOK_SCREEN_HEIGHT))

    return zoomed_frame_resized


camera_feed = capture_camera_feed()

found_eyetrackers = tr.find_all_eyetrackers()
if not found_eyetrackers:
    print("アイトラッカーが見つかりませんでした。接続を確認してください。")

if using_tobii:
    eye_tracker = found_eyetrackers[0]
    gaze_thread = threading.Thread(target=gaze_data_thread, args=(eye_tracker,), daemon=True)
    gaze_thread.start()

s_switch_thread = threading.Thread(target=receive_s_switch, daemon=True)
s_switch_thread.start()

program_start_time = time.perf_counter()
frame_count = 0
loop_count = 0

try:
    while True:
        loop_start_time = time.perf_counter()

        # for udp s
        key = cv2.waitKey(1) & 0xFF
        if s_flag == 1:
            key = ord('s')
            s_flag = 0
        else:
            pass

        ret, frame = camera_feed.read()
        if not ret:
            break

        # ズームを適用
        frame_with_zoom = apply_zoom(frame, scale_factor)

        # フレームをMacの解像度にリサイズ
        frame_resized = cv2.resize(frame_with_zoom, (MACBOOK_SCREEN_WIDTH, MACBOOK_SCREEN_HEIGHT))

        with gaze_data_lock:
            gaze_data = global_gaze_data

        frame_with_gaze = overlay_gaze_on_frame(frame_resized.copy(), gaze_data)  # 視線重畳したフレーム
        frame_expert = frame_resized.copy()  # 生のフレーム

        cv2.imshow("Beginner", frame_with_gaze)
        cv2.imshow("Expert", frame_expert)

        # 録画が開始されている場合、フレームを書き込み
        if is_recording:
            if video_writer_beginner is not None:
                video_writer_beginner.write(frame_with_gaze)  # 視線重畳の映像
            if video_writer_expert is not None:
                video_writer_expert.write(frame_expert)  # 生の映像

        if key == ord('q'):
            break
        elif key == ord('s'):  # 's'キーで記録開始/停止
            if is_recording:
                logging.info(f"------------------------------------robot stop---------------------------------------------")

                if is_exportdata:
                    with open(exportPath, 'w', newline='') as csvfile:
                        csv_writer = csv.writer(csvfile)
                        csv_writer.writerow(['timestamp', 'x', 'y'])
                        csv_writer.writerows(recorded_data)
                    
                    if video_writer_beginner is not None:
                        video_writer_beginner.release()
                        video_writer_beginner = None
                    if video_writer_expert is not None:
                        video_writer_expert.release()
                        video_writer_expert = None

                    logging.info(f"Gaze data saved to {exportPath}.")
                    logging.info(f"expert video saved to {expert_video_path}.")
                    logging.info(f"beginner video saved to {beginner_video_path}.")

                recorded_data.clear()
                is_recording = False
            else:
                is_recording = True
                record_count += 1
                logging.info(f"------------------------------------robot start--------------------------------------------")
                if is_exportdata:
                    exportPath = os.path.join(dirPath, f'gaze_data_{record_count}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
                    beginner_video_path = os.path.join(dirPath, f'beginner_video_{record_count}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.mp4')
                    expert_video_path = os.path.join(dirPath, f'expert_video_{record_count}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.mp4')
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4形式用のコーデック
                    video_writer_beginner = cv2.VideoWriter(beginner_video_path, fourcc, video_fps, (MACBOOK_SCREEN_WIDTH, MACBOOK_SCREEN_HEIGHT))
                    video_writer_expert = cv2.VideoWriter(expert_video_path, fourcc, video_fps, (MACBOOK_SCREEN_WIDTH, MACBOOK_SCREEN_HEIGHT))
                    logging.info(f"録画開始")

        # フレームカウントの増加と1秒ごとのFPS出力
        frame_count += 1
        loop_count += 1
        output_fps()

        # 固定フレームレート維持
        fix_framerate(time.perf_counter() - loop_start_time, 1 / desired_fps)

except KeyboardInterrupt:
    print("\nKeyboardInterrupt >> stop mainloop")

finally:
    # プログラム終了時に最終FPSを表示
    if loop_count > 0:
        elapsed_time = time.perf_counter() - program_start_time
        final_fps = loop_count / elapsed_time
        print(f"Average FPS: {final_fps:.2f}")

    camera_feed.release()
    if video_writer_beginner is not None:
        video_writer_beginner.release()
    if video_writer_expert is not None:
        video_writer_expert.release()
    cv2.destroyAllWindows()