from operator import length_hint
from statistics import stdev
import graph
from matplotlib import pyplot as plt
import numpy as np
from FileIO import FileIO

# ----- csvからデータを取得 ----- #
fileIO = FileIO()
# dat = fileIO.Read('SI2022主体感.csv', ',')
# dat = fileIO.Read('SI2022所有感.csv', ',')
# dat = fileIO.Read('SI2022操作性.csv', ',')
# dat = fileIO.Read('SI2022連帯感.csv', ',')
# dat = fileIO.Read('SI2022tasktime.csv', ',')
dat = fileIO.Read('SI2022NASATLX.csv', ',')

ylabel = [addr for addr in dat if 'ylabel' in addr[0]][0][1]
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
OP1list = list(map(float,OP1str))
OP2list = list(map(float,OP2str))
OP3list = list(map(float,OP3str))
OP4list = list(map(float,OP4str))

# # ----- 棒グラフ ----- #
# left = ['1', '2人(別々)','2人(融合)', '3']
# height = np.array([average_OP1, average_OP2_1, average_OP2_2, average_OP3])
# plt.bar(left, height, yerr = y_err, width=0.5, capsize=5, color = color)
# plt.xlabel('Condition')
# plt.ylabel(ylabel)
# # plt.ylim(1,7)
# plt.show()

# ----- 箱ひげ図 ----- #
fig, ax = plt.subplots()
left = ['1', '2(separate)','2(integration)', '3']
height = [OP1list, OP2list, OP3list, OP4list]

# ----- (操作性用) ----- #
# left = ['2(separate)','2(integration)', '3']
# height = [OP2list, OP3list, OP4list]

bp=ax.boxplot(height,
              labels = left,  #条件
              vert=True,  # 縦向きにする
              patch_artist=True,  # 細かい設定をできるようにする
              widths=0.7,  # boxの幅の設定
              medianprops=dict(color='black', linewidth=1),  # 中央値の線の設定
              whiskerprops=dict(color='black', linewidth=1),  # ヒゲの線の設定
              capprops=dict(color='black', linewidth=1),  # ヒゲの先端の線の設定
              flierprops=dict(markeredgecolor='black', markeredgewidth=1)  # 外れ値の設定
              )

# ----- boxの色のリスト ----- #
# colors = ['dodgerblue','steelblue','deepskyblue','mediumblue']
# colors = ['darkgray','steelblue','dodgerblue','deepskyblue']
colors = ['dimgray','gray','darkgray','lightgray']

# ----- (操作性用) ----- #
# colors = ['gray','darkgray','lightgray']

# ----- boxの色の設定 ----- #
for b, c in zip(bp['boxes'], colors):
    b.set(color='black', linewidth=1)  # boxの外枠の色
    b.set_facecolor(c) # boxの色

# ----- 縦横ラベル ----- #
plt.xlabel('Condition')
plt.ylabel(ylabel)
plt.setp(ax.get_xticklabels(), rotation=0) #labelsが重なった時角度変更
# plt.ylim(1,7)
plt.show()