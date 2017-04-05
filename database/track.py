import time
import glob
import speech_recognition as sr 
import os

def trackObject(imgname, matchthresh):
	import numpy as np
	import cv2

	ESC=27   
	camera = cv2.VideoCapture(0)
	orb = cv2.ORB()
	#orb = cv2.ORB_create()
	bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

	imgTrainColor=cv2.imread(imgname)
	imgTrainGray = cv2.cvtColor(imgTrainColor, cv2.COLOR_BGR2GRAY)

	kpTrain = orb.detect(imgTrainGray,None)
	kpTrain, desTrain = orb.compute(imgTrainGray, kpTrain)

	firsttime=True
	counter = 0
	while True:
		ret, imgCamColor = camera.read()
		imgCamGray = cv2.cvtColor(imgCamColor, cv2.COLOR_BGR2GRAY)
		kpCam = orb.detect(imgCamGray,None)
		kpCam, desCam = orb.compute(imgCamGray, kpCam)
		matches = bf.match(desCam,desTrain)
		dist = [m.distance for m in matches]
		thres_dist = (sum(dist) / len(dist)) * 0.5
		matches = [m for m in matches if m.distance < thres_dist]   

		if firsttime==True:
			h1, w1 = imgCamColor.shape[:2]
			h2, w2 = imgTrainColor.shape[:2]
			nWidth = w1+w2
			nHeight = max(h1, h2)
			hdif = (h1-h2)/2
			firsttime=False
		result = np.zeros((nHeight, nWidth, 3), np.uint8)
		# print np.size(result)
		result[hdif:hdif+h2, :w2] = imgTrainColor
		result[:h1, w2:w1+w2] = imgCamColor

		for i in range(len(matches)):
			pt_a=(int(kpTrain[matches[i].trainIdx].pt[0]), int(kpTrain[matches[i].trainIdx].pt[1]+hdif))
			pt_b=(int(kpCam[matches[i].queryIdx].pt[0]+w2), int(kpCam[matches[i].queryIdx].pt[1]))
			cv2.line(result, pt_a, pt_b, (255, 0, 0))

		cv2.imshow('Camara', result)
		
		key = cv2.waitKey(20)
		if key == ESC:
			break
		if len(matches) > matchthresh or counter > 100: # or wait 3 seconds
			if counter > 100:
				return False
			cv2.destroyAllWindows()
			camera.release()
			return True
		counter+=1
		#print len(matches)
	cv2.destroyAllWindows()
	camera.release()

r=sr.Recognizer()

with sr.Microphone() as source:
	r.adjust_for_ambient_noise(source)
	os.system("./speech.sh What do you want to find?")
	audio=r.listen(source)


inputString = r.recognize_google(audio)
inputString = inputString.lower()
print inputString
listObj = {'bottle':11, 'book':11, 'cube':8, 'mug':5, 'perfume':6, 'mouse':6}
flag = 0
objectToFind = ""
if "botal" in inputString or "portal" in inputString:
	objectToFind = "bottle"
elif "buk" in inputString:
	objectToFind = "book"
elif "cute" in inputString:
	objectToFind = "cube"
elif "mum" in inputString or "cup" in inputString or "class" in inputString:
	objectToFind = "mug" 
elif "deodorant" in inputString:
	objectToFind = "perfume"
elif "house" in inputString or "maus" in inputString:
	objectToFind = "mouse"
else:
	for i in listObj:
		if i in inputString:
			objectToFind = i
			objectThreshold = listObj[i]
			break
if objectToFind != "":
	img_files=glob.glob(objectToFind+'/*')
	flag = 0
	count = 0
	while True: 
		for i in img_files:
			print "[+] Trying image " + i
			ret = trackObject(i,objectThreshold)
			if ret == True:
				print "Found " + objectToFind
				try:
					os.system('./speech.sh ' + "found " + objectToFind) 
				except sr.UnknownValueError:
					print("[-] Error")
				except sr.RequestError as e:
					print "[-] Error"
				flag = 1
				break
			else:	
				try:
					os.system('./speech.sh ' + "lol hogaya") 
				except sr.UnknownValueError:
					print("[-] Error")
				except sr.RequestError as e:
					print "[-] Error"	
		if(flag == 1):
			break
else:
	try:
		os.system('./speech.sh ' + "Object not in Database") 
	except sr.UnknownValueError:
		print("[-] Error")
	except sr.RequestError as e:
		print "[-] Error"