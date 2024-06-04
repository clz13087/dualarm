import pandas as pd
import glob
from matplotlib import pyplot as plt

file_user = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/check_accuracy/3回目/OtherRigidBody_1*')
file_robot = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/check_accuracy/3回目/OtherRigidBody_2*')
for name in file_user:
    dat_user = pd.read_csv(name)
for name in file_robot:
    dat_robot = pd.read_csv(name)

time_user = dat_user['time']
x_user = dat_user['x']
y_user = dat_user['y']
z_user = dat_user['z']
roll_user = dat_user['roll']
pitch_user = dat_user['pitch']
yaw_user = dat_user['yaw']

time_robot = dat_robot['time']
x_robot = dat_robot['x']
y_robot = dat_robot['y']
z_robot = dat_robot['z']
roll_robot = dat_robot['roll']
pitch_robot = dat_robot['pitch']
yaw_robot = dat_robot['yaw']

fig, axes = plt.subplots(2, 3)

# x
axes[0,0].plot(time_user, x_user, c='darkorange', label='user')
axes[0,0].plot(time_robot, x_robot, c='dimgray', label='robot')
axes[0,0].set_xlabel('time[s]')
axes[0,0].set_ylabel('x[m]')
axes[0,0].set_title('x')
axes[0,0].legend()

# y
axes[0,1].plot(time_user, y_user, c='darkorange', label='user')
axes[0,1].plot(time_robot, y_robot, c='dimgray', label='robot')
axes[0,1].set_xlabel('time[s]')
axes[0,1].set_ylabel('y[m]')
axes[0,1].set_title('y')
axes[0,1].legend()

# z
axes[0,2].plot(time_user, z_user, c='darkorange', label='user')
axes[0,2].plot(time_robot, z_robot, c='dimgray', label='robot')
axes[0,2].set_xlabel('time[s]')
axes[0,2].set_ylabel('z[m]')
axes[0,2].set_title('z')
axes[0,2].legend()

# roll
axes[1,0].plot(time_user, roll_user, c='darkorange', label='user')
axes[1,0].plot(time_robot, roll_robot, c='dimgray', label='robot')
axes[1,0].set_xlabel('time[s]')
axes[1,0].set_ylabel('roll[°]')
axes[1,0].set_title('roll')
axes[1,0].legend()

# pitch
axes[1,1].plot(time_user, pitch_user, c='darkorange', label='user')
axes[1,1].plot(time_robot, pitch_robot, c='dimgray', label='robot')
axes[1,1].set_xlabel('time[s]')
axes[1,1].set_ylabel('pitch[°]')
axes[1,1].set_title('pitch')
axes[1,1].legend()

# yaw
axes[1,2].plot(time_user, yaw_user, c='darkorange', label='user')
axes[1,2].plot(time_robot, yaw_robot, c='dimgray', label='robot')
axes[1,2].set_xlabel('time[s]')
axes[1,2].set_ylabel('yaw[°]')
axes[1,2].set_title('yaw')
axes[1,2].legend()

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