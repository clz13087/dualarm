from turtle import color
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob
import japanize_matplotlib
from fastdtw import fastdtw
import seaborn as sns

file_record = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/SI2024/tsugumidata/mocap/8/Transform_Participant_1*')
file_before = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/SI2024/yamashitadata/mocap/1/Transform_Participant_1*')
file_after = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/SI2024/yamashitadata/mocap/10/Transform_Participant_1*')

for name in file_record:
    dat_record = pd.read_csv(name)
for name in file_before:
    dat_before = pd.read_csv(name)
for name in file_after:
    dat_after = pd.read_csv(name)

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

distance_before_expert, distance_after_expert, dtw_ratio = calculate_dtw_ratio(dat_record, dat_before, dat_after)

print(distance_before_expert, distance_after_expert, dtw_ratio)