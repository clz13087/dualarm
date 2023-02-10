from matplotlib import legend_handler
import pandas as pd
import numpy as np
import csv
import glob
import tqdm
from FileIO.FileIO import FileIO
from Jerk import JRK

class VAJ:
    def __init__(self,dat,tasktime) -> None:
        self.time_all = dat['time']
        self.x_all = dat['x']
        self.y_all = dat['y']
        self.z_all = dat['z']
        self.tasktime = tasktime

    def time2tasktime(self, time, tasktime):
        time_all_in_tasktime =[]
        for i in range(len(time)):
            if tasktime > time[i]:
                time_all_in_tasktime.append(time[i])      
        return time_all_in_tasktime

    def calcurate_vel_acceleration_jerk(self):
        time_all_in_tasktime = self.time2tasktime(self.time_all, self.tasktime)
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

        self.data = dict(time=time_all_in_tasktime, vx=self.vx , vy=self.vy, vz=self.vz, jx=self.jx, jy=self.jy, jz=self.jz)
        return self.data

JerkIndex_list_condition_1_left = []
JerkIndex_list_condition_2_left = []
JerkIndex_list_condition_3_left = []
JerkIndex_list_condition_1_right = []
JerkIndex_list_condition_2_right = []
JerkIndex_list_condition_3_right = []

if __name__ == '__main__':
    for i in range(3):
        condition = '条件' + str(i+1)
        for j in range(4):
            group = str(j+1) + '組目'
            for k in range(5):
                howmanytimes = str(k+1) + '回目'
                for l in range(2):
                    arm = str(l+1)
                    file = glob.glob('/Users/sanolab/this mac/大学/研究室/B4/卒論/卒論_data/data/' + condition + '/' + group +'/本番/' + howmanytimes+ '/' +'Transform_Robot_' + arm + '*')
                    for name in file:
                        dat = pd.read_csv(name)
                    
                    file_tasktime = '/Users/sanolab/this mac/大学/研究室/B4/卒論/卒論_data/data/tasktime.csv'
                    with open(file_tasktime, 'r') as file:
                        reader = csv.reader(file)
                        tasktime_data = list(reader)
                    tasktime = float(tasktime_data[6*i+j][k])+1
                    
                    vaj = VAJ(dat=dat, tasktime=tasktime)
                    data = vaj.calcurate_vel_acceleration_jerk()

                    jerk = JRK()
                    jerkindex = jerk.JRK_C(data)
                    
                    # ----- 全てを順に出力 ----- #
                    # print(condition + '_' + group + '_' + howmanytimes + '_' + arm + '_' +'jerkindex: ', format(jerkindex,'.3E'))

                    # ----- 条件と左右で分けて，一個の ----- #
                    if i == 0 and l == 0:
                        JerkIndex_list_condition_1_left.append(format(jerkindex,'.3E'))
                    if i == 1 and l == 0:
                        JerkIndex_list_condition_2_left.append(format(jerkindex,'.3E'))
                    if i == 2 and l == 0:
                        JerkIndex_list_condition_3_left.append(format(jerkindex,'.3E'))
                    if i == 0 and l == 1:
                        JerkIndex_list_condition_1_right.append(format(jerkindex,'.3E'))
                    if i == 1 and l == 1:
                        JerkIndex_list_condition_2_right.append(format(jerkindex,'.3E'))
                    if i == 2 and l == 1:
                        JerkIndex_list_condition_3_right.append(format(jerkindex,'.3E'))

    # ----- for left arm ----- # 
    JerkIndex_list_condition_1_left = list(map(float,JerkIndex_list_condition_1_left))
    JerkIndex_list_condition_2_left = list(map(float,JerkIndex_list_condition_2_left))
    JerkIndex_list_condition_3_left = list(map(float,JerkIndex_list_condition_3_left))

    # ----- for right arm ----- #
    JerkIndex_list_condition_1_right = list(map(float,JerkIndex_list_condition_1_right))
    JerkIndex_list_condition_2_right = list(map(float,JerkIndex_list_condition_2_right))
    JerkIndex_list_condition_3_right = list(map(float,JerkIndex_list_condition_3_right))

    # ----- for dual-arm ----- #
    JerkIndex_list_condition_1_dualarm = [(x + y) / 2 for x, y in zip(JerkIndex_list_condition_1_left, JerkIndex_list_condition_1_right)]
    JerkIndex_list_condition_2_dualarm = [(x + y) / 2 for x, y in zip(JerkIndex_list_condition_2_left, JerkIndex_list_condition_2_right)]
    JerkIndex_list_condition_3_dualarm = [(x + y) / 2 for x, y in zip(JerkIndex_list_condition_3_left, JerkIndex_list_condition_3_right)]