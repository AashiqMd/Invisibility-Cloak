import cv2 as cv
import numpy as np
import time
import argparse

#To make a suer friendly command line interface
parser = argparse.ArgumentParser()

parser.add_argument("--video",help = "Path to input video file. Skip this argument to capture frames from the camera")
args = parser.parse_args()

print ("-----------------INVISIBILITY TIME----------------------")

#Taking the input from argument video if it exists or the main camera.
cap = cv.VideoCapture(args.video if args.video else 0)      

#suspend execution for 3 seconds. Time given for camera warm up
time.sleep(3)                                               
count = 0
background = 0

"""
s, img = cap.read()
if s:    # frame captured without any errors
    cv.namedWindow("cam-test")
    cv.imshow("cam-test",img)
    cv.waitKey(0)
    cv.destroyWindow("cam-test")
    cv.imwrite("blue_towel.jpg",img)
"""

#Capturing and storing the background static frame
for i in range(60):
    ret,background = cap.read()

background = np.flip(background,axis=1)

while(cap.isOpened()):
    ret,img = cap.read()
    if not ret:
        break
    count+=1
    img = np.flip(img,axis=1)

    #Converting from BGR color space to HSV color space
    hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)

    #Generating a mask to detect red color
    lower_blue = np.array([100,80,40])
    upper_blue = np.array([140,255,150])
    mask1 = cv.inRange(hsv,lower_blue,upper_blue)
    """
    #OpenCV uses H value ranging from 0 to 180 instead of 360 to fit a 8 bit value
    #Red is between 0 to 30 and 150 to 180
    lower_red = np.array([173,200,70])
    upper_red = np.array([180,255,255])
    mask2 = cv.inRange(hsv,lower_red,upper_red)

    #OR operation on both masks
    mask1 = mask1+mask2
    """
    #Refining the mask corresponding to the detected red color
    mask1 = cv.morphologyEx(mask1,cv.MORPH_OPEN,np.ones((3,3),np.uint8),iterations=2)
    mask1 = cv.dilate(mask1,np.ones((3,3),np.uint8),iterations=2)
    mask2 = cv.bitwise_not(mask1)


    #Generating the final output
    res1 = cv.bitwise_and(img,img,mask=mask2)
    res2 = cv.bitwise_and(background,background,mask=mask1)
    final = cv.addWeighted(res1,1,res2,1,0)

    cv.imshow('image',final)
    k = cv.waitKey(1)
    if k == ord('q'):
        break
    elif k == ord('c'):
        cv.imwrite("black_hair.jpg",img)

cv.destroyAllWindows()
