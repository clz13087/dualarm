import glob
import pandas as pd
from matplotlib import pyplot as plt

file_record = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/SI2024/tsugumidata/mocap/8/Transform_Participant_2*')
file_before = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/SI2024/yamashitadata/mocap/1/Transform_Participant_2*')
# file_before = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/SI2024/tsugumidata/mocap/1/Transform_Participant_1*')
file_after = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/SI2024/yamashitadata/mocap/10/Transform_Participant_2*')
# file_after = glob.glob('/Users/sanolab/this mac/大学/研究室/M2/SI2024/tsugumidata/mocap/4/Transform_Participant_1*')

for name in file_record:
    dat_record = pd.read_csv(name)
for name in file_before:
    dat_before = pd.read_csv(name)
for name in file_after:
    dat_after = pd.read_csv(name)

fig, axes = plt.subplots(3,2)

# x
axes[0,0].plot(dat_record["time"], dat_record["x"], c='dimgray', label='record')
axes[0,0].plot(dat_before["time"], dat_before["x"], c='darkorange', label='before')
axes[0,0].plot(dat_after["time"], dat_after["x"], c='orange', label='after')
axes[0,0].set_xlabel('time[s]')
axes[0,0].set_ylabel('x[m]')
axes[0,0].set_title('x')
axes[0,0].legend()

# y
axes[1,0].plot(dat_record["time"], dat_record["y"], c='dimgray', label='record')
axes[1,0].plot(dat_before["time"], dat_before["y"], c='darkorange', label='before')
axes[1,0].plot(dat_after["time"], dat_after["y"], c='orange', label='after')
axes[1,0].set_xlabel('time[s]')
axes[1,0].set_ylabel('y[m]')
axes[1,0].set_title('y')
axes[1,0].legend()

# z
axes[2,0].plot(dat_record["time"], dat_record["z"], c='dimgray', label='record')
axes[2,0].plot(dat_before["time"], dat_before["z"], c='darkorange', label='before')
axes[2,0].plot(dat_after["time"], dat_after["z"], c='orange', label='after')
axes[2,0].set_xlabel('time[s]')
axes[2,0].set_ylabel('z[m]')
axes[2,0].set_title('z')
axes[2,0].legend()

# axes[0,1].plot(dat_record["time"], dat_record["weightpos"], c='dimgray', label='record')
# axes[0,1].plot(dat_before["time"], dat_before["weightpos"], c='darkorange', label='before')
# axes[0,1].plot(dat_after["time"], dat_after["weightpos"], c='orange', label='after')
# axes[0,1].set_xlabel('time[s]')
# axes[0,1].set_ylabel('x[m]')
# axes[0,1].set_title('x')
# axes[0,1].legend()

plt.show()