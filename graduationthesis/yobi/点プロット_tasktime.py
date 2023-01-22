from operator import length_hint
from statistics import stdev
import graph
from matplotlib import pyplot as plt
import numpy as np
from FileIO import FileIO
import seaborn as sns

# ----- csvからデータを取得 ----- #
fileIO = FileIO()
# dat = fileIO.Read('SI2022主体感(3人用).csv', ',')
# dat = fileIO.Read('SI2022所有感(3人用).csv', ',')
# dat = fileIO.Read('SI2022操作性(3人用).csv', ',')
# dat = fileIO.Read('SI2022連帯感(3人用).csv', ',')
# dat = fileIO.Read('SI2022tasktime.csv', ',')
dat = fileIO.Read('SI2022tasktime_点プロット.csv', ',')
# dat = fileIO.Read('SI2022NASATLX_点プロット.csv', ',')

ylabel = [addr for addr in dat if 'ylabel' in addr[0]][0][1]
# OP1 = [addr for addr in dat if 'OP1_A' in addr[0]]
# OP2 = [addr for addr in dat if 'OP1_B' in addr[0]]
# OP3 = [addr for addr in dat if 'OP2_1_A' in addr[0]]
# OP4 = [addr for addr in dat if 'OP2_1_B' in addr[0]]
# OP5 = [addr for addr in dat if 'OP2_2_A' in addr[0]]
# OP6 = [addr for addr in dat if 'OP2_2_B' in addr[0]]
# OP7 = [addr for addr in dat if 'OP3_A' in addr[0]]
# OP8 = [addr for addr in dat if 'OP3_B' in addr[0]]

OP1 = [addr for addr in dat if 'OP1' in addr[0]]
OP2 = [addr for addr in dat if 'OP2_1' in addr[0]]
OP3 = [addr for addr in dat if 'OP2_2' in addr[0]]
OP4 = [addr for addr in dat if 'OP3' in addr[0]]

# # ylabel = [addr for addr in dat if 'ylabel' in addr[0]][0][1]
# # OP1 = [addr for addr in dat if 'OP1_A' in addr[0]]
# # OP2 = [addr for addr in dat if 'OP1_B' in addr[0]]
# # OP3 = [addr for addr in dat if 'OP2_1_A' in addr[0]]
# # OP4 = [addr for addr in dat if 'OP2_1_B' in addr[0]]
# # OP5 = [addr for addr in dat if 'OP2_2_A' in addr[0]]
# # OP6 = [addr for addr in dat if 'OP2_2_B' in addr[0]]
# # OP7 = [addr for addr in dat if 'OP3_1_A' in addr[0]]
# # OP8 = [addr for addr in dat if 'OP3_1_B' in addr[0]]
# # OP9 = [addr for addr in dat if 'OP3_2_A' in addr[0]]
# # OP10 = [addr for addr in dat if 'OP3_2_B' in addr[0]]



# # ----- dict型に変換 ----- #
# # ALLdata = dict(OP1 = OP1, OP2 = OP2, OP3 = OP3, OP4 = OP4,)
# # OP = dict(OP1 = [], OP2 = [], OP3 = [], OP4 = [])

# ----- 不要部分を除く ----- #
# OP1[0].remove('OP1_A')
# OP2[0].remove('OP1_B')
# OP3[0].remove('OP2_1_A')
# OP4[0].remove('OP2_1_B')
# OP5[0].remove('OP2_2_A')
# OP6[0].remove('OP2_2_B')
# OP7[0].remove('OP3_A')
# OP8[0].remove('OP3_B')

OP1[0].remove('OP1')
OP2[0].remove('OP2_1')
OP3[0].remove('OP2_2')
OP4[0].remove('OP3')

# # OP1[0].remove('OP1_A')
# # OP2[0].remove('OP1_B')
# # OP3[0].remove('OP2_1_A')
# # OP4[0].remove('OP2_1_B')
# # OP5[0].remove('OP2_2_A')
# # OP6[0].remove('OP2_2_B')
# # OP7[0].remove('OP3_1_A')
# # OP8[0].remove('OP3_1_B')
# # OP9[0].remove('OP3_2_A')
# # OP10[0].remove('OP3_2_B')

# ----- list型に変換 ----- #
# OP1str = OP1[0]
# OP2str = OP2[0]
# OP3str = OP3[0]
# OP4str = OP4[0]
# OP5str = OP5[0]
# OP6str = OP6[0]
# OP7str = OP7[0]
# OP8str = OP8[0]

OP1str = OP1[0]
OP2str = OP2[0]
OP3str = OP3[0]
OP4str = OP4[0]

# # OP9str = OP9[0]
# # OP10str = OP10[0]

# OP1list = list(map(float,OP1str))
# OP2list = list(map(float,OP2str))
# OP3list = list(map(float,OP3str))
# OP4list = list(map(float,OP4str))
# OP5list = list(map(float,OP5str))
# OP6list = list(map(float,OP6str))
# OP7list = list(map(float,OP7str))
# OP8list = list(map(float,OP8str))

OP1list = list(map(float,OP1str))
OP2list = list(map(float,OP2str))
OP3list = list(map(float,OP3str))
OP4list = list(map(float,OP4str))

