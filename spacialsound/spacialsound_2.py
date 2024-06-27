import numpy as np
import pyaudio
import soundfile as sf
from scipy.spatial.transform import Rotation as R
from pysofaconventions.SOFAFile import SOFAFile
import time

# HRTFデータの読み込み（SOFAファイル形式）
sofa = SOFAFile('/Users/sanolab/this mac/大学/研究室/M2/spacialsound/hrtf/*', 'r')
hrtf_data = sofa.getDataIR()  # インパルス応答
hrtf_positions = sofa.getSourcePosition()  # HRTFの位置データ

# 音声ファイルの読み込み
audio_data, samplerate = sf.read('audio_file.wav')

# PyAudioの設定
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=2,
                rate=samplerate,
                output=True)

# バッファサイズの設定
buffer_size = 1024

# 方向ベクトルを計算する関数
def quaternion_to_direction_vector(quaternion):
    r = R.from_quat(quaternion)
    direction_vector = r.apply([0, 0, 1])  # Z軸方向を基準にする場合
    return direction_vector

# HRTFを適用する関数
def apply_hrtf(audio_chunk, direction_vector):
    azimuth = np.arctan2(direction_vector[1], direction_vector[0]) * 180 / np.pi
    elevation = np.arcsin(direction_vector[2]) * 180 / np.pi
    idx = np.argmin(np.sum((hrtf_positions[:, :2] - np.array([azimuth, elevation]))**2, axis=1))
    hrtf = hrtf_data[idx]
    left = np.convolve(audio_chunk, hrtf[:, 0])[:len(audio_chunk)]
    right = np.convolve(audio_chunk, hrtf[:, 1])[:len(audio_chunk)]
    stereo_data = np.vstack((left, right)).T
    return stereo_data

# ストリーミングデータを処理しながら音を再生
try:
    # モーションキャプチャデータのモック関数
    def get_motion_capture_data():
        # クォータニオンデータの例
        quaternion = [0, 0, 0, 1]  # ここに実際のデータ取得ロジックを追加
        return quaternion

    # 音声データをバッファに分割
    num_chunks = len(audio_data) // buffer_size
    audio_chunks = np.array_split(audio_data, num_chunks)

    for audio_chunk in audio_chunks:
        quaternion = get_motion_capture_data()
        direction_vector = quaternion_to_direction_vector(quaternion)
        hrtf_data = apply_hrtf(audio_chunk, direction_vector)
        stream.write(hrtf_data.astype(np.float32).tobytes())
        time.sleep(buffer_size / samplerate)

except KeyboardInterrupt:
    print("ストリーミング終了")

finally:
    # ストリームの終了
    stream.stop_stream()
    stream.close()
    p.terminate()
