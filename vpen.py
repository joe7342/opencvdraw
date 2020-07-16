import cv2
import numpy as np
import time
from time import strftime

load_from_disk = True
if load_from_disk:
#     blue = np.load('./color/blue.npy') # 偵測藍色物件
#     red = np.load('./color/red.npy') # 偵測紅色物件
    yellow = np.load('./color/yellow.npy') # 偵測黃色物件

# 畫筆初始顏色
pen_color = (255,0,0)

cap = cv2.VideoCapture(0)

# Load these 2 images and resize them to the same size.
# 左上角切換功能圖片 resize
pen_img = cv2.resize(cv2.imread('./img/pen.png',1), (60, 60))
eraser_img = cv2.resize(cv2.imread('./img/eraser.png',1), (60, 60))

kernel = np.ones((5,5),np.uint8)

# Making window size adjustable
cv2.namedWindow('image', cv2.WINDOW_NORMAL)

# This is the canvas on which we will draw upon
# canvas 為畫布
canvas = None

# Create a background subtractor Object
# 使用Background Subtractor MOG 2背景分離指令(不偵測陰影)
backgroundobject = cv2.createBackgroundSubtractorMOG2(detectShadows = False)

# This threshold determines the amount of disruption in the background.
# 設定背景干擾的門檻值
background_threshold = 600

# A variable which tells you if you're using a pen or an eraser.
switch = 'Pen'

# With this variable we will monitor the time between previous switch.
# 此變數讓我們可以監控上一次切換所間隔的時間
last_switch = time.time()

# Initilize x1,y1 points
x1,y1=0,0

# Threshold for noise
# 干擾閾值
noiseth = 800

# Threshold for wiper, the size of the contour must be bigger than this for # us to clear the canvas
wiper_thresh = 40000

# A variable which tells when to clear canvas
clear = False

while(1):

    _, frame = cap.read()
    frame = cv2.flip( frame, 1 )
    
    cv2.putText(frame,'<- touch',(65,30),cv2.FONT_HERSHEY_DUPLEX, 0.6, (200,100,255), 1, cv2.LINE_AA)
    
    # Initilize the canvas as a black image
    # 將畫布初始化為全黑圖片
    if canvas is None:
        canvas = np.zeros_like(frame)
        
    # Take the top left of the frame and apply the background subtractor there
    # 取框架的左上角並應用背景分離
    top_left = frame[0: 50, 0: 50]
    fgmask = backgroundobject.apply(top_left)
    
    
    # Note the number of pixels that are white, this is the level of disruption.
    
    switch_thresh = np.sum(fgmask==255)
        
    # If the disruption is greater than background threshold and there has 
    # been some time after the previous switch then you can change the 
    # object type.
    # 如果干擾大於背景閾值，且離上一次切換之後已有段時間，則可切換功能
    if switch_thresh>background_threshold and (time.time()-last_switch) > 1:

        # Save the time of the switch. 
        last_switch = time.time()
        
        if switch == 'Pen':
            switch = 'Eraser'
        else:
            switch = 'Pen'
    
            
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # If you're reading from memory then load the upper and lower ranges 
    # from there
    # 定義顏色範圍
    if load_from_disk:
#             lower_range = blue[0]
#             upper_range = blue[1]
#             lower_range = red[0]
#             upper_range = red[1]
            lower_range = yellow[0]
            upper_range = yellow[1]
        

    # 從HSV圖像中擷取藍色，黃色即獲得相應的遮罩
    # cv2.inRange()函數則是只顯示遮罩範圍內的顏色
    mask = cv2.inRange(hsv, lower_range, upper_range)
    
    # Perform morphological operations to get rid of the noise
    # 執行形態學運算以消除雜訊
    mask = cv2.erode(mask,kernel,iterations = 1)
    mask = cv2.dilate(mask,kernel,iterations = 2)
    
    # Find Contours
    # 找到物件邊緣
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, 
    cv2.CHAIN_APPROX_SIMPLE)
    
    # Make sure there is a contour present and also it size is bigger than 
    # noise threshold.
    if contours and cv2.contourArea(max(contours, key = cv2.contourArea)) > noiseth:
                
        c = max(contours, key = cv2.contourArea)    
        x2,y2,w,h = cv2.boundingRect(c)
        
        # Get the area of the contour
        # 取得輪廓範圍
        area = cv2.contourArea(c)

        # If there were no previous points then save the detected x2,y2 
        # coordinates as x1,y1. 
        # 如果沒有先前的座標點，則將偵測到的x2,y2坐標另存為x1,y1。
        if x1 == 0 and y1 == 0:
            x1,y1= x2,y2
        
        else:

            if switch == 'Pen':
                # Draw the line on the canvas
                # 畫筆顏色粗細
                    canvas = cv2.line(canvas, (x1,y1),
                    (x2,y2), pen_color, 5)
                
            else:
                # 橡皮擦大小
                cv2.circle(canvas, (x2, y2), 20,
                (0,0,0), -1)
            
        
        # After the line is drawn the new points become the previous points.
        x1,y1 = x2,y2
        
        # Now if the area is greater than the wiper threshold then set the 
        # clear variable to True
        
        if area > wiper_thresh:
            cv2.putText(canvas,'Cleaning Screen!',(50,250), 
            cv2.FONT_HERSHEY_SIMPLEX, 2, (150,0,255), 3, cv2.LINE_AA)
            clear = True 

    else:
        # If there were no contours detected then make x1,y1 = 0
        x1,y1 = 0,0
    
   
    # Now this piece of code is just for smooth drawing. (Optional)
    _ , mask = cv2.threshold(cv2.cvtColor (canvas, cv2.COLOR_BGR2GRAY), 20, 
    255, cv2.THRESH_BINARY)
    foreground = cv2.bitwise_and(canvas, canvas, mask = mask)
    background = cv2.bitwise_and(frame, frame,
    mask = cv2.bitwise_not(mask))
    frame = cv2.add(foreground,background)

    # Switch the images depending upon what we're using, pen or eraser.
    # 依照現在使用的功能切換左上角圖示
    if switch != 'Pen':
        cv2.circle(frame, (x1, y1), 20, (255,255,255), -1)
        frame[0: 60, 0: 60] = eraser_img
    else:
        frame[0: 60, 0: 60] = pen_img

    
    cv2.imshow('image',frame)

    k = cv2.waitKey(5) & 0xFF
    # 按Esc結束程式
    if k == 27:
        break
    
    # 按s鍵將所繪線條存成.png檔
    elif k == ord('s'):
        cv2.imwrite("./img/screenshot"+ strftime("%m%d_%H%M%S")+ ".png", canvas, [int(cv2.IMWRITE_PNG_COMPRESSION), 5])

    # 顏色切換
    elif k == ord('x'):
        pen_color = (0,0,255) # 紅色
        
    elif k == ord('c'):
        pen_color = (0,255,0) # 綠色
        
    elif k == ord('v'):
        pen_color = (0,255,255) # 黃色
        
    elif k == ord('b'):
        pen_color = (255,0,0) # 藍色
    
    elif k == ord('z'):
        pen_color = None
        
    
    # Clear the canvas after 1 second, if the clear variable is true
    if clear == True: 
        time.sleep(1)
        canvas = None
        
        # And then set clear to false
        clear = False   

cv2.destroyAllWindows()
cap.release()