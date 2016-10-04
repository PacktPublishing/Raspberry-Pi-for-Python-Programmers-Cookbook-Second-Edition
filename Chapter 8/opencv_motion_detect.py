#import the necessary packages
import cv2
import numpy as np

BLUR=(5,5)
HIBLUR=(30,30)
GAUSSIAN=(21,21)

imageBG=None
gray=True

movement=[]
AVG=2
avgX=0
avgY=0
count=0

def process_image(raw_image,control):
  global imageBG
  global count,avgX,avgY,movement,gray

  text=[]
  images=[]
  reset=False

  #Toggle Gray and reset background
  if control == ord("g"):
    if gray:
      gray=not gray
    reset=True
    print("Toggle Gray")
  #Display contour and hierarchy details
  elif control == ord("i"):
    print("Contour: %s"%contours)
    print("Hierarchy: %s"%hierarchy)
  #Reset the background image
  elif control == ord("r"):
    reset=True
    
  #Clear movement record and reset background
  if reset:
    print("Reset Background")
    imageBG=None
    movement=[]

  #Keep a copy of the raw image
  text.append("Raw Image")
  images.append(raw_image)

  if gray:
    raw_image=cv2.cvtColor(raw_image,cv2.COLOR_BGR2GRAY)

  #Blur the raw image
  text.append("with Gaussian Blur...")
  images.append(cv2.GaussianBlur(raw_image, GAUSSIAN, 0))

  #Initialise background
  if imageBG is None:
    imageBG=images[-1]

  text.append("with image delta...")  
  images.append(cv2.absdiff(imageBG,images[-1]))

  text.append("with threshold mask...")                
  images.append(cv2.threshold(images[-1], 25, 255,
                             cv2.THRESH_BINARY)[1])

  text.append("with dilation...")                
  images.append(cv2.dilate(images[-1],None, iterations=3))
 #text.append("with dilation kernel...")
  #kernel=np.ones((1,1),np.uint8)
  #images.append(cv2.dilate(images[-2],kernel, iterations=3))

  #Find contours
  if not gray:
    #Require gray image to find contours
    text.append("with dilation gray...")
    images.append(cv2.cvtColor(images[-1],cv2.COLOR_BGR2GRAY))
  text.append("with contours...")
  images.append(images[-1].copy())
  aimage, contours, hierarchy = cv2.findContours(images[-1],
                                                 cv2.RETR_LIST,
                                                 cv2.CHAIN_APPROX_SIMPLE)

  #Determine the area of each of the contours
  largest_area=0
  found_contour=None
  for cnt in contours:
    area = cv2.contourArea(cnt)
    #Find which one is largest
    if area > largest_area:
      largest_area=area
      found_contour=cnt


  if found_contour != None:
    #Find the centre of the contour
    M=cv2.moments(found_contour)
    cx,cy=int(M['m10']/M['m00']),int(M['m01']/M['m00'])
    #Calculate the average
    if count<AVG:
      avgX=(avgX+cx)/2
      avgY=(avgY+cy)/2
      count=count+1
    else:
      movement.append((int(avgX),int(avgY)))
      avgX=cx
      avgY=cy
      count=0

  #Display
  if found_contour != None:
    cv2.circle(images[0],(cx,cy),10,(255,255,255),-1)
  if len(movement) > 1:
    for i,j in enumerate(movement):
      if i>1:
        cv2.line(images[0],movement[i-1],movement[i],(255,255,255))
    
  return(images,text)  


#End

