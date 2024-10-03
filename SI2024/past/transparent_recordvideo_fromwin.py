import cv2
import numpy as np
import glob
import time
import logging
import os
import datetime
import socket

# ログ設定
logging.basicConfig(level=logging.INFO)

# -------------------------------------------------------- 　入力　　-----------------------------------------------------------------

# 動画ファイルのパス
# video_path = glob.glob("/Users/sanolab/this mac/大学/研究室/M2/SI2024/expertdata/gaze/1-7/*expert_video_2*.mp4")[0]
video_path = glob.glob("/Users/sanolab/this mac/大学/研究室/M2/SI2024/expertdata/gaze/8-37/*expert_video_30*.mp4")[0]
# video_path = glob.glob("/Users/sanolab/this mac/大学/研究室/M2/SI2024/expertdata/gaze/1-7/*beginner_video_5*.mp4")[0]
# video_path = glob.glob("/Users/sanolab/this mac/大学/研究室/M2/SI2024/expertdata/gaze/8-37/*beginner_video_30*.mp4")[0]

# video_path = glob.glob("/Users/sanolab/this mac/大学/研究室/M2/SI2024/expertdata/gaze/tsugumi/1/*expert_video_1*.mp4")[0]

# 保存先のパス
dirPath = "/Users/sanolab/this mac/大学/研究室/M2/SI2024/beginnerdata/2"
os.makedirs(dirPath, exist_ok=True)

# メインループのFPS（例: 14.6FPS）
desired_fps = 15
delay = int(1000 / desired_fps)

# 録画のfps
record_fps = 10

# Macのディスプレイサイズに合わせる（仮に1280x800に設定）
display_width, display_height = 1280, 800

# 透過率(録画の割合)
alpha = 0

# ----------------------------------------------------------------------------------------------------------------------------------

# UDPソケットを設定
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.bind(('133.68.108.26', 8000))

# ソケットを非ブロッキングモードに設定
udp_sock.setblocking(0)


# カメラの初期化
camera = cv2.VideoCapture(0)

# 動画の初期化
video = cv2.VideoCapture(video_path)

# 動画のFPS取得
video_fps = video.get(cv2.CAP_PROP_FPS)

# 動画の最初のフレームを取得
ret, first_frame = video.read()

# カメラのフレームサイズを取得
camera_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
camera_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

# ウィンドウの設定
cv2.namedWindow('Overlay', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Overlay', display_width, display_height)

# 動画のフレームをディスプレイサイズにリサイズ
first_frame = cv2.resize(first_frame, (display_width, display_height))

# FPS計算用の変数
frame_count = 0
start_time = time.time()
fps_list = []

# 録画関連の変数
is_recording = False
record_count = 0
video_writer = None

# sキーのトグル管理用
play_video = False

# プログラムのメインループ
while True:
    # キー入力の処理
    key = cv2.waitKey(delay) & 0xFF  # 指定されたFPSに基づいた待機時間

    try:
        # ソケットで受信
        data, addr = udp_sock.recvfrom(1024)
        print(f"Received message: {data} from {addr}")
        if data == b's':
            key = ord('s')  # sキーを押されたとみなす
    except BlockingIOError:
        # データが受信できなかった場合はスキップ
        pass

    # カメラのフレームを取得
    ret, camera_frame = camera.read()
    if not ret:
        break

    # カメラ映像のリサイズ
    camera_frame = cv2.resize(camera_frame, (display_width, display_height))

    # 最初のフレームをカメラ映像に透過合成
    overlay_frame = cv2.addWeighted(camera_frame, 1 - alpha, first_frame, alpha, 0)

    if key == ord('s'):
        # sキーが押された時のトグル動作
        if is_recording:
            # 録画停止と動画リセット
            is_recording = False
            play_video = False
            video_writer.release()
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 動画を最初に戻す
            logging.info(f"録画停止: {beginner_video_path}")
        else:
            # 録画開始と動画再生
            is_recording = True
            play_video = True
            record_count += 1
            beginner_video_path = os.path.join(dirPath, f'beginner_video_{record_count}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.mp4')
            video_writer = cv2.VideoWriter(beginner_video_path, cv2.VideoWriter_fourcc(*'mp4v'), record_fps, (display_width, display_height))
            logging.info(f"録画開始: {beginner_video_path}")

    elif key == ord('q'):
        break  # 'q'キーが押された場合にプログラムを終了

    # 動画を再生
    if play_video:
        ret, video_frame = video.read()
        if ret:
            # 動画フレームもカメラフレームにリサイズして透過合成
            video_frame = cv2.resize(video_frame, (display_width, display_height))
            overlay_frame = cv2.addWeighted(camera_frame, 1 - alpha, video_frame, alpha, 0)
        else:
            play_video = False  # 動画が終わったら再生停止
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 動画を最初に戻す

    # 結果を表示
    cv2.imshow('Overlay', overlay_frame)

    # 録画中であればフレームを書き込む
    if is_recording:
        video_writer.write(overlay_frame)

    # FPSの計算
    frame_count += 1
    elapsed_time = time.time() - start_time
    if elapsed_time > 1.0:  # 1秒ごとにFPSを表示
        fps = frame_count / elapsed_time
        fps_list.append(fps)
        logging.info(f"FPS: {fps:.2f}")
        frame_count = 0
        start_time = time.time()

# 平均FPSの計算
if fps_list:
    avg_fps = sum(fps_list) / len(fps_list)
    logging.info(f"平均FPS: {avg_fps:.2f}")

# リソース解放
camera.release()
video.release()
if video_writer is not None:
    video_writer.release()
cv2.destroyAllWindows()
