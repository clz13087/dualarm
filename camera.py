import cv2

# ----- connect camera ----- #
capture = cv2.VideoCapture(0)

while(True):

    # ----- get data ----- #
    ret,frame = capture.read()

    # ----- for failure ----- #
    if ret == False:
        print('画像取得できませんでした')   
        break

    # ----- find eyetracker ----- #
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)   #取得した画像のグレースケール画像を取得する
    cv2.imshow('f',frame)       #リアルタイムに取得した生画像を表示
    # cv2.imshow('g',gray)        #生画像をグレースケールにした画像を表示

    # ----- push q to end getting data ----- #
    if cv2.waitKey(1) & 0xFF == ord('q'):   
        break

# ----- disconnect and destroy window----- #
capture.release()
cv2.destroyAllWindows()