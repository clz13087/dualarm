''' Send the position and rotation to the xArm'''

# Author: Tsugumi Sato

from turtle import position


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

boy1 = Boy('tsugumi','aichi')
boy2 = Boy('wataru','tokyo')

boy1.print()


import numpy as np

A = np.ndarray([1,2,3,4],[5,6,7,8])

print(A)