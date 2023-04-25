from matplotlib import legend_handler
import pandas as pd
import numpy as np
import csv
import glob
import tqdm
from FileIO.FileIO import FileIO
from v_a import VAJ
from Jerk import JRK

class Journey:
    def __init__(self) -> None:
        pass

    def get_data(self,data):
        self.tl = data['time']
        self.v_x = data['vx']
        self.v_y = data['vy']
        self.v_z = data['vz']

    def journey_from_vel(self, d):
        self.get_data(d)
        self.vel_sq_list = []
        for i in range(len(self.v_x)):
            self.vel_sq = np.sqrt(self.v_x[i]**2 + self.v_y[i]**2 + self.v_z[i]**2)
            self.vel_sq_list.append(self.vel_sq)
        self.journey = np.sum(self.vel_sq_list)
        return self.journey

Journey_condition1_group1_robot =[]
Journey_condition1_group2_robot =[]
Journey_condition1_group3_robot =[]
Journey_condition1_group4_robot =[]

Journey_condition2_group1_robot =[]
Journey_condition2_group2_robot =[]
Journey_condition2_group3_robot =[]
Journey_condition2_group4_robot =[]

Journey_condition3_group1_robot =[]
Journey_condition3_group2_robot =[]
Journey_condition3_group3_robot =[]
Journey_condition3_group4_robot =[]

Journey_condition1_group1_P1 = []
Journey_condition1_group2_P1 = []
Journey_condition1_group3_P1 = []
Journey_condition1_group4_P1 = []

Journey_condition2_group1_P1 = []
Journey_condition2_group1_P2 = []
Journey_condition2_group2_P1 = []
Journey_condition2_group2_P2 = []
Journey_condition2_group3_P1 = []
Journey_condition2_group3_P2 = []
Journey_condition2_group4_P1 = []
Journey_condition2_group4_P2 = []

Journey_condition3_group1_P1 = []
Journey_condition3_group1_P2 = []
Journey_condition3_group1_P3 = []
Journey_condition3_group2_P1 = []
Journey_condition3_group2_P2 = []
Journey_condition3_group2_P3 = []
Journey_condition3_group3_P1 = []
Journey_condition3_group3_P2 = []
Journey_condition3_group3_P3 = []
Journey_condition3_group4_P1 = []
Journey_condition3_group4_P2 = []
Journey_condition3_group4_P3 = []

