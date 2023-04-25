from lib2to3.pgen2.token import OP
from operator import length_hint
from re import A
from statistics import stdev

from cv2 import DISOpticalFlow_PRESET_ULTRAFAST
import graph
from matplotlib import pyplot as plt
import numpy as np
from FileIO import FileIO
import matplotlib.ticker as ptick
from matplotlib.ticker import ScalarFormatter

class Box:
    def __init__(self) -> None:
        pass

    def boxplot(self, dat):
        self.dat = dat
        ylabel = [addr for addr in self.dat if 'ylabel' in addr[0]][0][1]
        OP1 = [addr for addr in self.dat if 'OP1' in addr[0]]
        OP2 = [addr for addr in self.dat if 'OP2' in addr[0]]
        OP3 = [addr for addr in self.dat if 'OP3' in addr[0]]

        # ----- 不要部分を除く ----- #
        OP1[0].remove('OP1')
        OP2[0].remove('OP2')
        OP3[0].remove('OP3')

        # ----- list型に変換 ----- #
        OP1str = OP1[0]
        OP2str = OP2[0]
        OP3str = OP3[0]
        OP1list = list(map(float,OP1str))
        OP2list = list(map(float,OP2str))
        OP3list = list(map(float,OP3str))
        # OP1list = np.log10(OP1list)
        # OP2list = np.log10(OP2list)
        # OP3list = np.log10(OP3list)

        # ----- 箱ひげ図 ----- #
        fig, ax = plt.subplots()
        left = ['1', '2', '3']
        height = [OP1list, OP2list, OP3list]

        bp=ax.boxplot(height,
                    labels = left,  #条件
                    vert=True,  # 縦向きにする
                    patch_artist=True,  # 細かい設定をできるようにする
                    widths=0.7,  # boxの幅の設定
                    medianprops=dict(color='black', linewidth=1),  # 中央値の線の設定
                    whiskerprops=dict(color='black', linewidth=1),  # ヒゲの線の設定
                    capprops=dict(color='black', linewidth=1),  # ヒゲの先端の線の設定
                    flierprops=dict(markeredgecolor='black', markeredgewidth=0)  # 外れ値の設定
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
        plt.ylim(0,0.50*10**14)

        # ax.set(ylabel=r'$log_{10}Jerk Index$')
        plt.show()

    def boxplotfor2(self, dat):
        self.dat = dat
        ylabel = [addr for addr in self.dat if 'ylabel' in addr[0]][0][1]
        # OP1 = [addr for addr in self.dat if 'OP1' in addr[0]]
        OP2 = [addr for addr in self.dat if 'OP2' in addr[0]]
        OP3 = [addr for addr in self.dat if 'OP3' in addr[0]]

        # ----- 不要部分を除く ----- #
        # OP1[0].remove('OP1')
        OP2[0].remove('OP2')
        OP3[0].remove('OP3')

        # ----- list型に変換 ----- #
        # OP1str = OP1[0]
        OP2str = OP2[0]
        OP3str = OP3[0]
        # OP1list = list(map(float,OP1str))
        OP2list = list(map(float,OP2str))
        OP3list = list(map(float,OP3str))
        # OP1list = np.log10(OP1list)
        # OP2list = np.log10(OP2list)
        # OP3list = np.log10(OP3list)

        # ----- 箱ひげ図 ----- #
        fig, ax = plt.subplots()
        left = ['2', '3']
        height = [OP2list, OP3list]

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
        colors = ['gray','darkgray','lightgray']

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
        # plt.ylim(0,0.50*10**14)

        # ax.set(ylabel=r'$log_{10}Jerk Index$')
        plt.show()

if __name__ == '__main__':
    # # ----- csvからデータを取得 ----- #
    fileIO = FileIO()
    # dat_1 = fileIO.Read('主体感絶対.csv', ',')
    # dat_2 = fileIO.Read('主体感相対.csv', ',')

    # dat_3 = fileIO.Read('tasktime絶対.csv', ',')
    # dat_4 = fileIO.Read('tasktime相対.csv', ',')

    # dat_5 = fileIO.Read('NASATLX絶対.csv', ',')
    # dat_6 = fileIO.Read('NASATLX相対.csv', ',')

    # dat_7 = fileIO.Read('所有感絶対.csv', ',')
    # dat_8 = fileIO.Read('所有感相対.csv', ',')

    # dat_9 = fileIO.Read('操作性絶対.csv', ',')
    # dat_10 = fileIO.Read('操作性相対.csv', ',')

    # dat_11 = fileIO.Read('FoC絶対.csv', ',')
    # dat_12 = fileIO.Read('FoC相対.csv', ',')

    # dat_13 = fileIO.Read('FoC to Control Rate.csv', ',')

    # dat_14 = fileIO.Read('Jerk Index average(left arm).csv', ',')
    # dat_15 = fileIO.Read('Jerk Index average(right arm).csv', ',')
    # dat_16 = fileIO.Read('Jerk Index average(dual-arm).csv', ',')

    # dat_17 = fileIO.Read('連帯感.csv', ',')

    box = Box()
    dat = fileIO.Read('name.csv', ',')
    name = [addr for addr in dat if 'name' in addr[0]]
    name[0].remove('name')
    for i in range(17):
        name_str = name[0][i] + '.csv'
        dat = fileIO.Read(name_str, ',')
        if i < 16:
            box.boxplot(dat)
        elif i == 16:
            box.boxplotfor2(dat)
        