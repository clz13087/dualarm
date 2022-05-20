# Author: Tsugumi Sato

from tkinter import E
from turtle import position
import numpy as np


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