if __name__ == '__main__':
    for i in range(3):
        condition = '条件' + str(i+1)
        for j in range(4):
            group = str(j+1) + '組目'
            for k in range(5):
                howmanytimes = str(k+1) + '回目'

                file_tasktime = '/Users/sanolab/this mac/大学/研究室/B4/卒論/卒論_data/data/tasktime.csv'
                with open(file_tasktime, 'r') as file:
                    reader = csv.reader(file)
                    tasktime_data = list(reader)
                tasktime = float(tasktime_data[6*i+j][k])+1

                for l in range(2):
                    arm = str(l+1)
                    file = glob.glob('/Users/sanolab/this mac/大学/研究室/B4/卒論/卒論_data/data/' + condition + '/' + group +'/本番/' + howmanytimes+ '/' +'Transform_Robot_' + arm + '*')
                    for name in file:
                        dat = pd.read_csv(name)
                    
                    vaj = VAJ(dat=dat, tasktime=tasktime)
                    data = vaj.calcurate_vel_acceleration_jerk()

                    journey_class = Journey()
                    journey = journey_class.journey_from_vel(data)

                    if i == 0 and j == 0:
                        Journey_condition1_group1_robot.append(journey)

                    if i == 0 and j == 1:
                        Journey_condition1_group2_robot.append(journey)

                    if i == 0 and j == 2:
                        Journey_condition1_group3_robot.append(journey)

                    if i == 0 and j == 3:
                        Journey_condition1_group4_robot.append(journey)


                    if i == 1 and j == 0:
                        Journey_condition2_group1_robot.append(journey)

                    if i == 1 and j == 1:
                        Journey_condition2_group2_robot.append(journey)

                    if i == 1 and j == 2:
                        Journey_condition2_group3_robot.append(journey)

                    if i == 1 and j == 3:
                        Journey_condition2_group4_robot.append(journey)


                    if i == 2 and j == 0:
                        Journey_condition3_group1_robot.append(journey)

                    if i == 2 and j == 1:
                        Journey_condition3_group2_robot.append(journey)

                    if i == 2 and j == 2:
                        Journey_condition3_group3_robot.append(journey)

                    if i == 2 and j == 3:
                        Journey_condition3_group4_robot.append(journey)


                for m in range(6):
                    num = str(m+1)
                    file = glob.glob('/Users/sanolab/this mac/大学/研究室/B4/卒論/卒論_data/data/' + condition + '/' + group +'/本番/' + howmanytimes+ '/' +'Transform_Participant_' + num + '*')
                    for name in file:
                        dat = pd.read_csv(name)
                    
                    vaj = VAJ(dat=dat, tasktime=tasktime)
                    data = vaj.calcurate_vel_acceleration_jerk()

                    journey_class = Journey()
                    journey = journey_class.journey_from_vel(data)

                    if i == 0 and j == 0 and (m == 0 or m == 1) :
                        Journey_condition1_group1_P1.append(journey)
                        
                    if i == 0 and j == 1 and (m == 0 or m == 1) :
                        Journey_condition1_group2_P1.append(journey)

                    if i == 0 and j == 2 and (m == 0 or m == 1) :
                        Journey_condition1_group3_P1.append(journey)

                    if i == 0 and j == 3 and (m == 0 or m == 1) :
                        Journey_condition1_group4_P1.append(journey)


                    if i == 1 and j == 0 and (m == 0 or m == 1) :
                        Journey_condition2_group1_P1.append(journey)
                        
                    if i == 1 and j == 1 and (m == 0 or m == 1) :
                        Journey_condition2_group2_P1.append(journey)

                    if i == 1 and j == 2 and (m == 0 or m == 1) :
                        Journey_condition2_group3_P1.append(journey)

                    if i == 1 and j == 3 and (m == 0 or m == 1) :
                        Journey_condition2_group4_P1.append(journey)                        

                    if i == 1 and j == 0 and (m == 2 or m == 3) :
                        Journey_condition2_group1_P2.append(journey)
                        
                    if i == 1 and j == 1 and (m == 2 or m == 3) :
                        Journey_condition2_group2_P2.append(journey)

                    if i == 1 and j == 2 and (m == 2 or m == 3) :
                        Journey_condition2_group3_P2.append(journey)

                    if i == 1 and j == 3 and (m == 2 or m == 3) :
                        Journey_condition2_group4_P2.append(journey)
                        

                    if i == 2 and j == 0 and (m == 0 or m == 1) :
                        Journey_condition3_group1_P1.append(journey)
                        
                    if i == 2 and j == 1 and (m == 0 or m == 1) :
                        Journey_condition3_group2_P1.append(journey)

                    if i == 2 and j == 2 and (m == 0 or m == 1) :
                        Journey_condition3_group3_P1.append(journey)

                    if i == 2 and j == 3 and (m == 0 or m == 1) :
                        Journey_condition3_group4_P1.append(journey)                        

                    if i == 2 and j == 0 and (m == 2 or m == 3) :
                        Journey_condition3_group1_P2.append(journey)
                        
                    if i == 2 and j == 1 and (m == 2 or m == 3) :
                        Journey_condition3_group2_P2.append(journey)

                    if i == 2 and j == 2 and (m == 2 or m == 3) :
                        Journey_condition3_group3_P2.append(journey)

                    if i == 2 and j == 3 and (m == 2 or m == 3) :
                        Journey_condition3_group4_P2.append(journey)      

                    if i == 2 and j == 0 and (m == 4 or m == 5) :
                        Journey_condition3_group1_P3.append(journey)
                        
                    if i == 2 and j == 1 and (m == 4 or m == 5) :
                        Journey_condition3_group2_P3.append(journey)

                    if i == 2 and j == 2 and (m == 4 or m == 5) :
                        Journey_condition3_group3_P3.append(journey)

                    if i == 2 and j == 3 and (m == 4 or m == 5) :
                        Journey_condition3_group4_P3.append(journey)                             


