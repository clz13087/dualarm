import pandas as pd
import glob
from matplotlib import pyplot as plt
import numpy as np

class VAJ:
    def __init__(self,dat) -> None:
        self.time_all = dat['time']
        self.x_all = dat['x']
        self.y_all = dat['y']
        self.z_all = dat['z']

    def calcurate_vel_acceleration_jerk(self):
        time_all_in_tasktime = self.time_all
        self.data = {}
        self.vx = []
        self.vy = []
        self.vz = []
        self.ax = []
        self.ay = []
        self.az = []
        self.jx = []
        self.jy = []
        self.jz = []

        for i in range(len(time_all_in_tasktime)-3):
            dt1 = time_all_in_tasktime[i+1] - time_all_in_tasktime[i]
            self.vx.append((self.x_all[i+1] - self.x_all[i])/dt1)
            self.vy.append((self.y_all[i+1] - self.y_all[i])/dt1)
            self.vz.append((self.z_all[i+1] - self.z_all[i])/dt1)

            dt2 = time_all_in_tasktime[i+2] - time_all_in_tasktime[i+1]
            self.vx.append((self.x_all[i+2] - self.x_all[i+1])/dt2)
            self.vy.append((self.y_all[i+2] - self.y_all[i+1])/dt2)
            self.vz.append((self.z_all[i+2] - self.z_all[i+1])/dt2)

            dt3 = time_all_in_tasktime[i+3] - time_all_in_tasktime[i+2]
            self.vx.append((self.x_all[i+3] - self.x_all[i+2])/dt3)
            self.vy.append((self.y_all[i+3] - self.y_all[i+2])/dt3)
            self.vz.append((self.z_all[i+3] - self.z_all[i+2])/dt3)

            self.ax.append((self.vx[i+1] - self.vx[i])/dt1)
            self.ay.append((self.vy[i+1] - self.vy[i])/dt1)
            self.az.append((self.vz[i+1] - self.vz[i])/dt1)

            self.ax.append((self.vx[i+2] - self.vx[i+1])/dt2)
            self.ay.append((self.vy[i+2] - self.vy[i+1])/dt2)
            self.az.append((self.vz[i+2] - self.vz[i+1])/dt2)

            self.jx.append((self.ax[i+1] - self.ax[i])/dt1)
            self.jy.append((self.ay[i+1] - self.ay[i])/dt1)
            self.jz.append((self.az[i+1] - self.az[i])/dt1)

            # ----- jerk求めるために先に計算した，v2個とa1個を削除 ----- #
            del self.vx[-2:]
            del self.vy[-2:]
            del self.vz[-2:]
            del self.ax[-1:]
            del self.ay[-1:]
            del self.az[-1:]

        self.data = dict(time=time_all_in_tasktime, x=self.x_all, y=self.y_all, z=self.z_all, vx=self.vx , vy=self.vy, vz=self.vz, jx=self.jx, jy=self.jy, jz=self.jz)
        return self.data

file_user = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/check_accuracy/12回目/Transform_Participant_2*')
file_robot = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/check_accuracy/12回目/OtherRigidBody_2*')
for name in file_user:
    dat_user = pd.read_csv(name)
for name in file_robot:
    dat_robot = pd.read_csv(name)

vaj_class_user = VAJ(dat_user)
vaj_user = vaj_class_user.calcurate_vel_acceleration_jerk()
vaj_class_robot = VAJ(dat_robot)
vaj_robot = vaj_class_robot.calcurate_vel_acceleration_jerk()

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

pos_diff = np.sqrt((x_user - x_robot)**2 + (y_user - y_robot)**2 + (z_user - z_robot)**2)
vel = np.sqrt(np.array(vaj_user['vx'])**2 + np.array(vaj_user['vy'])**2 + np.array(vaj_user['vz'])**2)
new_pos_diff = pos_diff[:-3]

plt.subplots()

# x
plt.scatter(vel, new_pos_diff, c='darkorange', label='user')
# axes[0,0].plot(time_robot, x_diff, c='gray', label='diff')
plt.xlabel('velocity')
plt.ylabel('diff')
# axes[0,0].set_title('x')
plt.legend()

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
# plt.ylim(0,0.015)
# plt.xlim(0,0.25)

# グラフの表示
plt.show()