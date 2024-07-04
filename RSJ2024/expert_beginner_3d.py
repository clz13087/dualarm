from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob

file_expert = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/RSJ2024/experiment/expertdata/1/Transform_Participant_2*')
file_before = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/RSJ2024/experiment/beginnerdata/konishi/before/1/Transform_Participant_2*')
file_after = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/RSJ2024/experiment/beginnerdata/konishi/after/1/Transform_Participant_2*')
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

fig = plt.figure()
axes = fig.add_subplot(111,projection='3d')
# ax.set_aspect('equal')

axes.scatter(x_expert,y_expert,z_expert,c='darkorange', label='expert')
axes.scatter(x_before,y_before,z_before,c='dimgray', label='before')
axes.scatter(x_after,y_after,z_after,c='red', label='after')
axes.legend()
plt.show()
