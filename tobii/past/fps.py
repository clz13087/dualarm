import cv2
import time

# カメラを初期化
cap = cv2.VideoCapture(0)

# FPSの計算に使用する変数
fps = 0
frame_count = 0
start_time = time.time()

while True:
    # フレームをキャプチャ
    ret, frame = cap.read()
    if not ret:
        break

    # フレーム数をカウント
    frame_count += 1

    # 一定時間ごとにFPSを計算
    elapsed_time = time.time() - start_time
    if elapsed_time > 1.0:
        fps = frame_count / elapsed_time
        frame_count = 0
        start_time = time.time()
        print(f"FPS: {fps:.2f}")

    # フレームを表示
    cv2.imshow('Camera Feed', frame)

    # 'q'を押すとループを終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# リソースの解放
cap.release()
cv2.destroyAllWindows()
