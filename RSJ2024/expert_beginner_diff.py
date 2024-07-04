from turtle import color
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob
import japanize_matplotlib

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


def calculate_distance_ratio(dat_expert, dat_before, dat_after):
    # 各データセットのx, y, zのデータを取得
    x_expert, y_expert, z_expert = dat_expert['x'], dat_expert['y'], dat_expert['z']
    x_before, y_before, z_before = dat_before['x'], dat_before['y'], dat_before['z']
    x_after, y_after, z_after = dat_after['x'], dat_after['y'], dat_after['z']

    # numpy配列に変換
    expert_data = np.array([x_expert, y_expert, z_expert]).T
    before_data = np.array([x_before, y_before, z_before]).T
    after_data = np.array([x_after, y_after, z_after]).T

    def get_representative_point(data):
        idx = np.argmax(np.abs(data[:, 0]))
        return data[idx]

    # 各データセットの代表点を取得
    expert_point = get_representative_point(expert_data)
    before_point = get_representative_point(before_data)
    after_point = get_representative_point(after_data)

    # 距離を計算
    def calculate_distance(point1, point2):
        return np.linalg.norm(point1 - point2)

    distance_before_expert = calculate_distance(before_point, expert_point)
    distance_after_expert = calculate_distance(after_point, expert_point)

    # 無次元化
    distance_ratio =   distance_after_expert / distance_before_expert

    return distance_before_expert, distance_after_expert, distance_ratio


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
            distance_before_expert, distance_after_expert, distance_ratio = calculate_distance_ratio(expert_data['data'], before_data['data'], after_data['data'])
            if condition == '模倣':
                imitation.append(distance_ratio)
            elif condition == '融合':
                integration.append(distance_ratio)
            
            # 結果を出力
            print(f'  task {task}: ratio = {distance_ratio}')


# データの例
data = {
    '模倣': imitation,
    '融合': integration
}

# データをリスト形式で整理
data_list = [data['模倣'], data['融合']]

# 箱ひげ図の作成
plt.figure(figsize=(4, 3))
plt.boxplot(data_list, labels=['模倣', '融合'], showfliers=False, medianprops = dict(color='k', linewidth = 1))

# 軸のラベルを設定
# plt.xlabel('条件')
plt.ylabel('正解との差の練習前後の比')
# plt.title('模倣と融合の箱ひげ図')
plt.savefig('/Users/sanolab/miniforge3/envs/test/RSJ2024/fig/diff.pdf')
plt.savefig('/Users/sanolab/miniforge3/envs/test/RSJ2024/fig/diff.png')

# グラフの表示
plt.show()