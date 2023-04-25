from re import S
from matplotlib import legend_handler
import pandas as pd
import numpy as np
import csv
import glob
import tqdm
from FileIO.FileIO import FileIO
from v_a import VAJ
from Jerk import JRK

class INNER:
    def __init__(self,dat_1,dat_2,tasktime) -> None:
        vaj_1 = VAJ(dat=dat_1, tasktime=tasktime)
        vaj_2 = VAJ(dat=dat_1, tasktime=tasktime)
        dat_1 = vaj_1.calcurate_vel_acceleration_jerk()
        dat_2 = vaj_2.calcurate_vel_acceleration_jerk()
        self.time_all = dat_1['time']
        self.vx_1_all = dat_1['vx']
        self.vy_1_all = dat_1['vy']
        self.vz_1_all = dat_1['vz']
        self.vx_2_all = dat_2['vx']
        self.vy_2_all = dat_2['vy']
        self.vz_2_all = dat_2['vz']
        self.x_1_all = dat_1['x']
        self.y_1_all = dat_1['y']
        self.z_1_all = dat_1['z']
        self.x_2_all = dat_2['x']
        self.y_2_all = dat_2['y']
        self.z_2_all = dat_2['z']

        
        self.tasktime = tasktime

    def time2tasktime(self, time, tasktime):
        time_all_in_tasktime =[]
        for i in range(len(time)):
            if tasktime > time[i]:
                time_all_in_tasktime.append(time[i])      
        return time_all_in_tasktime

    def innerproduct(self):
        time_all_in_tasktime = self.time2tasktime(self.time_all, self.tasktime)
        self.cos_list = []
        for i in range(len(time_all_in_tasktime)-3):
            self.cos_top = self.vx_1_all[i]*self.vx_2_all[i] + self.vy_1_all[i]*self.vy_2_all[i] + self.vz_1_all[i]*self.vz_2_all[i]
            self.cos_bottom = np.sqrt(self.vx_1_all[i]**2 + self.vy_1_all[i]**2 + self.vz_1_all[i]**2) * np.sqrt(self.vx_2_all[i]**2 + self.vy_2_all[i]**2 + self.vz_2_all[i]**2)
            if i < len(time_all_in_tasktime)-1:
                distance_1_x = self.x_1_all[i+1] - self.x_1_all[i]
                distance_1_y = self.y_1_all[i+1] - self.y_1_all[i]
                distance_1_z = self.z_1_all[i+1] - self.z_1_all[i]
                distance_2_x = self.x_2_all[i+1] - self.x_2_all[i]
                distance_2_y = self.y_2_all[i+1] - self.y_2_all[i]
                distance_2_z = self.z_2_all[i+1] - self.z_2_all[i]
                distance_1 = np.sqrt(distance_1_x**2 + distance_1_y**2 + distance_1_z**2)
                distance_2 = np.sqrt(distance_2_x**2 + distance_2_y**2 + distance_2_z**2)

                if distance_1 < 0.00000005 or distance_2 < 0.00000005 or np.sqrt(self.vx_1_all[i]**2 + self.vy_1_all[i]**2 + self.vz_1_all[i]**2) == 0 or np.sqrt(self.vx_2_all[i]**2 + self.vy_2_all[i]**2 + self.vz_2_all[i]**2) == 0:
                    pass
                else:
                    self.cos = self.cos_top/self.cos_bottom
                    self.cos_list.append(self.cos)
        return self.cos_list


dat  = {}
cos_condition2_list = []
cos_condition3_list = []
cos_1_list = []
cos_2_list = []
cos_3_list = []

