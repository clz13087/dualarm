# Author: Tsugumi Sato

from tkinter import E
from turtle import pos, position
import numpy as np
from FileIO import FileIO


if __name__ == '__main__':
    print('hello')


for i in range(3):
    print(i)


newid=1
print('participant'+str(newid))



season = {'春':'spring','夏':'summer','秋':'autumn','冬':'winter'}
print(season['夏'])

class Boy:
    def __init__(self,name,place_of_birth):
        # OK:インスタンス変数
        self.name = name
        self.place_of_birth = place_of_birth

    def print(self):
        print('{}君:{}生まれ'.format(self.name,self.place_of_birth))

    def print2(self):
        print(self.name)

boy1 = Boy('tsugumi','aichi')
boy2 = Boy('wataru','tokyo')

boy1.print()
boy2.print2()

def max(a,b,c):
    ''''3つの値の最大値を求めて返却'''
    max = a
    if b > max: max = b
    if c > max: max = c
    return max

print(max(6,2,4))

def max2(a,b):
    '''aとbの最大値を求めて返却'''
    if a > b:
        return a
    return b

print(max2(4,1))

flag = True

if flag:
    print('true')

else:
     print('false')

x = [n for n in range(1,8)]
print(x)

y = [n for n in range(1,8) if n%2 == 0]
print(y)


z = [[1,2,3,],[4,5,6,]]

print(z[0])
print(z[1])
print(z[1][2])



# fileIO = FileIO()

# dat = fileIO.Read('test.csv',',')

# xArmIP1 = [addr for addr in dat if 'xArmIP1' in addr[0]][0][1]
# xArmIP2 = [addr for addr in dat if 'xArmIP2' in addr[0]][0][1]

# print(xArmIP1)
# print(xArmIP2)




A = np.array([[1,2,3],[4,5,6],[7,8,9]])
B = np.array([1,2])
ADim = A.ndim
BDim = B.ndim
print(ADim,BDim)


def divide_each(a, b):
    try:
        print(a/b)
    
    except ZeroDivisionError as e:
        print(type(e))
    
    except:
        print('Error')

    else:
        print('正常終了')
    
    finally:
        print('お疲れ様です')


divide_each(4,2)
divide_each(1, 0)
divide_each('a','b')



pos = {'p1':1,'p2':2,'p3':3,'p4':4}
roles = ['p1','p2','p3','p4']

print(pos[roles[0]],pos[roles[3]])

participantNum = 3
pN = participantNum
weightSliderList = []
weightSliderList_0 = [1/pN for n in range(pN)]
weightSliderList = [weightSliderList_0,weightSliderList_0]

print(weightSliderList)
print(type(weightSliderList))

s = np.array([[1,2,3],[4,5,6]])

print(s)

list = [n for n in range(7) if n%2 == 0 ]
print(list, end = ' ')