Journey_condition1_group1_robot = np.sum(Journey_condition1_group1_robot)
Journey_condition1_group2_robot = np.sum(Journey_condition1_group2_robot)
Journey_condition1_group3_robot = np.sum(Journey_condition1_group3_robot)
Journey_condition1_group4_robot = np.sum(Journey_condition1_group4_robot)

Journey_condition2_group1_robot = np.sum(Journey_condition2_group1_robot)
Journey_condition2_group2_robot = np.sum(Journey_condition2_group2_robot)
Journey_condition2_group3_robot = np.sum(Journey_condition2_group3_robot)
Journey_condition2_group4_robot = np.sum(Journey_condition2_group4_robot)

Journey_condition3_group1_robot = np.sum(Journey_condition3_group1_robot)
Journey_condition3_group2_robot = np.sum(Journey_condition3_group2_robot)
Journey_condition3_group3_robot = np.sum(Journey_condition3_group3_robot)
Journey_condition3_group4_robot = np.sum(Journey_condition3_group4_robot)


Journey_condition1_group1_P1 = np.sum(Journey_condition1_group1_P1)
Journey_condition1_group2_P1 = np.sum(Journey_condition1_group2_P1)
Journey_condition1_group3_P1 = np.sum(Journey_condition1_group3_P1)
Journey_condition1_group4_P1 = np.sum(Journey_condition1_group4_P1)

Journey_condition2_group1_P1 = np.sum(Journey_condition2_group1_P1)
Journey_condition2_group2_P1 = np.sum(Journey_condition2_group2_P1)
Journey_condition2_group3_P1 = np.sum(Journey_condition2_group3_P1)
Journey_condition2_group4_P1 = np.sum(Journey_condition2_group4_P1)
Journey_condition2_group1_P2 = np.sum(Journey_condition2_group1_P2)
Journey_condition2_group2_P2 = np.sum(Journey_condition2_group2_P2)
Journey_condition2_group3_P2 = np.sum(Journey_condition2_group3_P2)
Journey_condition2_group4_P2 = np.sum(Journey_condition2_group4_P2)

Journey_condition3_group1_P1 = np.sum(Journey_condition3_group1_P1)
Journey_condition3_group2_P1 = np.sum(Journey_condition3_group2_P1)
Journey_condition3_group3_P1 = np.sum(Journey_condition3_group3_P1)
Journey_condition3_group4_P1 = np.sum(Journey_condition3_group4_P1)
Journey_condition3_group1_P2 = np.sum(Journey_condition3_group1_P2)
Journey_condition3_group2_P2 = np.sum(Journey_condition3_group2_P2)
Journey_condition3_group3_P2 = np.sum(Journey_condition3_group3_P2)
Journey_condition3_group4_P2 = np.sum(Journey_condition3_group4_P2)
Journey_condition3_group1_P3 = np.sum(Journey_condition3_group1_P3)
Journey_condition3_group2_P3 = np.sum(Journey_condition3_group2_P3)
Journey_condition3_group3_P3 = np.sum(Journey_condition3_group3_P3)
Journey_condition3_group4_P3 = np.sum(Journey_condition3_group4_P3)

# OP1 = [Journey_condition1_group1_P1/Journey_condition1_group1_robot,
#        Journey_condition1_group2_P1/Journey_condition1_group2_robot,
#        Journey_condition1_group3_P1/Journey_condition1_group3_robot,
#        Journey_condition1_group4_P1/Journey_condition1_group4_robot]

# OP2 = [Journey_condition2_group1_P1*0.5/Journey_condition2_group1_robot, Journey_condition2_group1_P2*0.5/Journey_condition2_group1_robot,
#        Journey_condition2_group2_P1*0.5/Journey_condition2_group2_robot, Journey_condition2_group2_P2*0.5/Journey_condition2_group2_robot,
#        Journey_condition2_group3_P1*0.5/Journey_condition2_group3_robot, Journey_condition2_group3_P2*0.5/Journey_condition2_group3_robot,
#        Journey_condition2_group4_P1*0.5/Journey_condition2_group4_robot, Journey_condition2_group4_P2*0.5/Journey_condition2_group4_robot]

