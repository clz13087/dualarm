import tobii_research as tr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import screeninfo

def gaze_data_callback(gaze_data):
    global right_01, left_01

    right_01 = list(gaze_data['right_gaze_point_on_display_area'])
    left_01 = list(gaze_data['left_gaze_point_on_display_area'])

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

    