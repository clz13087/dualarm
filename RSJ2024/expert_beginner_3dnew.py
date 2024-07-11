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

            fig = plt.figure()
            axes = fig.add_subplot(111,projection='3d')
            axes.scatter(expert_data['data']['x'],expert_data['data']['y'],expert_data['data']['z'],c='darkorange', label='expert')
            axes.scatter(before_data['data']['x'],before_data['data']['y'],before_data['data']['z'],c='dimgray', label='before')
            axes.scatter(after_data['data']['x'],after_data['data']['y'],after_data['data']['z'],c='red', label='after')
            axes.legend()
            plt.savefig(f'/Users/sanolab/miniforge3/envs/test/RSJ2024/fig/3d/{condition}_{subject}_{task}.png')
            print(f' create: {condition}_{subject}_{task}.png')