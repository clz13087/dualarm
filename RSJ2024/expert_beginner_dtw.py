from turtle import color
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob
import japanize_matplotlib
from fastdtw import fastdtw
import seaborn as sns

# ファイルパスの設定
base_folder = '/Users/sanolab/this mac/大学/研究室/M2/RSJ2024/experiment/'
expert_folder = base_folder + 'expertdata/'
before_folder = base_folder + 'beginnerdata/'
after_folder = base_folder + 'beginnerdata/'

# 条件と被験者の設定
conditions = ['模倣', '融合']
subjects = {
    '模倣': ['sugata', 'tsuruoka'],
    '融合': ['konishi', 'taisei']
}

# データを格納するための空の辞書
data = {condition: [] for condition in conditions}

# Expertデータの読み込み
for task in range(1, 5):  # タスク1からタスク4まで
    file_expert = glob.glob(expert_folder + f'{task}/Transform_Participant_2*')
    for name in file_expert:
        dat_expert = pd.read_csv(name)
        data['模倣'].append({'subject': 'expert', 'task': f'{task}', 'data': dat_expert})
        data['融合'].append({'subject': 'expert', 'task': f'{task}', 'data': dat_expert})

# Beforeデータの読み込み
for condition in subjects:
    for subject in subjects[condition]:
        for task in range(1, 5):  # タスク1からタスク4まで
            file_before = glob.glob(before_folder + f'{subject}/before/{task}/Transform_Participant_2*')
            for name in file_before:
                dat_before = pd.read_csv(name)
                data[condition].append({'subject': subject, 'practice': 'before', 'task': f'{task}', 'data': dat_before})

# Afterデータの読み込み
for condition in subjects:
    for subject in subjects[condition]:
        for task in range(1, 5):  # タスク1からタスク4まで
            file_after = glob.glob(after_folder + f'{subject}/after/{task}/Transform_Participant_2*')
            for name in file_after:
                dat_after = pd.read_csv(name)
                data[condition].append({'subject': subject, 'practice': 'after', 'task': f'{task}', 'data': dat_after})


def euclidean_distance_3d(practice, expert):
    return np.sqrt((practice[0] - expert[0]) ** 2 + (practice[1] - expert[1]) ** 2 + (practice[2] - expert[2]) ** 2)

def calculate_dtw_ratio(dat_expert, dat_before, dat_after):
    # 各データセットのx, y, zのデータを取得
    x_expert, y_expert, z_expert = dat_expert['x'], dat_expert['y'], dat_expert['z']
    x_before, y_before, z_before = dat_before['x'], dat_before['y'], dat_before['z']
    x_after, y_after, z_after = dat_after['x'], dat_after['y'], dat_after['z']

    # numpy配列に変換
    expert_data = np.array([x_expert, y_expert, z_expert]).T
    before_data = np.array([x_before, y_before, z_before]).T
    after_data = np.array([x_after, y_after, z_after]).T

    distance_before_expert, path_before_expert = fastdtw(before_data, expert_data, dist=euclidean_distance_3d)
    distance_after_expert, path_after_expert = fastdtw(after_data, expert_data, dist=euclidean_distance_3d)

    # 無次元化
    dtw_ratio =  distance_after_expert / distance_before_expert

    return distance_before_expert, distance_after_expert, dtw_ratio


imitation = []
integration = []

# 無次元比を計算して出力する
for condition in conditions:
    print(f'-----------条件: {condition}-----------')
    for subject in subjects[condition]:
        print(f'被験者: {subject}')
        for task in range(1, 5):
            # expertデータ, beforeデータ, afterデータを取得
            expert_data = [item for item in data[condition] if item['task'] == f'{task}' and item['subject'] == 'expert'][0]
            before_data = [item for item in data[condition] if item['subject'] == f'{subject}' and item['task'] == f'{task}' and item['practice'] == 'before'][0]
            after_data = [item for item in data[condition] if item['subject'] == f'{subject}' and item['task'] == f'{task}' and item['practice'] == 'after'][0]
            
            # calculate_dimensionless_ratio 関数に渡して無次元比を計算
            distance_before_expert, distance_after_expert, dtw_ratio = calculate_dtw_ratio(expert_data['data'], before_data['data'], after_data['data'])
            if condition == '模倣':
                imitation.append(dtw_ratio)
            elif condition == '融合':
                integration.append(dtw_ratio)
            
            # 結果を出力
            print(f'  task {task}: dtw ratio = {dtw_ratio}')

# 箱ひげ図とデータポイントのプロット
plt.figure(figsize=(4, 3))
df = pd.DataFrame({
    'Condition': ['模倣'] * len(imitation) + ['融合'] * len(integration),
    'Ratio': imitation + integration
})

# 箱ひげ図を作成
sns.boxplot(x='Condition', y='Ratio', data=df, showfliers=False, boxprops=dict(facecolor='white', edgecolor='k'))

# データポイントをプロット
# sns.stripplot(x='Condition', y='Ratio', data=df, jitter=True, color='black', dodge=True)

# 軸のラベルを設定
plt.xlabel('')
plt.ylabel('DTWの練習前後の比')

plt.savefig('/Users/sanolab/miniforge3/envs/test/RSJ2024/fig/dtw.pdf')
plt.savefig('/Users/sanolab/miniforge3/envs/test/RSJ2024/fig/dtw.png')
plt.savefig('/Users/sanolab/this mac/大学/研究室/M2/RSJ2024/tex/2024j_tex_tsugumi/fig/dtw.pdf')