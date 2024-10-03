import cv2
import numpy as np
import glob
import time
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)

# 動画ファイルのパス
# video_path = glob.glob("/Users/sanolab/this mac/大学/研究室/M2/SI2024/expertdata/gaze/1-7/*expert_video_30*.mp4")[0]
video_path = glob.glob("/Users/sanolab/this mac/大学/研究室/M2/SI2024/expertdata/gaze/8-37/*expert_video_30*.mp4")[0]
# video_path = glob.glob("/Users/sanolab/this mac/大学/研究室/M2/SI2024/expertdata/gaze/1-7/*beginner_video_5*.mp4")[0]
# video_path = glob.glob("/Users/sanolab/this mac/大学/研究室/M2/SI2024/expertdata/gaze/8-37/*beginner_video_30*.mp4")[0]

# カメラの初期化
camera = cv2.VideoCapture(0)

# 動画の初期化
video = cv2.VideoCapture(video_path)

# 動画のFPS取得
video_fps = video.get(cv2.CAP_PROP_FPS)

# メインループのFPS（例: 30FPS）
desired_fps = 14.6
delay = int(1000 / desired_fps)

# 動画の最初のフレームを取得
ret, first_frame = video.read()

# カメラのフレームサイズを取得
camera_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
camera_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Macのディスプレイサイズに合わせる（仮に1280x800に設定）
display_width, display_height = 1280, 800

# ウィンドウの設定
cv2.namedWindow('Overlay', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Overlay', display_width, display_height)

# 動画のフレームをディスプレイサイズにリサイズ
first_frame = cv2.resize(first_frame, (display_width, display_height))

# 透過率(録画の割合)
alpha = 0.5

# FPS計算用の変数
frame_count = 0
start_time = time.time()
fps_list = []

# キーが押されたかを管理
key_pressed = False

# プログラムのメインループ
while True:
    # カメラのフレームを取得
    ret, camera_frame = camera.read()
    if not ret:
        break

    # カメラ映像のリサイズ
    camera_frame = cv2.resize(camera_frame, (display_width, display_height))

    # 最初のフレームをカメラ映像に透過合成
    overlay_frame = cv2.addWeighted(camera_frame, 1 - alpha, first_frame, alpha, 0)

    # キー入力の処理
    key = cv2.waitKey(delay) & 0xFF  # 指定されたFPSに基づいた待機時間
    if key == ord('s'):
        key_pressed = True  # 's'キーが押された場合にフラグを立てる
    elif key == ord('q'):
        break  # 'q'キーが押された場合にプログラムを終了

    # 's'キーが押されたら動画を再生
    if key_pressed:
        ret, video_frame = video.read()
        if ret:
            # 動画フレームもカメラフレームにリサイズして透過合成
            video_frame = cv2.resize(video_frame, (display_width, display_height))
            overlay_frame = cv2.addWeighted(camera_frame, 1 - alpha, video_frame, alpha, 0)

    # 結果を表示
    cv2.imshow('Overlay', overlay_frame)
    
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
cv2.destroyAllWindows()
