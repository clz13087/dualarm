import pandas as pd
import glob
from matplotlib import pyplot as plt

file_expert = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/RSJ2024/experiment/expertdata/4/Transform_Participant_2*')
file_before = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/RSJ2024/experiment/beginnerdata/sugata/before/4/Transform_Participant_2*')
file_after = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/RSJ2024/experiment/beginnerdata/sugata/after/4/Transform_Participant_2*')
for name in file_expert:
    dat_expert = pd.read_csv(name)
for name in file_before:
    dat_before = pd.read_csv(name)
for name in file_after:
    dat_after = pd.read_csv(name)

time_expert = dat_expert['time']
x_expert = dat_expert['x']
y_expert = dat_expert['y']
z_expert = dat_expert['z']
roll_expert = dat_expert['roll']
pitch_expert = dat_expert['pitch']
yaw_expert = dat_expert['yaw']

time_before = dat_before['time']
x_before = dat_before['x']
y_before = dat_before['y']
z_before = dat_before['z']
roll_before = dat_before['roll']
pitch_before = dat_before['pitch']
yaw_before = dat_before['yaw']

time_after = dat_after['time']
x_after = dat_after['x']
y_after = dat_after['y']
z_after = dat_after['z']
roll_after = dat_after['roll']
pitch_after = dat_after['pitch']
yaw_after = dat_after['yaw']

fig, axes = plt.subplots(3, 2)

# x
axes[0,0].plot(time_expert, x_expert, c='darkorange', label='expert')
axes[0,0].plot(time_before, x_before, c='dimgray', label='before')
axes[0,0].plot(time_after, x_after, c='gray', label='after')
# axes[0,0].plot(time_robot, x_diff, c='gray', label='diff')
axes[0,0].set_xlabel('time[s]')
axes[0,0].set_ylabel('x[m]')
axes[0,0].set_title('x')
axes[0,0].legend()

# y
axes[1,0].plot(time_expert, y_expert, c='darkorange', label='expert')
axes[1,0].plot(time_before, y_before, c='dimgray', label='before')
axes[1,0].plot(time_after, y_after, c='gray', label='after')
axes[1,0].set_xlabel('time[s]')
axes[1,0].set_ylabel('y[m]')
axes[1,0].set_title('y')
axes[1,0].legend()

# z
axes[2,0].plot(time_expert, z_expert, c='darkorange', label='expert')
axes[2,0].plot(time_before, z_before, c='dimgray', label='before')
axes[2,0].plot(time_after, z_after, c='gray', label='after')
axes[2,0].set_xlabel('time[s]')
axes[2,0].set_ylabel('z[m]')
axes[2,0].set_title('z')
axes[2,0].legend()

# roll
axes[0,1].plot(time_expert, roll_expert, c='darkorange', label='expert')
axes[0,1].plot(time_before, roll_before, c='dimgray', label='before')
axes[0,1].plot(time_after, roll_after, c='gray', label='after')
axes[0,1].set_xlabel('time[s]')
axes[0,1].set_ylabel('roll[°]')
axes[0,1].set_title('roll')
axes[0,1].legend()

# pitch
axes[1,1].plot(time_expert, pitch_expert, c='darkorange', label='expert')
axes[1,1].plot(time_before, pitch_before, c='dimgray', label='before')
axes[1,1].plot(time_after, pitch_after, c='gray', label='after')
axes[1,1].set_xlabel('time[s]')
axes[1,1].set_ylabel('pitch[°]')
axes[1,1].set_title('pitch')
axes[1,1].legend()

# yaw
axes[2,1].plot(time_expert, yaw_expert, c='darkorange', label='expert')
axes[2,1].plot(time_before, yaw_before, c='dimgray', label='before')
axes[2,1].plot(time_after, yaw_after, c='gray', label='after')
axes[2,1].set_xlabel('time[s]')
axes[2,1].set_ylabel('yaw[°]')
axes[2,1].set_title('yaw')
axes[2,1].legend()

# ax.scatter(time, OP3_y, c='darkorange', label='3')
# ax.scatter(OP2_x, OP2_y, s=100, c="gray", alpha=1, linewidths=0, edgecolors="gray", label='2') 
# ax.scatter(OP3_x, OP3_y, s=60, c="darkorange", alpha=1, linewidths=0, edgecolors="darkorange", label='3') 
# plt.text(0.1, 0.1, f"r = {correlation:.3f}", ha="right", va="top", transform=plt.gca().transAxes)

# 軸のタイトルや凡例などの設定
# ax.set_title('3つの凡例を持つグラフ')
# ax.set_xlabel(xlabel)
# ax.set_ylabel(ylabel)
# plt.legend(loc='center left', bbox_to_anchor=(1., .5))
# plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1.03), ncol=3)
# plt.ylim(0,101)
# plt.xlim(0,1.01)

# グラフの表示
plt.show()