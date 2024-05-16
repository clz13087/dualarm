from operator import length_hint
from ssl import OP_ALL
from statistics import stdev
import graph
from matplotlib import pyplot as plt
import numpy as np
from FileIO import FileIO

# ----- csvからデータを取得(任意のdataのコメントアウトを外す) ----- #
fileIO = FileIO()

# ----- 2条件 or 3条件 ----- #
mode = 3

# ----- x座標 ----- #
# dat = fileIO.Read('主体感絶対.csv', ',')
# dat = fileIO.Read('主体感相対.csv', ',')
dat = fileIO.Read('tasktime絶対プロット.csv', ',')
# dat = fileIO.Read('Jerk絶対プロット.csv', ',')
# dat = fileIO.Read('シンクロparticipant.csv', ',')
# dat = fileIO.Read('tasktime練習.csv', ',')
# dat = fileIO.Read('Jerk練習.csv', ',')
# dat = fileIO.Read('tasktime相対.csv', ',')
# dat = fileIO.Read('NASATLX絶対.csv', ',')
# dat = fileIO.Read('NASATLX相対.csv', ',')
# dat = fileIO.Read('所有感絶対.csv', ',')
# dat = fileIO.Read('所有感相対.csv', ',')
# dat = fileIO.Read('操作性絶対.csv', ',')
# dat = fileIO.Read('操作性相対.csv', ',')
# dat = fileIO.Read('FoC絶対.csv', ',')kore
# dat = fileIO.Read('FoC相対.csv', ',')
# dat = fileIO.Read('FoC to Control Rate.csv', ',')
# dat = fileIO.Read('操作量.csv', ',')
# dat = fileIO.Read('連帯感.csv', ',')

# dat = fileIO.Read('tasktime絶対.csv', ',')
# dat = fileIO.Read('Jerk Index average(left arm).csv', ',')
# dat = fileIO.Read('Jerk Index average(right arm).csv', ',')
# dat = fileIO.Read('Jerk Index average(dual-arm).csv', ',')
# dat = fileIO.Read('シンクロ.csv', ',')

# dat = fileIO.Read('Jerk Index(dual-arm).csv', ',')
# dat = fileIO.Read('tasktimenotaverage.csv', ',')
# dat = fileIO.Read('シンクロnotaverage.csv', ',')

xlabel = [addr for addr in dat if 'ylabel' in addr[0]][0][1]
OP1_x = [addr for addr in dat if 'OP1' in addr[0]]
OP2_x = [addr for addr in dat if 'OP2' in addr[0]]
OP3_x = [addr for addr in dat if 'OP3' in addr[0]]

# ----- y座標 ----- #
# dat = fileIO.Read('主体感絶対.csv', ',')
# dat = fileIO.Read('主体感相対.csv', ',')
# dat = fileIO.Read('tasktime絶対プロット.csv', ',')
# dat = fileIO.Read('Jerk絶対プロット.csv', ',')
# dat = fileIO.Read('シンクロparticipant.csv', ',')
dat = fileIO.Read('tasktime練習.csv', ',')
# dat = fileIO.Read('Jerk練習.csv', ',')
# dat = fileIO.Read('tasktime相対.csv', ',')
# dat = fileIO.Read('NASATLX絶対.csv', ',')
# dat = fileIO.Read('NASATLX相対.csv', ',')
# dat = fileIO.Read('所有感絶対.csv', ',')
# dat = fileIO.Read('所有感相対.csv', ',')
# dat = fileIO.Read('操作性絶対.csv', ',')
# dat = fileIO.Read('操作性相対.csv', ',')
# dat = fileIO.Read('FoC絶対.csv', ',')
# dat = fileIO.Read('FoC相対.csv', ',')
# dat = fileIO.Read('FoC to Control Rate.csv', ',')
# dat = fileIO.Read('操作量.csv', ',')kore
# dat = fileIO.Read('連帯感.csv', ',')

# dat = fileIO.Read('tasktime絶対.csv', ',')
# dat = fileIO.Read('Jerk Index average(left arm).csv', ',')
# dat = fileIO.Read('Jerk Index average(right arm).csv', ',')
# dat = fileIO.Read('Jerk Index average(dual-arm).csv', ',')
# dat = fileIO.Read('シンクロ.csv', ',')

# dat = fileIO.Read('Jerk Index(dual-arm).csv', ',')
# dat = fileIO.Read('tasktimenotaverage.csv', ',')
# dat = fileIO.Read('シンクロnotaverage.csv', ',')

