import graph
from matplotlib import pyplot as plt
import numpy as np
from FileIO import FileIO

# ----- csvからデータを取得 ----- #
fileIO = FileIO()
dat = fileIO.Read('graphtest.csv', ',')
ParticipantNum1 = [addr for addr in dat if 'participantNum1' in addr[0]]
ParticipantNum2 = [addr for addr in dat if 'participantNum2' in addr[0]]
ParticipantNum3 = [addr for addr in dat if 'participantNum3' in addr[0]]
data = [addr for addr in dat if 'data' in addr[0]][0][1]

# ----- dict型に変換 ----- #
ALLdata = dict(participantNum1 = ParticipantNum1, participantNum2 = ParticipantNum2, participantNum3 = ParticipantNum3,)
PN = dict(P1 = [], P2 = [], P3 = []) 

# ----- PNにリストとして入れ込む ----- #
for i in range(3):
    for j in range(int(data)):
        a = ALLdata['participantNum'+str(i+1)]
        PN['P'+str(i+1)].append(int(a[0][j+1]))

# ----- 測定したデータの平均値 ----- #
participantNum_1_average = np.average(np.array(PN['P1']))
participantNum_2_average = np.average(np.array(PN['P2']))
participantNum_3_average = np.average(np.array(PN['P3']))

# ----- データプロット ----- #
left = ['1', '2', '3']
height = np.array([participantNum_1_average, participantNum_2_average, participantNum_3_average])

plt.bar(left, height, width=0.5)
plt.xlabel('Participant Number')
plt.ylabel('Time[s]')
plt.show()