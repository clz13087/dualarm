from operator import length_hint
from statistics import stdev
import graph
from matplotlib import pyplot as plt
import numpy as np
from FileIO.FileIO import FileIO
import seaborn as sns

# ----- csvからデータを取得 ----- #
fileIO = FileIO()
dat = fileIO.Read('senseofagency_点プロット.csv', ',')
# dat = fileIO.Read('senseofownership_点プロット.csv', ',')

ylabel = [addr for addr in dat if 'ylabel' in addr[0]][0][1]
OP1 = [addr for addr in dat if 'OP1' in addr[0]]
OP2 = [addr for addr in dat if 'OP2' in addr[0]]
OP3 = [addr for addr in dat if 'OP3' in addr[0]]

OP1[0].remove('OP1')
OP2[0].remove('OP2')
OP3[0].remove('OP3')

# ----- strをlistに変換 ----- #
OP1list = list(map(float,OP1[0]))
OP2list = list(map(float,OP2[0]))
OP3list = list(map(float,OP3[0]))

# # ----- 箱ひげ図 ----- #
# fig, ax = plt.subplots()
# left = ['1', '2(separate)', '2(integration)', '3(center)', '3(side)']
# height = [OP1list, OP2list, OP3list, OP4list, OP5list] 

# bp=ax.boxplot(height,
#               labels = left,  #条件
#               vert=True,  # 縦向きにする
#               patch_artist=True,  # 細かい設定をできるようにする
#               widths=0.7,  # boxの幅の設定
#               medianprops=dict(color='black', linewidth=1),  # 中央値の線の設定
#               whiskerprops=dict(color='black', linewidth=1),  # ヒゲの線の設定
#               capprops=dict(color='black', linewidth=1),  # ヒゲの先端の線の設定
#               flierprops=dict(markeredgecolor='black', markeredgewidth=1)  # 外れ値の設定
#               )

height1 = [OP1list[0],OP2list[0],OP3list[0]]
height2 = [OP1list[1],OP2list[1],OP3list[1]]
height3 = [OP1list[2],OP2list[2],OP3list[2]]
left = ['1', '2', '3']

# ----- 縦横ラベル ----- #
fig, ax = plt.subplots()
ax.scatter(left, height1, color = "k")
ax.scatter(left, height2, color = "k")
ax.scatter(left, height3, color = "k")
plt.xlabel('Condition')
plt.ylabel(ylabel)
# plt.setp(ax.get_xticklabels(), rotation=0) #labelsが重なった時角度変更
# sns.swarmplot(y = height, color="r")
plt.ylim(0,100)
plt.show()