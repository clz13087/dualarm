# ----------------------------------------------------------------------- 
# Author:   Tsugumi Sato (NIT)
# Created:  2022/8/30
# Summary:  tobii全般
# -----------------------------------------------------------------------

import tobiiresearch as tr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import screeninfo
from FileIO.FileIO import FileIO

class Tobii:
    def __init__(self, robotspace: float, taskspace: float, sideweight: float, centerweight: float) -> None:
        # ----- read parameters from setting.csv ----- #
        # fileIO = FileIO()
        # dat = fileIO.Read('settings.csv', ',')
        # ----- ここはrobotcontrolmanagerclassに追加 ----- #
        # robotspace = [addr for addr in dat if 'robotspace' in addr[0]][0][1]
        # taskspace = [addr for addr in dat if 'taskspace' in addr[0]][0][1]
        # sideweight = [addr for addr in dat if 'sideweight' in addr[0]][0][1]
        # centerweight = [addr for addr in dat if 'centerweight' in addr[0]][0][1]
        self.robotspace = robotspace
        self.taskspace = taskspace
        self.sideweight = sideweight
        self.centerweight = centerweight

    def eyedata2weight(self):
        """
        eyedata2weight
        """
        # ----- find eyetracker ----- #
        found_eyetrackers = tr.find_all_eyetrackers()
        my_eyetracker = found_eyetrackers[0]
        eye(my_eyetracker)

        # ----- l: left, r: right, cl: center left, cr: center right ----- #
        l = self.robotspace
        r = 1 - self.robotspace
        cl = (1 - self.taskspace)/2
        cr = (1 + self.taskspace)/2
        weightlist = []

        # ----- change weight according to eye_x ----- #
        if eye_x < l:
            weightlist = [self.sideweight, 1]
        elif eye_x >= l and eye_x < cl:
            weightslider = ((eye_x - l)/(self.centerweight - self.sideweight))*(cl - l) +l
            weightlist = [weightslider, weightslider]
        elif eye_x >= cl and eye_x <= cr:
            weightlist = [self.centerweight, self.centerweight]
        elif eye_x > cr and eye_x <= r:
            weightslider = ((eye_x - cr)/(self.sideweight - self.centerweight))*(r - cr) + cr
            weightlist = [weightslider, weightslider]
        elif eye_x > r:
            weightlist = [1, self.sideweight]
        else:
            weightlist = [self.sideweight, self.sideweight]
        
        weightlist = weightlist.reshape(len(weightlist),1)

        print('weightlist:',weightlist)
        return weightlist

def gaze_data_callback(gaze_data):
    global eye_x, eye_y

    right_01 = list(gaze_data['right_gaze_point_on_display_area'])
    left_01 = list(gaze_data['left_gaze_point_on_display_area'])

    eye_x = (right_01[0] + left_01[0])/2
    eye_y = (right_01[1] + left_01[1])/2

def eye(eyetracker):
    """
    call gaze_data_callback when tobii gets eye data
    """
    eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA,gaze_data_callback,as_dictionary=True)

def get_screen_information():
    """
    get screen information
    """
    s_info = screeninfo.get_monitors()
    if len(s_info) == 1:
        s_info = s_info[0]
        s_width = s_info.width
        s_height = s_info.height
    elif len(s_info) == 2:
        s_info = s_info[1]
        s_width = s_info.width
        s_height = s_info.height
    print("screen information: ",s_info)

    return s_width, s_height