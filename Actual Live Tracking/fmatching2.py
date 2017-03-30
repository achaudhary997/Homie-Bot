import numpy as np
import cv2
import math
  
ESC=27   
camera = cv2.VideoCapture(0)
camera2 = camera
orb = cv2.ORB_create()
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

imgTrainColor=cv2.imread('rubux.png')
imgTrainColor2 = cv2.imread('croppednew.png')
imgTrainGray = cv2.cvtColor(imgTrainColor, cv2.COLOR_BGR2GRAY)
imgTrainGray2 = cv2.cvtColor(imgTrainColor2, cv2.COLOR_BGR2GRAY)
kpTrain = orb.detect(imgTrainGray,None)
kpTrain2 = orb.detect(imgTrainGray2, None)
kpTrain, desTrain = orb.compute(imgTrainGray, kpTrain)
kpTrain2, desTrain2 = orb.compute(imgTrainGray2, kpTrain2)
firsttime=True

while True:
   
    ret, imgCamColor = camera.read()
    imgCamGray = cv2.cvtColor(imgCamColor, cv2.COLOR_BGR2GRAY)
    kpCam = orb.detect(imgCamGray,None)
    kpCam, desCam = orb.compute(imgCamGray, kpCam)
    matches = bf.match(desCam,desTrain)
    matches2=bf.match(desCam,desTrain2)
    dist = [m.distance for m in matches]
    dist2 = [m.distance for m in matches2]
    thres_dist = (sum(dist) / len(dist)) * 0.5
    thres_dist2 = (sum(dist2) / len(dist2)) * 0.5
    matches = [m for m in matches if m.distance < thres_dist]
    matches2 = [m for m in matches2 if m.distance < thres_dist2]   

    if firsttime==True:
        h1, w1 = imgCamColor.shape[:2]
        h2, w2 = imgTrainColor.shape[:2]
        h3,w3 = imgTrainColor2.shape[:2]
        nWidth = w1+w2
        nWidth2 = w1 + w3
        nHeight = max(h1, h2)
        nHeight2 = max(h1,h3)
        hdif = ((h1-h2)/2)
        hdif2=((h1-h3)/2)
        firsttime=False
       
    result = np.zeros((nHeight, nWidth, 3), np.uint8)
    result2 = np.zeros((nHeight2, nWidth2,3), np.uint8)
    result[hdif:hdif+h2, :w2] = imgTrainColor
    result2[hdif2:hdif2+h3, : w3] = imgTrainColor2
    result[:h1, w2:w1+w2] = imgCamColor
    result2[:h1, w3:w1+w3] = imgCamColor

    for i in range(len(matches)):
        pt_a=(int(kpTrain[matches[i].trainIdx].pt[0]), int(kpTrain[matches[i].trainIdx].pt[1]+hdif))
        pt_b=(int(kpCam[matches[i].queryIdx].pt[0]+w2), int(kpCam[matches[i].queryIdx].pt[1]))
        cv2.line(result, pt_a, pt_b, (255, 0, 0))

    for i in range(len(matches2)):
        pt_a=(int(kpTrain2[matches2[i].trainIdx].pt[0]), int(kpTrain2[matches2[i].trainIdx].pt[1]+hdif2))
        pt_b=(int(kpCam[matches2[i].queryIdx].pt[0]+w2), int(kpCam[matches2[i].queryIdx].pt[1]))
        cv2.line(result2, pt_a, pt_b, (255, 0, 0))


    cv2.imshow('Camara', result)
    cv2.imshow('Camara', result2)
    key = cv2.waitKey(20)                                 
    if key == ESC:
        break

cv2.destroyAllWindows()
camera.release()