if __name__ == '__main__':
    for i in range(2):
        condition = '条件' + str(i+2)
        for j in range(4):
            group = str(j+1) + '組目'
            for k in range(5):
                howmanytimes = str(k+1) + '回目'

                file_tasktime = '/Users/sanolab/this mac/大学/研究室/B4/卒論/卒論_data/data/tasktime.csv'
                with open(file_tasktime, 'r') as file:
                    reader = csv.reader(file)
                    tasktime_data = list(reader)
                tasktime = float(tasktime_data[6*i+j][k])+1

                if i == 0:
                    for m in range(4):
                        num = str(m+1)
                        file = glob.glob('/Users/sanolab/this mac/大学/研究室/B4/卒論/卒論_data/data/' + condition + '/' + group +'/本番/' + howmanytimes+ '/' +'Transform_Participant_' + num + '*')
                        file = file[0]
                        dat[str(num)] = pd.read_csv(file)

                    inner_1 = INNER(dat_1=dat['1'],dat_2=dat['3'],tasktime=tasktime)
                    cos_list_left_12 = inner_1.innerproduct()
                    cos_left = np.average(cos_list_left_12)

                    inner_2 = INNER(dat_1=dat['2'],dat_2=dat['4'],tasktime=tasktime)
                    cos_list_right_12 = inner_2.innerproduct()
                    cos_right = np.average(cos_list_right_12)

                    cos = (cos_left + cos_right)/2
                    cos_condition2_list.append(cos)

                if i == 1:
                    for m in range(6):
                        num = str(m+1)
                        file = glob.glob('/Users/sanolab/this mac/大学/研究室/B4/卒論/卒論_data/data/' + condition + '/' + group +'/本番/' + howmanytimes+ '/' +'Transform_Participant_' + num + '*')
                        file = file[0]
                        dat[str(num)] = pd.read_csv(file)

                    inner_1 = INNER(dat_1=dat['1'],dat_2=dat['3'],tasktime=tasktime)
                    inner_2 = INNER(dat_1=dat['1'],dat_2=dat['5'],tasktime=tasktime)
                    inner_3 = INNER(dat_1=dat['3'],dat_2=dat['5'],tasktime=tasktime)
                    cos_list_left_12 = inner_1.innerproduct()
                    cos_list_left_13 = inner_2.innerproduct()
                    cos_list_left_23 = inner_3.innerproduct()

                    inner_4 = INNER(dat_1=dat['2'],dat_2=dat['4'],tasktime=tasktime)
                    inner_5 = INNER(dat_1=dat['2'],dat_2=dat['6'],tasktime=tasktime)
                    inner_6 = INNER(dat_1=dat['4'],dat_2=dat['6'],tasktime=tasktime)
                    cos_list_right_12 = inner_4.innerproduct()
                    cos_list_right_13 = inner_5.innerproduct()
                    cos_list_right_23 = inner_6.innerproduct()

                    # cos_list_left = [(x + y + z) / 3 for x, y, z in zip(cos_list_left_12, cos_list_left_13, cos_list_left_23)]
                    # cos_list_right = [(x + y + z) / 3 for x, y, z in zip(cos_list_right_12, cos_list_right_13, cos_list_right_23)]
                    # cos_left = np.average(cos_list_left)
                    # cos_right = np.average(cos_list_right)
                    # cos = (cos_left + cos_right)/2
                    # cos_condition3_list.append(cos)

                    cos_list_left_1 = [(x + y) / 2 for x, y in zip(cos_list_left_12, cos_list_left_13)]
                    cos_list_left_2 = [(x + y) / 2 for x, y in zip(cos_list_left_12, cos_list_left_23)]
                    cos_list_left_3 = [(x + y) / 2 for x, y in zip(cos_list_left_13, cos_list_left_23)]
                    cos_list_right_1 = [(x + y) / 2 for x, y in zip(cos_list_right_12, cos_list_right_13)]
                    cos_list_right_2 = [(x + y) / 2 for x, y in zip(cos_list_right_12, cos_list_right_23)]
                    cos_list_right_3 = [(x + y) / 2 for x, y in zip(cos_list_right_13, cos_list_right_23)]
                    cos_left_1 = np.average(cos_list_left_1)
                    cos_left_2 = np.average(cos_list_left_2)
                    cos_left_3 = np.average(cos_list_left_3)
                    cos_right_1 = np.average(cos_list_right_1)
                    cos_right_2 = np.average(cos_list_right_2)
                    cos_right_3 = np.average(cos_list_right_3)
                    cos_1 = (cos_left_1 + cos_right_1)/2
                    cos_2 = (cos_left_2 + cos_right_2)/2
                    cos_3 = (cos_left_3 + cos_right_3)/2
                    cos_1_list.append(cos_1)
                    cos_2_list.append(cos_2)
                    cos_3_list.append(cos_3)

# cos_condition3_list[15] = 0.5888016335090112
# cos_condition2_average_list = []
# cos_condition3_average_list = []

# for i in range(4):
#     i = 5*i
#     average = sum(cos_condition2_list[i:i+5])/5
#     cos_condition2_average_list.append(average)
# for i in range(4):
#     i = 5*i
#     average = sum(cos_condition3_list[i:i+5])/5
#     cos_condition3_average_list.append(average)

# print(cos_condition2_list)
# print(cos_condition2_average_list)
# print(cos_condition3_list)
# print(cos_condition3_average_list)


# cos_condition3_list[15] = 0.5888016335090112
cos_1_average_list = []
cos_2_average_list = []
cos_3_average_list = []

for i in range(4):
    i = 5*i
    if i == 15:
        average = sum(cos_1_list[i+1:i+5])/5
    else:
        average = sum(cos_1_list[i:i+5])/5
    cos_1_average_list.append(average)

for i in range(4):
    i = 5*i
    if i == 15:
        average = sum(cos_2_list[i+1:i+5])/5
    else:
        average = sum(cos_2_list[i:i+5])/5
    cos_2_average_list.append(average)

for i in range(4):
    i = 5*i
    if i == 15:
        average = sum(cos_3_list[i+1:i+5])/5
    else:
        average = sum(cos_3_list[i:i+5])/5
    cos_3_average_list.append(average)


print(cos_1_list)
print(cos_2_list)
print(cos_3_list)
print(cos_1_average_list)
print(cos_2_average_list)
print(cos_3_average_list)
