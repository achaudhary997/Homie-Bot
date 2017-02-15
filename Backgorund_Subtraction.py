# Currently works for red (tested for notebook cover)
# By Anubhav

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #Values below are HSV Values
    lower_red = np.array([100,100,100])
    upper_red = np.array([220,200,255])
    
    #The lines below create the mask over the original image
    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame,frame, mask= mask)

    kernel = np.ones((5,5),np.uint8)
    #erosion = cv2.erode(mask,kernel,iterations = 1)
    #dilation = cv2.dilate(mask,kernel,iterations = 1)

    cv2.imshow('Original',frame)
    cv2.imshow('Mask',mask)
    #cv2.imshow('Erosion',erosion)
    #cv2.imshow('Dilation',dilation)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()