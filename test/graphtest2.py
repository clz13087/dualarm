import graph
from matplotlib import pyplot as plt
import numpy as np
from FileIO import FileIO

# ----- csvからデータを取得 ----- #
fileIO = FileIO()
dat = fileIO.Read('graphtest2.csv',',')
leftdata = [addr for addr in dat if 'leftdata' in addr[0]]
xlabel = [addr for addr in dat if 'xlabel' in addr[0]][0][1]
ylabel = [addr for addr in dat if 'ylabel' in addr[0]][0][1]
width = [addr for addr in dat if 'width' in addr[0]][0][1]
leftmax = [addr for addr in dat if 'leftmax' in addr[0]][0][1]
leftmin = [addr for addr in dat if 'leftmin' in addr[0]][0][1]
heightmax = [addr for addr in dat if 'heightmax' in addr[0]][0][1]
heightmin = [addr for addr in dat if 'heightmin' in addr[0]][0][1]
title = [addr for addr in dat if 'title' in addr[0]][0][1]

number = int(leftmax) - int(leftmin) + int(width)
a = int(leftmin)
height = []

# ----- 同じ値をカウント ----- #
while a <= number:
    b = str(a)
    count = leftdata[0].count(b)
    height.append(count)
    a += int(width)

# ----- leftを文字列に変換 ----- #
left = list(range(int(leftmin),int(leftmax)+1,int(width)))
left = list(map(str,left))

# ----- グラフ作成 ----- #
plt.bar(left, height, width = 1)
plt.xlabel(xlabel)
plt.ylabel(ylabel)
# plt.xlim(leftmin,leftmax)
# plt.ylim(heightmin,heightmax)
plt.title(title)
plt.show()

