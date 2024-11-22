import glob
import pandas as pd
from matplotlib import pyplot as plt
from scipy.signal import butter, filtfilt

# バターワースフィルター関数
def butter_lowpass_filter(data, cutoff=0.1, fs=1.0, order=2):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)

# ファイルの読み込み
file_record = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/SI2024/tsugumidata/mocap/8/Transform_Participant_1*')
file_before = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/SI2024/yamashitadata/mocap/10/Transform_Participant_1*')
file_after = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/SI2024/yamashitadata/mocap/10/Transform_Participant_5*')

# file_record = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/SI2024/yamashitadata/fordtw/record/Transform_Robot_1*')
# file_before = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/SI2024/yamashitadata/fordtw/before/Transform_Robot_1*')
# file_after = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/SI2024/yamashitadata/fordtw/before/Transform_Robot_1*')

# file_record = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/SI2024/yamashitadata/fordtw/record/Transform_Participant_1*')
# file_before = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/SI2024/yamashitadata/fordtw/before/Transform_Participant_1*')
# file_after = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/SI2024/yamashitadata/fordtw/before/Transform_Participant_5*')

datasets = {"record": None, "before": None, "after": None}
for key, files in zip(datasets.keys(), [file_record, file_before, file_after]):
    for name in files:
        datasets[key] = pd.read_csv(name)

# フィルタ適用対象のカラム
columns_to_filter = ["x", "y", "z", "qx", "qy", "qz", "qw", "weightpos"]
columns_to_filter = ["x", "y", "z", "qx", "qy", "qz", "qw"]

# サンプリング周波数（仮定）とフィルターの設定
fs = 200.0  # サンプリング周波数 [Hz]
cutoff = 10.0  # カットオフ周波数 [Hz]
order = 4  # フィルターの次数

# データにフィルターを適用
for key, data in datasets.items():
    for col in columns_to_filter:
        data[f"{col}_filtered"] = butter_lowpass_filter(data[col], cutoff=cutoff, fs=fs, order=order)

# グラフの作成
fig, axes = plt.subplots(4, 2, figsize=(18, 10))
positions = ["x", "y", "z"]
orientations = ["qx", "qy", "qz", "qw"]

# 位置データの描画（1行目）
for i, pos in enumerate(positions):
    for key, color in zip(datasets.keys(), ['dimgray', 'darkblue', 'darkorange']):
        axes[i, 0].plot(datasets[key]["time"], datasets[key][f"{pos}_filtered"], c=color, label=f'{key}')
    axes[i, 0].set_title(pos)
    axes[i, 0].set_xlabel('time [s]')
    axes[i, 0].set_ylabel(f'{pos} [m]')
    axes[i, 0].legend()
    axes[i, 0].grid()


# 姿勢データの描画（2行目）
for i, ori in enumerate(orientations):
    for key, color in zip(datasets.keys(), ['dimgray', 'darkblue', 'darkorange']):
        axes[i, 1].plot(datasets[key]["time"], datasets[key][f"{ori}_filtered"], c=color, label=f'{key}')
    axes[i, 1].set_title(ori)
    axes[i, 1].set_xlabel('time [s]')
    axes[i, 1].set_ylabel(f'{ori}')
    axes[i, 1].legend()
    axes[i, 1].grid()

# ratio
# axes[3, 0].plot(datasets["record"]["time"], datasets["record"]["weightpos"], c='dimgray', label='record')
# axes[3, 0].plot(datasets["before"]["time"], datasets["before"]["weightpos"], c='darkblue', label='before')
# axes[3, 0].plot(datasets["after"]["time"], datasets["after"]["weightpos"], c='darkorange', label='after')
# axes[3, 0].set_xlabel('time[s]')
# axes[3, 0].set_ylabel('ratio[-]')
# axes[3, 0].set_title('ratio')
# axes[3, 0].legend()

axes[3, 0].axis('off')

plt.tight_layout()
plt.show()