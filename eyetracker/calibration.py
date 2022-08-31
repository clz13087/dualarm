# ----------------------------------------------------------------------- 
# Author:   Tsugumi Sato (NIT)
# Created:  2022/8/30
# Summary:  calibration
# -----------------------------------------------------------------------

import tobiiresearch as tr
import time
import cv2
import sys

# ----- find eyetracker ----- #
found_eyetrackers = tr.find_all_eyetrackers()
my_eyetracker = found_eyetrackers[0]

# ----- draw points for calibration ----- #
def draw_calibration_points(point):
    img_file_name = 'img/image' + str(point[0]) + '_' +str(point[1]) + '.png'
    img = cv2.imread(img_file_name)
    cv2.namedWindow('screen', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(
        'screen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('screen', img)
    cv2.waitKey(2500)  # 2.5s calibration

def calibration(eyetracker):
    calibration = tr.ScreenBasedCalibration(eyetracker)
    calibration.enter_calibration_mode()

    # ----- points for calibration ----- #
    points_to_calibrate = [(0.5,0.5),(0.1,0.1),(0.1,0.9),(0.9,0.1),(0.9,0.9)]

    for point in points_to_calibrate:
        print(("Show a point on screen at {0}.").format(point))
        draw_calibration_points(point)

        print(("Collecting data at {0}.").format(point))

        # ----- calibrate eyes ----- #
        if calibration.collect_data(point[0], point[1]) != tr.CALIBRATION_STATUS_SUCCESS:
            calibration.collect_data(point[0], point[1])

    # ----- display calibration result ----- #
    print('Computing and applying calibration.')
    calibration_result = calibration.compute_and_apply()
    print(('Compute and apply returned {0} and collected at {1} points.').
          format(calibration_result.status, len(calibration_result.calibration_points)))

    # ----- leave calibration mode ----- #
    calibration.leave_calibration_mode()
    print('Left calibration mode.')

if __name__ == '__main__':
    calibration(my_eyetracker)
    sys.exit()