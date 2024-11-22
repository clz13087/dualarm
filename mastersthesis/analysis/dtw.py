from turtle import color
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob
import japanize_matplotlib
from fastdtw import fastdtw
import seaborn as sns
from scipy.signal import butter, filtfilt

file_record = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/SI2024/yamashitadata/fordtw/record/Transform_Robot_1*')
file_before = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/SI2024/yamashitadata/fordtw/before/Transform_Robot_1*')
file_after = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/SI2024/yamashitadata/fordtw/after/Transform_Robot_1*')

# file_record = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/SI2024/tsugumidata/mocap/8/Transform_Participant_1*')
# file_before = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/SI2024/yamashitadata/mocap/1/Transform_Participant_1*')
# file_after = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/SI2024/yamashitadata/mocap/10/Transform_Participant_1*')

for name in file_record:
    dat_record = pd.read_csv(name)
for name in file_before:
    dat_before = pd.read_csv(name)
for name in file_after:
    dat_after = pd.read_csv(name)

def euclidean_distance_3d(practice, expert):
    return np.sqrt((practice[0] - expert[0]) ** 2 + (practice[1] - expert[1]) ** 2 + (practice[2] - expert[2]) ** 2)

# バターワースフィルターの適用
def butter_lowpass_filter(data, cutoff, fs, order):
    nyquist = 0.5 * fs  # ナイキスト周波数
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data, axis=0)
    return y

# 微分計算
def compute_derivative(data):
    kernel = np.array([1, 0, -1]) / 2.0  # 差分カーネル
    derivative = np.apply_along_axis(lambda col: np.convolve(col, kernel, mode='same'), axis=0, arr=data)
    return derivative

def calculate_dtw_ddtw_ratio(dat_expert, dat_before, dat_after, cutoff, fs, order):
    # 各データセットのx, y, zのデータを取得
    x_expert, y_expert, z_expert = dat_expert['x'], dat_expert['y'], dat_expert['z']
    x_before, y_before, z_before = dat_before['x'], dat_before['y'], dat_before['z']
    x_after, y_after, z_after = dat_after['x'], dat_after['y'], dat_after['z']

    # numpy配列に変換
    expert_data = np.array([x_expert, y_expert, z_expert]).T
    before_data = np.array([x_before, y_before, z_before]).T
    after_data = np.array([x_after, y_after, z_after]).T

    # フィルター適用
    expert_filtered = butter_lowpass_filter(expert_data, cutoff, fs, order)
    before_filtered = butter_lowpass_filter(before_data, cutoff, fs, order)
    after_filtered = butter_lowpass_filter(after_data, cutoff, fs, order)

    # DTW計算
    distance_dtw_before, _ = fastdtw(before_filtered, expert_filtered, dist=euclidean_distance_3d)
    distance_dtw_after, _ = fastdtw(after_filtered, expert_filtered, dist=euclidean_distance_3d)

    # 微分データの計算
    expert_derivative = compute_derivative(expert_filtered)
    before_derivative = compute_derivative(before_filtered)
    after_derivative = compute_derivative(after_filtered)

    # DDTW計算
    distance_ddtw_before, _ = fastdtw(before_derivative, expert_derivative, dist=euclidean_distance_3d)
    distance_ddtw_after, _ = fastdtw(after_derivative, expert_derivative, dist=euclidean_distance_3d)

    # 無次元化
    dtw_ratio = distance_dtw_after / distance_dtw_before
    ddtw_ratio = distance_ddtw_after / distance_ddtw_before

    return expert_filtered, before_filtered, after_filtered, distance_dtw_before, distance_dtw_after, dtw_ratio, distance_ddtw_before, distance_ddtw_after, ddtw_ratio

def plot_position_and_velocity(raw_data, time_data, filtered_data, labels, title_prefix="", axes=None):
    if axes is None:
        fig, axes = plt.subplots(3, 2, figsize=(12, 12))

    # 位置データのプロット (x, y, zごとに分けて)
    for i, label in enumerate(labels):
        axes[i, 0].plot(time_data, raw_data[:, i], linestyle='--', alpha=0.8, label=f"{title_prefix} (raw)")
        axes[i, 0].plot(time_data, filtered_data[:, i], label=f"{title_prefix} (filtered)")
        axes[i, 0].set_title(f"{label} Position")
        axes[i, 0].legend(loc='upper right')
        axes[i, 0].grid()

    # 速度データのプロット (x, y, zごとに分けて)
    velocity = compute_derivative(filtered_data)
    for i, label in enumerate(labels):
        axes[i, 1].plot(time_data, velocity[:, i], label=f"{title_prefix} velocity")
        axes[i, 1].set_title(f"{label} Velocity")
        axes[i, 1].legend(loc='upper right')
        axes[i, 1].grid()
        axes[i, 1].set_ylim(-0.0005, 0.0005)
    
# fordtw,ddtw
cutoff = 5  # カットオフ周波数
fs = 200  # サンプリング周波数
order = 4
filtered_expert, filtered_before, filtered_after, distance_dtw_before, distance_dtw_after, dtw_ratio, distance_ddtw_before, distance_ddtw_after, ddtw_ratio = calculate_dtw_ddtw_ratio(dat_record, dat_before, dat_after, cutoff, fs, order)
print(f"DTW - Distance Before: {distance_dtw_before:.2f}, Distance After: {distance_dtw_after:.2f}, Ratio: {dtw_ratio:.2f}")
print(f"DDTW - Distance Before: {distance_ddtw_before:.2f}, Distance After: {distance_ddtw_after:.2f}, Ratio: {ddtw_ratio:.2f}")

# forplot
fig, axes = plt.subplots(3, 2, figsize=(20, 12))
plot_position_and_velocity(np.array([dat_record['x'], dat_record['y'], dat_record['z']]).T, dat_record["time"], filtered_expert, labels=["x", "y", "z"], title_prefix="expert", axes=axes)
plot_position_and_velocity(np.array([dat_before['x'], dat_before['y'], dat_before['z']]).T, dat_before["time"], filtered_before, labels=["x", "y", "z"], title_prefix="before", axes=axes)
plot_position_and_velocity(np.array([dat_after['x'], dat_after['y'], dat_after['z']]).T, dat_after["time"], filtered_after, labels=["x", "y", "z"], title_prefix="after", axes=axes)
plt.tight_layout()
plt.show()