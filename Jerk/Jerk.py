import pandas as pd
import numpy as np
import csv

with open('data/src/sample.csv') as f:
    print(f.read)

class JRK:
    def __init__(self) -> None:
        print('--- import --- : Motion Analysis Jerk')

    def JRK_C(self,d):
        print('--- calculate --- : Motion Analysis Jerk')
        self.get_data(d)
        self.jrk = self.Ahmad_2016()
        print('jrk : ',self.jrk)
        return self.jrk    
    
    def Ahmad_2016(self):
        self.jrk_sq_list = []
        for i in range(len(self.j_x)):
            self.jrk_sq = self.j_x[i]**2 + self.j_y[i]**2 + self.j_z[i]**2            
            self.jrk_sq_list.append(self.jrk_sq)
        self.sum_jrk = np.sum(self.jrk_sq_list)
        self.dt = self.tl.values[-1] - self.tl.values[0]
        self.vel_sq_list = []
        for i in range(len(self.v_x)):
            self.vel_sq = np.sqrt(self.v_x[i]**2 + self.v_y[i]**2 + self.v_z[i]**2)
            self.vel_sq_list.append(self.vel_sq)
        self.sum_vel = np.sum(self.vel_sq_list)
        self.normalized_Jrk_index = self.sum_jrk * self.dt**5 / (self.sum_vel**2)
        return self.normalized_Jrk_index    
        
    def get_data(self,data):
        self.tl = data['time']
        self.v_x = data['vx']
        self.v_y = data['vy']
        self.v_z = data['vz']
        self.j_x = data['jx']
        self.j_y = data['jy']
        self.j_z = data['jz']


if __name__ == '__main__':
    jrkclass = JRK
    jrk = jrkclass.JRK_C