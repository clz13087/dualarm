import cv2
from tobii import Tobii
import screeninfo

robotspace = 0.15
taskspace = 0.3

l = robotspace
r = 1 - robotspace
cl = (1 - taskspace)/2
cr = (1 + taskspace)/2


# ----- connect camera ----- #
cap = cv2.VideoCapture(0)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

s_info = screeninfo.get_monitors()
if len(s_info) == 1:
    s_info = s_info[0]
    s_width = s_info.width
    s_height = s_info.height
elif len(s_info) == 2:
    s_info = s_info[1]
    s_width = s_info.width
    s_height = s_info.height

s_width =  3008
s_height = 1692

line1_x = l * s_width
line2_x = cl * s_width
line3_x = cr * s_width
line4_x = r * s_width
line_y = s_height

while(True):
    
    robotspace = 0.15
    taskspace = 0.3

    l = robotspace
    r = 1 - robotspace
    cl = (1 - taskspace)/2
    cr = (1 + taskspace)/2

    s_width = 1920
    s_height = 1080

    line1_x = l * s_width
    line2_x = cl * s_width
    line3_x = cr * s_width
    line4_x = r * s_width
    line_y = s_height

    # ----- get data ----- #
    ret,frame = cap.read()

    # ----- for failure ----- #
    if ret == False:
        print('画像取得できませんでした')   
        break

    cv2.line(frame, pt1=(int(line1_x), 0), pt2=(int(line1_x), line_y), color=(0,0,255),thickness= 4)
    cv2.line(frame, pt1=(int(line2_x), 0), pt2=(int(line2_x), line_y), color=(0,255,0),thickness= 4)
    cv2.line(frame, pt1=(int(line3_x), 0), pt2=(int(line3_x), line_y), color=(0,255,0),thickness= 4)
    cv2.line(frame, pt1=(int(line4_x), 0), pt2=(int(line4_x), line_y), color=(0,0,255),thickness= 4)

    # ----- display camera image ----- #
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)   #取得した画像のグレースケール画像を取得する
    cv2.imshow('f',frame)       #リアルタイムに取得した生画像を表示
    # cv2.imshow('g',gray)        #生画像をグレースケールにした画像を表示

    # ----- push q to end getting data ----- #
    if cv2.waitKey(1) & 0xFF == ord('q'):   
        break

# ----- disconnect and destroy window----- #
cap.release()
cv2.destroyAllWindows()