# OP1list = 1
# OP2list = 2
# OP3list = 3
# OP4list = 4
# OP5list = 5
# OP6list = 5
# OP7list = 7
# OP8list = 5

# # OP9list = list(map(float,OP9str))
# # OP10list = list(map(float,OP10str))

# # # ----- 棒グラフ ----- #
# # left = ['1', '2人(別々)','2人(融合)', '3']
# # height = np.array([average_OP1, average_OP2_1, average_OP2_2, average_OP3])
# # plt.bar(left, height, yerr = y_err, width=0.5, capsize=5, color = color)
# # plt.xlabel('Condition')
# # plt.ylabel(ylabel)
# # # plt.ylim(1,7)
# # plt.show()



# # ----- プロット ----- #
# left = ['1_A','1_B', '2_A (separate)', '2_B (separate)','2_A (integration)','2_B (integration)', '3_A', '3_B']
# height = [OP1list, OP2list, OP3list, OP4list, OP5list, OP6list, OP7list, OP8list]

# left = ['1_A','1_B', '2_A (separate)', '2_B (separate)','2_A (integration)','2_B (integration)', '3_A (center)','3_B (center)', '3_A (side)', '3_B (side)']
# height = [OP1list, OP2list, OP3list, OP4list, OP5list, OP6list, OP7list, OP8list, OP9list, OP10list]



# # ----- 箱ひげ図 ----- #
# fig, ax = plt.subplots()
# left = ['1', '2(separate)', '2(integration)', '3(center)', '3(side)']
# height = [OP1list, OP2list, OP3list, OP4list, OP5list] 

# # ----- (操作性用) ----- #
# left = ['2(separate)','2(integration)', '3']
# height = [OP2list, OP3list, OP4list]

# # ----- (操作性用3) ----- #
# left = ['2(separate)','2(integration)', '3(center)', '3(side)']
# height = [OP2list, OP3list, OP4list, OP5list]

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

# ----- boxの色のリスト ----- #
# colors = ['dodgerblue','steelblue','deepskyblue','mediumblue']
# colors = ['darkgray','steelblue','dodgerblue','deepskyblue']
# colors = ['dimgray','gray','darkgray','lightgray','gainsboro']

# ----- (操作性用) ----- #
# colors = ['gray','darkgray','lightgray']

# ----- (操作性用3) ----- #
# colors = ['gray','darkgray','lightgray','gainsboro']

# # ----- boxの色の設定 ----- #
# for b, c in zip(bp['boxes'], colors):
#     b.set(color='black', linewidth=1)  # boxの外枠の色
#     b.set_facecolor(c) # boxの色


# height1 = [OP1list[0],OP2list[0],OP3list[0],OP4list[0],OP5list[0],OP6list[0],OP7list[0],OP8list[0]]
# height2 = [OP1list[1],OP2list[1],OP3list[1],OP4list[1],OP5list[1],OP6list[1],OP7list[1],OP8list[1]]
# height3 = [OP1list[2],OP2list[2],OP3list[2],OP4list[2],OP5list[2],OP6list[2],OP7list[2],OP8list[2]]
# height4 = [OP1list[3],OP2list[3],OP3list[3],OP4list[3],OP5list[3],OP6list[3],OP7list[3],OP8list[3]]
# height5 = [OP1list[4],OP2list[4],OP3list[4],OP4list[4],OP5list[4],OP6list[4],OP7list[4],OP8list[4]]
# left = ['1_A','1_B', '2_A (separate)', '2_B (separate)','2_A (integration)','2_B (integration)', '3_A', '3_B']

height1 = [OP1list[0],OP2list[0],OP3list[0],OP4list[0]]
height2 = [OP1list[1],OP2list[1],OP3list[1],OP4list[1]]
height3 = [OP1list[2],OP2list[2],OP3list[2],OP4list[2]]
height4 = [OP1list[3],OP2list[3],OP3list[3],OP4list[3]]
height5 = [OP1list[4],OP2list[4],OP3list[4],OP4list[4]]
height6 = [OP1list[5],OP2list[5],OP3list[5],OP4list[5]]
height7 = [OP1list[6],OP2list[6],OP3list[6],OP4list[6]]
height8 = [OP1list[7],OP2list[7],OP3list[7],OP4list[7]]
height9 = [OP1list[8],OP2list[8],OP3list[8],OP4list[8]]
height10 = [OP1list[9],OP2list[9],OP3list[9],OP4list[9]]
left = ['1', '2 (separate)', '2 (integration)', '3']

# ----- 縦横ラベル ----- #
fig, ax = plt.subplots()
ax.scatter(left, height1, color = "k")
ax.scatter(left, height2, color = "k")
ax.scatter(left, height3, color = "k")
ax.scatter(left, height4, color = "k")
ax.scatter(left, height5, color = "k")
ax.scatter(left, height6, color = "k")
ax.scatter(left, height7, color = "k")
ax.scatter(left, height8, color = "k")
ax.scatter(left, height9, color = "k")
ax.scatter(left, height10, color = "k")
plt.xlabel('Condition')
plt.ylabel(ylabel)
# plt.setp(ax.get_xticklabels(), rotation=0) #labelsが重なった時角度変更
# sns.swarmplot(y = height, color="r")
plt.ylim(10,40)
plt.show()