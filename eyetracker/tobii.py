# ----------------------------------------------------------------------- 
# Author:   Tsugumi Sato (NIT)
# Created:  2022/8/30
# Summary:  tobii全般
# -----------------------------------------------------------------------

from re import L
import tobiiresearch as tr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import screeninfo
from FileIO.FileIO import FileIO
import cv2

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
        self.l = self.robotspace
        self.r = 1 - self.robotspace
        self.cl = (1 - self.taskspace)/2
        self.cr = (1 + self.taskspace)/2
        weightlist = []

        # ----- change weight according to eye_x ----- #
        if eye_x < self.l:
            weightlist = [self.sideweight, 1]
        elif eye_x >= self.l and eye_x < self.cl:
            weightslider = ((eye_x - self.l)/(self.centerweight - self.sideweight))*(self.cl - self.l) + self.l
            weightlist = [weightslider, weightslider]
        elif eye_x >= self.cl and eye_x <= self.cr:
            weightlist = [self.centerweight, self.centerweight]
        elif eye_x > self.cr and eye_x <= self.r:
            weightslider = ((eye_x - self.cr)/(self.sideweight - self.centerweight))*(self.r - self.cr) + self.cr
            weightlist = [weightslider, weightslider]
        elif eye_x > self.r:
            weightlist = [1, self.sideweight]
        else:
            weightlist = [self.sideweight, self.sideweight]

        print('weightlist:',weightlist)
        return weightlist

    def camera(self):
        """
        display camera image & weight lines
        """
        # ----- connect camera ----- #
        cap = cv2.VideoCapture(0)

        # ----- get camera info ----- #
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # ----- set weight lines ----- #
        line1_x = self.l * width
        line2_x = self.cl * width
        line3_x = self.cr * width
        line4_x = self.r * width
        line_y = height

        # ----- get data ----- #
        ret,frame = cap.read()

        # ----- for failure ----- #
        if ret == False:
            print('画像取得できませんでした')
        
        # ----- display lines ----- #
        cv2.line(frame, pt1=(int(line1_x), 0), pt2=(int(line1_x), line_y), color=(0,0,255),thickness= 4)
        cv2.line(frame, pt1=(int(line2_x), 0), pt2=(int(line2_x), line_y), color=(0,255,0),thickness= 4)
        cv2.line(frame, pt1=(int(line3_x), 0), pt2=(int(line3_x), line_y), color=(0,255,0),thickness= 4)
        cv2.line(frame, pt1=(int(line4_x), 0), pt2=(int(line4_x), line_y), color=(0,0,255),thickness= 4)

        # ----- display camera image ----- #
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)   #取得した画像のグレースケール画像を取得する
        cv2.imshow('f',frame)       #リアルタイムに取得した生画像を表示
        # cv2.imshow('g',gray)        #生画像をグレースケールにした画像を表示

        # ----- push q to end getting data ----- #
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

        # ----- disconnect and destroy window----- #
        # cap.release()
        # cv2.destroyAllWindows()

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