# OP3 = [Journey_condition3_group1_P1*0.33/Journey_condition3_group1_robot, Journey_condition3_group1_P2*0.33/Journey_condition3_group1_robot, Journey_condition3_group1_P3*0.33/Journey_condition3_group1_robot,
#        Journey_condition3_group2_P1*0.33/Journey_condition3_group2_robot, Journey_condition3_group2_P2*0.33/Journey_condition3_group2_robot, Journey_condition3_group2_P3*0.33/Journey_condition3_group2_robot,
#        Journey_condition3_group3_P1*0.33/Journey_condition3_group3_robot, Journey_condition3_group3_P2*0.33/Journey_condition3_group3_robot, Journey_condition3_group3_P3*0.33/Journey_condition3_group3_robot,
#        Journey_condition3_group4_P1*0.33/Journey_condition3_group4_robot, Journey_condition3_group4_P2*0.33/Journey_condition3_group4_robot, Journey_condition3_group4_P3*0.33/Journey_condition3_group4_robot]

OP1 = [Journey_condition1_group1_P1/Journey_condition1_group1_P1,
       Journey_condition1_group2_P1/Journey_condition1_group2_P1,
       Journey_condition1_group3_P1/Journey_condition1_group3_P1,
       Journey_condition1_group4_P1/Journey_condition1_group4_P1]

OP2 = [Journey_condition2_group1_P1/(Journey_condition2_group1_P1+Journey_condition2_group1_P2), Journey_condition2_group1_P2/(Journey_condition2_group1_P1+Journey_condition2_group1_P2),
       Journey_condition2_group2_P1/(Journey_condition2_group2_P1+Journey_condition2_group2_P2), Journey_condition2_group2_P2/(Journey_condition2_group2_P1+Journey_condition2_group2_P2),
       Journey_condition2_group3_P1/(Journey_condition2_group3_P1+Journey_condition2_group3_P2), Journey_condition2_group3_P2/(Journey_condition2_group3_P1+Journey_condition2_group3_P2),
       Journey_condition2_group4_P1/(Journey_condition2_group4_P1+Journey_condition2_group4_P2), Journey_condition2_group4_P2/(Journey_condition2_group4_P1+Journey_condition2_group4_P2)]

OP3 = [Journey_condition3_group1_P1/(Journey_condition3_group1_P1+Journey_condition3_group1_P2+Journey_condition3_group1_P3), Journey_condition3_group1_P2/(Journey_condition3_group1_P1+Journey_condition3_group1_P2+Journey_condition3_group1_P3), Journey_condition3_group1_P3/(Journey_condition3_group1_P1+Journey_condition3_group1_P2+Journey_condition3_group1_P3),
       Journey_condition3_group2_P1/(Journey_condition3_group2_P1+Journey_condition3_group2_P2+Journey_condition3_group2_P3), Journey_condition3_group2_P2/(Journey_condition3_group2_P1+Journey_condition3_group2_P2+Journey_condition3_group2_P3), Journey_condition3_group2_P3/(Journey_condition3_group2_P1+Journey_condition3_group2_P2+Journey_condition3_group2_P3),
       Journey_condition3_group3_P1/(Journey_condition3_group3_P1+Journey_condition3_group3_P2+Journey_condition3_group3_P3), Journey_condition3_group3_P2/(Journey_condition3_group3_P1+Journey_condition3_group3_P2+Journey_condition3_group3_P3), Journey_condition3_group3_P3/(Journey_condition3_group3_P1+Journey_condition3_group3_P2+Journey_condition3_group3_P3),
       Journey_condition3_group4_P1/(Journey_condition3_group4_P1+Journey_condition3_group4_P2+Journey_condition3_group4_P3), Journey_condition3_group4_P2/(Journey_condition3_group4_P1+Journey_condition3_group4_P2+Journey_condition3_group4_P3), Journey_condition3_group4_P3/(Journey_condition3_group4_P1+Journey_condition3_group4_P2+Journey_condition3_group4_P3)]

print(OP1)
print(OP2)
print(OP3)