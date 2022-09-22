from operator import length_hint
from statistics import stdev
import graph
from matplotlib import pyplot as plt
import numpy as np
from FileIO import FileIO

# ----- csvからデータを取得 ----- #
fileIO = FileIO()
dat = fileIO.Read('SI2022.csv', ',')
# dat = fileIO.Read('SI2022所有感.csv', ',')
# dat = fileIO.Read('SI2022操作感.csv', ',')
# dat = fileIO.Read('SI2022連帯感.csv', ',')
# dat = fileIO.Read('SI2022tasktime.csv', ',')
# dat = fileIO.Read('SI2022NASATLX.csv', ',')
OP1 = [addr for addr in dat if 'OP1' in addr[0]]
OP2 = [addr for addr in dat if 'OP2_1' in addr[0]]
OP3 = [addr for addr in dat if 'OP2_2' in addr[0]]
OP4 = [addr for addr in dat if 'OP3' in addr[0]]

# ----- dict型に変換 ----- #
# ALLdata = dict(OP1 = OP1, OP2 = OP2, OP3 = OP3, OP4 = OP4,)
# OP = dict(OP1 = [], OP2 = [], OP3 = [], OP4 = [])

# ----- 不要部分を除く ----- #
OP1[0].remove('OP1')
OP2[0].remove('OP2_1')
OP3[0].remove('OP2_2')
OP4[0].remove('OP3')

# ----- list型に変換 ----- #
OP1str = OP1[0]
OP2str = OP2[0]
OP3str = OP3[0]
OP4str = OP4[0]
OP1list = list(map(int,OP1str))
OP2list = list(map(int,OP2str))
OP3list = list(map(int,OP3str))
OP4list = list(map(int,OP4str))

# # ----- OPにリストとして入れ込む ----- #
# for i in range(4):
#     for j in range(len('OP'+str(i+1)+[0])):
#         a = ALLdata['OP'+str(i+1)]
#         OP['OP'+str(i+1)].append(int(a[0][j+1]))

# ----- 測定したデータの平均値 ----- #
average_OP1 = np.average(np.array(OP1list))
average_OP2_1 = np.average(np.array(OP2list))
average_OP2_2 = np.average(np.array(OP3list))
average_OP3 = np.average(np.array(OP4list))

# ----- 標準偏差 ----- #
y_err = [stdev(OP1list), stdev(OP2list), stdev(OP3list), stdev(OP4list)]

# ----- データプロット ----- #
left = ['1', '2人(別々)','2人(融合)', '3']
height = np.array([average_OP1, average_OP2_1, average_OP2_2, average_OP3])
plt.bar(left, height, yerr = y_err, width=0.5, capsize=5)
plt.xlabel('Condition')
plt.ylabel('Rating Score')
plt.show()