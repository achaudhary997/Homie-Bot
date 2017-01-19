"""
Created on Sun Aug 21 09:14:58 2016

@author: Yashit
"""
import numpy as np
import argparse
import glob
import cv2
import time

def autoCanny(image, sigma=0.23):
	v = np.median(image)
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower,  upper)
	return edged

def cannyOut(img):
	g_img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	b_img=cv2.GaussianBlur(g_img, (3, 3), 0)
	auto=autoCanny(b_img)
	return auto

cap = cv2.VideoCapture(0)

while(True):
	ret, frame = cap.read()

	time.sleep(0.1)
	frameNew = cannyOut(frame)
	cv2.imshow('frame',frameNew)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()