ylabel = [addr for addr in dat if 'ylabel' in addr[0]][0][1]
OP1_y = [addr for addr in dat if 'OP1' in addr[0]]
OP2_y = [addr for addr in dat if 'OP2' in addr[0]]
OP3_y = [addr for addr in dat if 'OP3' in addr[0]]


if mode == 3:
    # ----- 不要部分を除く ----- #
    OP1_x[0].remove('OP1')
    OP2_x[0].remove('OP2')
    OP3_x[0].remove('OP3')
    OP1_y[0].remove('OP1')
    OP2_y[0].remove('OP2')
    OP3_y[0].remove('OP3')

    # ----- list型に変換 ----- #
    OP1_x = list(map(float,OP1_x[0]))
    OP2_x = list(map(float,OP2_x[0]))
    OP3_x = list(map(float,OP3_x[0]))
    OP1_y = list(map(float,OP1_y[0]))
    OP2_y = list(map(float,OP2_y[0]))
    OP3_y = list(map(float,OP3_y[0]))
    # OP1_x = np.log10(OP1_x)
    # OP2_x = np.log10(OP2_x)
    # OP3_x = np.log10(OP3_x)
    # OP1_y = np.log10(OP1_y)
    # OP2_y = np.log10(OP2_y)
    # OP3_y = np.log10(OP3_y)

    # 相関係数
    x = OP1_x + OP2_x + OP3_x
    y = OP1_y + OP2_y + OP3_y
    correlation = np.corrcoef(x, y)[0, 1]
    print(x)
    print(y)
    print("相関係数：", correlation)

    # プロット
    fig, ax = plt.subplots()
    # ax.scatter(OP1_x, OP1_y, c='olivedrab', label='1')
    # ax.scatter(OP2_x, OP2_y, c='steelblue', label='2')
    # ax.scatter(OP3_x, OP3_y, c='darkorange', label='3')
    ax.scatter(OP1_x, OP1_y, s=100, c="white", alpha=1, edgecolors="k", label='1') 
    ax.scatter(OP2_x, OP2_y, s=100, c="white", alpha=1, edgecolors="k", label='2', marker="s") 
    ax.scatter(OP3_x, OP3_y, s=100, c="white", alpha=1, edgecolors="k", label='3', marker="^") 
    # plt.text(0.9, 0.1, f"r = {correlation:.3f}", ha="right", va="top", transform=plt.gca().transAxes)

    # 軸のタイトルや凡例などの設定
    # ax.set_title('3つの凡例を持つグラフ')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    # plt.legend(loc='center left', bbox_to_anchor=(1., .5))
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1.03), ncol=3)
    plt.ylim(0,60)
    plt.xlim(0,60)

    # グラフの表示
    plt.show()

if mode == 2:
    # ----- 不要部分を除く ----- #
    OP2_x[0].remove('OP2')
    OP3_x[0].remove('OP3')
    OP2_y[0].remove('OP2')
    OP3_y[0].remove('OP3')

    # ----- list型に変換 ----- #
    OP2_x = list(map(float,OP2_x[0]))
    OP3_x = list(map(float,OP3_x[0]))
    OP2_y = list(map(float,OP2_y[0]))
    OP3_y = list(map(float,OP3_y[0]))
    # OP2_x = np.log10(OP2_x)
    # OP3_x = np.log10(OP3_x)
    # OP2_y = np.log10(OP2_y)
    # OP3_y = np.log10(OP3_y)

    # 相関係数
    x = OP2_x + OP3_x
    y = OP2_y + OP3_y
    correlation = np.corrcoef(x, y)[0, 1]
    print("相関係数：", correlation)

    # プロット
    fig, ax = plt.subplots()
    # ax.scatter(OP2_x, OP2_y, c='steelblue', label='2')
    # ax.scatter(OP3_x, OP3_y, c='darkorange', label='3')
    ax.scatter(OP2_x, OP2_y, s=100, c="gray", alpha=1, linewidths=0, edgecolors="gray", label='2') 
    ax.scatter(OP3_x, OP3_y, s=60, c="darkorange", alpha=1, linewidths=0, edgecolors="darkorange", label='3') 
    plt.text(0.1, 0.1, f"r = {correlation:.3f}", ha="right", va="top", transform=plt.gca().transAxes)

    # 軸のタイトルや凡例などの設定
    # ax.set_title('3つの凡例を持つグラフ')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    # plt.legend(loc='center left', bbox_to_anchor=(1., .5))
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1.03), ncol=3)
    # plt.ylim(0,101)
    # plt.xlim(0,1.01)

    # グラフの表示
    plt.show()