import speech_recognition as sr 
import os
import pyowm
from lxml import html
import requests
import time
from datetime import datetime
import glob

#settings
mic_name = "USB Device 0x46d:0x825: Audio (hw:1,0)"
sample_rate = 48000
chunk_size = 2048

r=sr.Recognizer()

mic_list = sr.Microphone.list_microphone_names()

for i,microphone_name in enumerate(mic_list):
	if microphone_name == mic_name:
		device_id=i
		print microphone_name
		print device_id
def input_speech():
	while True:
		print "trying to listen"
		with sr.Microphone(device_index=device_id, sample_rate = sample_rate, chunk_size=chunk_size) as source:
			r.adjust_for_ambient_noise(source)
			print "okay say something"
			audio=r.listen(source)
			print "sup"
		try:
			text=r.recognize_google(audio)
			print text
			break
		except:
			os.system('./speech.sh ' + "could you please repeat that? I did not quite understand you.")

	#text = r.recognize_google(audio)
	return text

def weather():
	owm = pyowm.OWM('8e47cb932d1448c4049c3506aca77f87')
	os.system("./speech.sh " + "Which place?")
	place = input_speech()
	observation = owm.weather_at_place(place)
	w = observation.get_weather()
	complete_temp = w.get_temperature('celsius') 
	for i in complete_temp:
		if(i=="temp"):
			os.system('./speech.sh ' + "The temperature is " + str(complete_temp[i]) + " Degrees celsius ")

def news_for_today():
	response = requests.get('https://news.google.com/news/section?cf=all&pz=1&topic=b&siidp=b458d5455b7379bd8193a061024cd11baa97&ict=ln')
	if (response.status_code == 200):
		pagehtml = html.fromstring(response.text)
		news = pagehtml.xpath('//h2[@class="esc-lead-article-title"] \
		                      /a/span[@class="titletext"]/text()')
		for i in news:
			os.system('./speech.sh ' + i)



def current_time():
	d=str(datetime.now().time())
	d=d[:5]
	d=datetime.strptime(d, "%H:%M")
	d=d.strftime("%I:%M %p")
	os.system('./speech.sh ' + d)

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

def realvoiceinput(inputString):	
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
		img_files=glob.glob(objectToFind+'database/*')
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

def determine(ans):
	option1a="news"
	option2a="weather"
	option3a="time"
	option4a ="find"
	option4v="where"
	
	if option1a in ans:
		news_for_today()
	elif option2a in ans:
		weather()
	elif option3a in ans:
		current_time()
	elif option4a in ans or option4v in ans:
		realvoiceinput(ans)

#news_for_today()
#current_time()

if __name__ == "__main__":
	os.system("./speech.sh " + "Hey there! Whats up? ")
	print "hello"
	ans = input_speech()
	print ans
	determine(ans.lower())


