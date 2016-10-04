# import the necessary packages
#from picamera.array import PiRGBArray
#from picamera import PiCamera
#import time
import cv2
import numpy as np

BLUR=(5,5)
threshold=0
#Set the BGR color thresholds
THRESH_TXT=["Blue","Green","Red","Magenta","Yellow"]
THRESH_LOW=[[80,40,0],[40,80,0],[40,0,80],[80,0,80],[0,80,80]]
THRESH_HI=[[220,100,80],[100,220,80],[100,80,220],[220,80,220],[80,220,220]]

def process_image(raw_image,control):
        global threshold
        text=[]
        images=[]

        #Switch color threshold
        if control == ord("c"):
          threshold=(threshold+1)%len(THRESH_LOW)

        #Keep a copy of the raw image
        text.append("Raw Image %s"%THRESH_TXT[threshold])
        images.append(raw_image)
        #Blur the raw image
        text.append("with Blur...%s"%THRESH_TXT[threshold])
        images.append(cv2.blur(raw_image, BLUR))

        lower = np.array(THRESH_LOW[threshold],dtype="uint8")
        upper = np.array(THRESH_HI[threshold], dtype="uint8")

        text.append("with Threshold...%s"%THRESH_TXT[threshold])
        images.append(cv2.inRange(images[-1], lower, upper))


        # find contours in the threshold image
        text.append("with Contours...%s"%THRESH_TXT[threshold])
        images.append(images[-1].copy())
        image, contours, hierarchy = cv2.findContours(images[-1],
                                                      cv2.RETR_LIST,
                                                      cv2.CHAIN_APPROX_SIMPLE)

        # finding contour with maximum area and store it as best_cnt
        max_area = 0
        best_cnt = 1
        for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > max_area:
                        max_area = area
                        best_cnt = cnt

        # finding centroids of best_cnt and draw a circle there
        M = cv2.moments(best_cnt)
        cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        
        if max_area>0:
          cv2.circle(raw_image,(cx,cy),8,(THRESH_HI[threshold]),-1)
          cv2.circle(raw_image,(cx,cy),4,(THRESH_LOW[threshold]),-1)

        return(images,text)
#End

