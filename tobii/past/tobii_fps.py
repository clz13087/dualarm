import tobii_research as tr
import time

# 目のトラッカーを検出
eyetrackers = tr.find_all_eyetrackers()

if not eyetrackers:
    print("Eyetracker not found.")
    exit()

eyetracker = eyetrackers[0]

# FPSの計算に使用する変数
frame_count = 0
start_time = time.time()

def gaze_data_callback(gaze_data):
    global frame_count
    frame_count += 1

# Gazeデータのストリームを開始
eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)

try:
    while True:
        # 一定時間ごとにFPSを計算
        elapsed_time = time.time() - start_time
        if elapsed_time > 1.0:
            fps = frame_count / elapsed_time
            frame_count = 0
            start_time = time.time()
            print(f"FPS: {fps:.2f}")

except KeyboardInterrupt:
    # プログラムが終了する際にトラッカーの購読を解除
    eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
    print("Program terminated.")
