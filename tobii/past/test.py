import cv2
import tobii_research as tr
import threading
import datetime
import csv
import os
import time
import math

# 設定
dirPath = "/Users/sanolab/this mac/大学/研究室/M2/SI2024/pre/tobiitest/5"
os.makedirs(dirPath, exist_ok=True)

# MacBookの解像度
MACBOOK_SCREEN_WIDTH = 1280
MACBOOK_SCREEN_HEIGHT = 800

# 変数の初期化
is_recording = False
recorded_data = []  # (timestamp, gaze_x, gaze_y)
record_count = 0  # 録画回数を追跡する変数

video_writer = None
video_fps = 22  # 録画するフレームレート
global_gaze_data = None
gaze_data_lock = threading.Lock()

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
                cv2.circle(frame, (x, y), 15, (0, 0, 255), 3)

                # 録画中の場合、データを保存
                if is_recording:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                    recorded_data.append((timestamp, x, y))

    return frame

def main():
    global is_recording, recorded_data, record_count, video_writer

    camera_feed = capture_camera_feed()
    
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

    try:
        while True:
            frame_start_time = time.time()

            ret, frame = camera_feed.read()
            if not ret:
                break

            # フレームをMacの解像度にリサイズ
            frame_resized = cv2.resize(frame, (MACBOOK_SCREEN_WIDTH, MACBOOK_SCREEN_HEIGHT))

            with gaze_data_lock:
                gaze_data = global_gaze_data

            frame_with_gaze = overlay_gaze_on_frame(frame_resized.copy(), gaze_data)
            cv2.imshow("Gaze Tracking", frame_with_gaze)

            # 録画が開始されている場合、フレームを書き込み
            if is_recording and video_writer is not None:
                video_writer.write(frame_with_gaze)

            # FPSの計算
            frame_count += 1
            elapsed_time = time.time() - start_time
            if elapsed_time > 1.0:
                fps = frame_count / elapsed_time
                print(f"FPS: {fps:.2f}")
                frame_count = 0
                start_time = time.time()

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):  # 's'キーで記録開始/停止
                if is_recording:
                    # 録画停止
                    print("Recording stopped.")
                    if recorded_data:
                        record_count += 1
                        exportPath = os.path.join(dirPath, f'gaze_data_{record_count}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
                        with open(exportPath, 'w', newline='') as csvfile:
                            csv_writer = csv.writer(csvfile)
                            csv_writer.writerow(['timestamp', 'x', 'y'])
                            csv_writer.writerows(recorded_data)
                        print(f"Gaze data saved to {exportPath}.")
                    recorded_data.clear()
                    is_recording = False
                    if video_writer is not None:
                        video_writer.release()
                        video_writer = None
                else:
                    # 録画開始
                    is_recording = True
                    print("Recording started.")
                    video_path = os.path.join(dirPath, f'video_{record_count + 1}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.mp4')
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4形式用のコーデック
                    video_writer = cv2.VideoWriter(video_path, fourcc, video_fps, (MACBOOK_SCREEN_WIDTH, MACBOOK_SCREEN_HEIGHT))
                    print(f"Video recording started at {video_path}.")

            # 録画時間調整
            frame_processing_time = time.time() - frame_start_time
            if frame_processing_time < (1 / video_fps):
                time.sleep((1 / video_fps) - frame_processing_time)

    except KeyboardInterrupt:
        print("\nKeyboardInterrupt >> stop mainloop")

    finally:
        # プログラム終了時に最終FPSを表示
        if frame_count > 0:
            elapsed_time = time.time() - start_time
            final_fps = frame_count / elapsed_time
            print(f"Final FPS: {final_fps:.2f}")

        camera_feed.release()
        if video_writer is not None:
            video_writer.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
