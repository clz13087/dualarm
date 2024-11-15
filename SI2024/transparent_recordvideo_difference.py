import cv2
import numpy as np
import glob
import time
import logging
import os
import socket
import threading
import datetime

# ログ設定
logging.basicConfig(level=logging.INFO)

# -------------------------------------------------------- 　入力　　-----------------------------------------------------------------
# 動画ファイルのパス
video_path = glob.glob("/Users/sanolab/this mac/大学/研究室/M2/SI2024/tsugumidata/expert_gaze/8/*beginner_video_1*.mp4")[0]

# 保存先のパス
dirPath = "/Users/sanolab/this mac/大学/研究室/M2/SI2024/tsugumidata/beginner/other4"
os.makedirs(dirPath, exist_ok=True)
is_exportdata = False

# 基本設定
desired_fps = 10
robotside_fps = 200
record_fps = 10
display_width, display_height = 1280, 720
alpha = 0.5
scale_factor = 2

# UDPソケットを設定
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.bind(('133.68.108.26', 8000))
# -----------------------------------------------------------------------------------------------------------------------------------

# スレッド関数で差分データを受信し `robotside_fps` を更新
lock = threading.Lock()

def receive_diff_data():
    global desired_fps, delay, s_flag, robotside_fps
    while True:
        try:
            udp_data, addr = udp_sock.recvfrom(1024)
            with lock:  # ロックを取得
                if udp_data == b's':
                    s_flag = 1
                else:
                    robotside_fps = float(udp_data.decode())
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

# スレッド開始
diff_thread = threading.Thread(target=receive_diff_data)
diff_thread.start()

# カメラと動画の初期化
camera = cv2.VideoCapture(0)
video = cv2.VideoCapture(video_path)
video_fps = video.get(cv2.CAP_PROP_FPS)

# 最初のフレームを取得
ret, first_frame = video.read()
if ret:
    first_frame = cv2.resize(first_frame, (display_width, display_height))

# メインループのための初期設定
play_video = False
s_flag = 0
video_playback_time = 0.0
loop_start_time = time.perf_counter()
frame_count = 0
last_time = time.time()

# 録画関連の変数
is_recording = False
record_count = 0
video_writer = None

# ウィンドウの設定
cv2.namedWindow('Overlay', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Overlay', display_width, display_height)

# プログラムのメインループ
while True:
    key = cv2.waitKey(1) & 0xFF

    if s_flag == 1:
        key = ord('s')
        s_flag = 0
    else:
        pass

    # カメラのフレーム取得
    ret, camera_frame = camera.read()
    if not ret:
        break

    # ズーム処理
    center_x, center_y = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)) // 2, int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)) // 2
    zoom_width, zoom_height = int(center_x / scale_factor), int(center_y / scale_factor)
    zoomed_camera_frame = camera_frame[center_y-zoom_height:center_y+zoom_height, center_x-zoom_width:center_x+zoom_width]
    zoomed_camera_frame_resized = cv2.resize(zoomed_camera_frame, (display_width, display_height))

    # 再生速度の計算 (例: robotside_fps を基に再生速度変更)
    playback_speed = 0.5 + (robotside_fps - 100) * (1 - 0.5) / (200 - 100)
    if play_video:
        video_playback_time += (1 / desired_fps) * playback_speed * 1000  # ミリ秒単位で再生位置を更新
        video.set(cv2.CAP_PROP_POS_MSEC, video_playback_time)
        ret, video_frame = video.read()
        if ret:
            video_frame = cv2.resize(video_frame, (display_width, display_height))
            overlay_frame = cv2.addWeighted(zoomed_camera_frame_resized, 1 - alpha, video_frame, alpha, 0)
        else:
            video_playback_time = 0  # 動画が終了したらリセット
            play_video = False
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
    else:
        # 再生が開始される前はfirst_frameを表示
        overlay_frame = cv2.addWeighted(zoomed_camera_frame_resized, 1 - alpha, first_frame, alpha, 0)

    # ゲージの描画処理
    gauge_width = int((200 - robotside_fps) *12.5)  # 最大200FPSに基づくゲージ
    difference = (200 - robotside_fps) * 0.8    # differenceのリミット8cm
    cv2.rectangle(overlay_frame, (10, display_height - 30), (10 + gauge_width, display_height - 10), (0, 255, 0), -1)
    cv2.putText(overlay_frame, f"difference: {difference:.2f}mm", (10, display_height - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

    # 画面表示
    cv2.imshow('Overlay', overlay_frame)

    # 's'キーでトグル
    if key == ord('s'):
        if is_recording:
            play_video  = False
            is_recording = False
            video_playback_time = 0 if not play_video else video_playback_time
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 動画を最初に戻す
            logging.info(f"------------------------------------robot stop---------------------------------------------")
            if is_exportdata:
                video_writer.release()
                logging.info(f"録画停止: {beginner_video_path}")
        else:
            play_video = True
            is_recording = True
            record_count += 1
            logging.info(f"------------------------------------robot start--------------------------------------------")
            if is_exportdata:
                beginner_video_path = os.path.join(dirPath, f'beginner_video_{record_count}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.mp4')
                video_writer = cv2.VideoWriter(beginner_video_path, cv2.VideoWriter_fourcc(*'mp4v'), record_fps, (display_width, display_height))
                logging.info(f"録画開始: {beginner_video_path}")

    elif key == ord('q'):
        break

    # 録画中であればフレームを書き込む
    if is_recording and is_exportdata:
        video_writer.write(overlay_frame)

    # フレームカウントの増加と1秒ごとのFPS出力
    frame_count += 1
    output_fps()

    # 固定フレームレート維持
    fix_framerate(time.perf_counter() - loop_start_time, 1 / desired_fps)
    loop_start_time = time.perf_counter()

# リソース解放
camera.release()
video.release()
if video_writer is not None:
    video_writer.release()
cv2.destroyAllWindows()