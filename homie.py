import speech_recognition as sr 
import os
import pyowm
from lxml import html
import requests
import time
from datetime import datetime
import glob
import random
import RPi.GPIO as GPIO
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart



def cleanup():
	GPIO.cleanup()

def dont_move():
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7,GPIO.OUT)
        GPIO.setup(11,GPIO.OUT)
        GPIO.setup(13,GPIO.OUT)
        GPIO.setup(15,GPIO.OUT)
        GPIO.output(7,False)
        GPIO.output(11,False)
        GPIO.output(13,False)
        GPIO.output(15,False)

# how much to rotate
dont_move()
rotate_time = 0.18
#rotate_time_3 = 0.650
#rotate_time_2 = 0.465
#rotate_time = 
min_move_front_distance = 10
move_forward_time = 0.33


# times for various movements
#rotate_time = 0.1
move_backward_time = 0.5
#move_forward_time = 0.5


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

def input_speech(c):
		#while True:
		print "trying to listen"
		with sr.Microphone(device_index=device_id, sample_rate = sample_rate, chunk_size=chunk_size) as source:
			r.adjust_for_ambient_noise(source)
			print "okay say something"
			if c==0:
				os.system('./speech.sh ' + "What can I do for you?")
			if c==1:
       				os.system('./speech.sh ' + "What would be the subject of your email?")
			if c==2:
				os.system('./speech.sh ' + "Who would you like to send the email to? Please spell out the email address")
			if c==3:
	 			os.system('./speech.sh ' + "What would you like the content of your mail to have?")
			if c==4:
				os.system('./speech.sh ' + "could you please repeat that?")
			audio=r.listen(source)
			# print "sup"
		try:
			text=r.recognize_google(audio)
			print text
			
		except sr.UnknownValueError:
			text = input_speech(4)
		
		return text
		#text = r.recognize_google(audio)

def weather():
	owm = pyowm.OWM('8e47cb932d1448c4049c3506aca77f87')
        os.system('./speech.sh ' + "What would be the subject of your email?")
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
		k=0
		for i in news:
			print i
			os.system('./speech.sh ' + i)
			k+=1
			if k==3:
				break


def current_time():
	d=str(datetime.now().time())
	d=d[:5]
	d=datetime.strptime(d, "%H:%M")
	d=d.strftime("%I:%M %p")
	os.system('./speech.sh ' + d)

def joke():
	L=["I cannot believe I got fired from the calendar factory. All I did was take a day off.", "Why did the scientist install a knocker on his door? He wanted to win the No-bell prize", "A neutron walks into a bar and asks, 'How much for a beer?' The bartender replies, 'For you? No charge'", "It is so cold outside I saw a politician with his hands in his own pockets", "After many years of studying at a university, I have finally become a PhD or Pizza Hut Delivery man as people call it."]
	i=random.randrange(0,len(L))
	os.system('./speech.sh ' + L[i])

def SendMail(ImgFileName,objectName):
	print "entered mail  funcciton"
        img_data = open('./screenshots/'+ImgFileName, 'rb').read()
	msg = MIMEMultipart()
	msg['Subject'] = "Here is the location of your object!"
	msg['From'] = 'scrypting101@gmail.com'
	msg['To'] = 'yashitmaheshwary@gmail.com'

	text = MIMEText("View the image to know where your "+objectName + " is")
	msg.attach(text)
	image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
	msg.attach(image)

	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.ehlo()
	s.starttls()
	s.ehlo()
	s.login('scrypting101@gmail.com', 'dkismean*')
	s.sendmail(msg['From'], msg['To'], msg.as_string())
	s.quit()
	os.system('./speech.sh ' + "The location of your "+objectName+" has been mailed to you.") 

def mailer():
	msg = MIMEMultipart()
	#os.system('./speech.sh ' + "What would be the subject of your email?") 
	sub = input_speech(1)
	#os.system('./speech.sh ' + "Who would you like to send the email to? Please spell out the email address")
	add = input_speech(2)
	add = add.replace(" ","")
	dot = "dot"
	at = "at"
	iiit = "iit"
	
	if dot in add:
		add=add.replace(dot,".")
	if at in add:
		add = add.replace(at, "@")
	if iiit in add:
		add = add[:add.find("@")+1] + "iiitd.ac.in"
	add=add.lower()
	print add
	#os.system('./speech.sh ' + "What would you like the content of your mail to have?")
	t = input_speech(3)
	msg['Subject'] = sub
	msg['From'] = "scrypting101@gmail.com"
	msg['To'] = add
	text = MIMEText(t)
	print text
	#msg.attach(text)
	#s = smtplib.SMTP('smtp.gmail.com', 587)
	#s.ehlo()
	#s.starttls()
	#s.ehlo()
	#s.login('scrypting101@gmail.com', 'dkismean*')
	#s.sendmail(msg['From'], msg['To'], msg.as_string())
	os.system("./speech.sh " + "The email has been sent")
	#s.quit()

def trackObject(imgname, matchthresh):
	import numpy as np
	import cv2
	listOfMatches = []
	ESC=27   
	camera = cv2.VideoCapture(0)
	#orb = cv2.ORB()
	orb = cv2.ORB_create()
	bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

	imgTrainColor = cv2.imread(imgname)
	imgTrainGray = cv2.cvtColor(imgTrainColor, cv2.COLOR_BGR2GRAY)

	kpTrain = orb.detect(imgTrainGray,None)
	kpTrain, desTrain = orb.compute(imgTrainGray, kpTrain)

	firsttime=True
	counter = 0
	while (camera.isOpened()):
		ret, imgCamColor = camera.read()
		if ret:
			imgCamGray = cv2.cvtColor(imgCamColor, cv2.COLOR_BGR2GRAY)
			kpCam = orb.detect(imgCamGray,None)
			kpCam, desCam = orb.compute(imgCamGray, kpCam)
			matches = bf.match(desCam,desTrain)
			dist = [m.distance for m in matches]
			try:
				thres_dist = (sum(dist) / len(dist)) * 0.5
			except ZeroDivisionError:
				thres_dist = (sum(dist) *0.5)
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

			#cv2.imshow('Camara', result)
			
			key = cv2.waitKey(20)
			if key == ESC:
				break
			if len(matches) > matchthresh or counter > 60: # or wait 3 seconds
				if counter > 60:
					return False, listOfMatches
				cv2.destroyAllWindows()
				camera.release()
				return True, listOfMatches
			counter+=1
			listOfMatches.append(len(matches))
			#print len(matches)
	cv2.destroyAllWindows()
	camera.release()

def voiceInput(inputString):	
	listObj = {'bottle':9, 'book':10, 'cube':8, 'mug':5, 'perfume':6, 'mouse':5, 'yoghurt':7}
	flag = 0
	objectToFind = ""
	if "botal" in inputString or "portal" in inputString:
		objectToFind = "bottle"
		objectThreshold = listObj[objectToFind]
	elif "buk" in inputString:
		objectToFind = "book"
		objectThreshold = listObj[objectToFind]

	elif "cute" in inputString:
		objectToFind = "cube"
		objectThreshold = listObj[objectToFind]

	elif "mum" in inputString or "cup" in inputString or "class" in inputString:
		objectToFind = "mug"
		objectThreshold = listObj[objectToFind]
 
	elif "deodorant" in inputString:
		objectToFind = "perfume"
		objectThreshold = listObj[objectToFind]

	elif "house" in inputString or "maus" in inputString:
		objectToFind = "mouse"
		objectThreshold = listObj[objectToFind]

	elif "yoga" in inputString or "yoghurt" in inputString or "yogurt" in inputString or "yogart" in inputString:
		objectToFind = "yoghurt"
		objectThreshold = listObj[objectToFind]
	else:
		for i in listObj:
			if i in inputString:
				objectToFind = i
				objectThreshold = listObj[i]
				break
	if objectToFind != "":
		img_files=glob.glob('./database/'+objectToFind+'/*')
		flag = 0
		count = 0
		x=10
		k=0
		flag2=0
		flag3=0
		left_flag=0
		middle_flag=0
		right_flag=0
		mount=[]
		rightmidcount=0
		flag69=0
		while True: 
			count=0
			for i in img_files:
				print "[+] Trying image " + i
				ret, b = trackObject(i,objectThreshold)
				if left_flag==2:
					flag69=1
				if ret == True:
					print "Found " + objectToFind
					#move_down()
					time.sleep(move_backward_time)
					dont_move()
					try:
						os.system('./speech.sh ' + "found " + objectToFind) 
					except sr.UnknownValueError:
						print("[-] Error")
					except sr.RequestError as e:
						print "[-] Error"
					flag = 1
					cleanup()
					os.system("mkdir screenshots")
					os.system("fswebcam ./screenshots/" + objectToFind + ".jpg")
					SendMail(objectToFind+".jpg",objectToFind)
					os.system("rm -rf ./screenshots")
					break
				else:
					for matches in b:
						if matches >= 2:
							count += 1
					print 'count is '+str(count)
					if flag2==0:
						mount.append(count)
						k+=1
					if k==x:
						flag2=1
					if flag2==1 and flag3==0:
						
						print 'moving left to position with max count'
						print 'direction is:  ' + str(mount.index(max(mount)))
						for i in range(mount.index(max(mount))):
							move_left()	
							time.sleep(rotate_time)
							dont_move()
							time.sleep(0.2)
						flag3=1

					if count < 14 and flag69==1 and flag2==1: #after we come to the position directed towards object, move left, then middle then right
						move_right()
						print 'right'
						time.sleep(rotate_time/2)
						dont_move()
						
							#voiceInput(objectToFind)
					elif count > 14 and findDistance > 14 and flag2==1:
						move_up()
						print 'moving forward'
						time.sleep(move_forward_time)
						dont_move()
						#voiceInput(objectToFind)
					elif flag2==0:
					        if count < 10:    
                               				 os.system("./speech.sh " + "Not there!")
                            			else:
                               				 os.system("./speech.sh " + "Maybe it is in that direction")
                       				move_left()
						print 'moving left to search for max count'
			
                                                
                        			time.sleep(rotate_time)
						dont_move()
					"""
                                        try:
						os.system('./speech.sh ' + "lol hogaya") 
					except sr.UnknownValueError:
						print("[-] Error")
					except sr.RequestError as e:
						print "[-] Error"	
                                        """			
                        if(flag == 1):
				cleanup()
				break
	else:
		cleanup()
		try:
			os.system('./speech.sh ' + "Object not in Database") 
		except sr.UnknownValueError:
			print("[-] Error")
		except sr.RequestError as e:
			print "[-] Error"

def determine(ans):
	option1="news"
	option2="weather"
	option3="time"
	option4 ="find"
	option5="where"
	option6="joke"
	option7="move"
	option8="email"
	option9="mail"
	option10="male"
	
	if option1 in ans:
		news_for_today()
	elif option2 in ans:
		weather()
	elif option3 in ans:
		current_time()
	elif option4 in ans or option5 in ans:
		voiceInput(ans)
	elif option6 in ans:
		joke()
	elif option6 in ans:
		move()
	elif option8 in ans or option9 in ans or option10 in ans:
		mailer()
	else:
		determine(input_speech(4))


def findDistance():
	import time
	import curses
	import RPi.GPIO as GPIO
	GPIO.setmode(GPIO.BOARD)

	TRIG = 16
	ECHO = 18
	print ("[+] Distance Measurement in Progress")

	GPIO.setup(TRIG, GPIO.OUT)
	GPIO.setup(ECHO, GPIO.IN)

	GPIO.output(TRIG, False)
	print ("[+] Waiting for sensor to settle")
	time.sleep(0.5)

	GPIO.output(TRIG, True)
	time.sleep(0.00001)
	GPIO.output(TRIG, False)

	while GPIO.input(ECHO)==0:
		pulse_start = time.time()

	while GPIO.input(ECHO)==1:
		pulse_end = time.time()

	pulse_duration = pulse_end - pulse_start

	distance = pulse_duration * 17150

	ditance = round(distance, 2)

	print ("Distance:", distance, "cm") # The final distance
	GPIO.cleanup()
	return distance

def move_left():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(7,GPIO.OUT)	
	GPIO.setup(11,GPIO.OUT)
	GPIO.setup(13,GPIO.OUT)
	GPIO.setup(15,GPIO.OUT)
	GPIO.output(7,True)
	GPIO.output(11,False)
	GPIO.output(13,True)
	GPIO.output(15,False)

def move_right():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(7,GPIO.OUT)	
	GPIO.setup(11,GPIO.OUT)
	GPIO.setup(13,GPIO.OUT)
	GPIO.setup(15,GPIO.OUT)						
	GPIO.output(7,False)
	GPIO.output(11,True)
	GPIO.output(13,False)
	GPIO.output(15,True)

def move_up():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(7,GPIO.OUT)	
	GPIO.setup(11,GPIO.OUT)
	GPIO.setup(13,GPIO.OUT)
	GPIO.setup(15,GPIO.OUT)
	GPIO.output(7,True)
	GPIO.output(11,False)
	GPIO.output(13,False)
	GPIO.output(15,True)

def move_down():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(7,GPIO.OUT)	
	GPIO.setup(11,GPIO.OUT)
	GPIO.setup(13,GPIO.OUT)
	GPIO.setup(15,GPIO.OUT)
	GPIO.output(7,False)
	GPIO.output(11,True)
	GPIO.output(13,True)
	GPIO.output(15,False)

def dont_move():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(7,GPIO.OUT)	
	GPIO.setup(11,GPIO.OUT)
	GPIO.setup(13,GPIO.OUT)
	GPIO.setup(15,GPIO.OUT)
	GPIO.output(7,False)
	GPIO.output(11,False)
	GPIO.output(13,False)
	GPIO.output(15,False)

if __name__ == "__main__":
	while True:
		#os.system("./speech.sh " + "What can I do for you? ")
		#print "hello"
		ans = input_speech(0)
		L=['No','no','nope','Nope','Nothing','nothing']
		for i in L:
			if i in ans:
				os.system("./speech.sh " + "Okay I will go to sleep then")
				exit()
		print ans
		determine(ans.lower())
			#os.system(".hat!")

	
	#for i in range(3):
	#	move_right()
	#	time.sleep(rotate_time/2)
	#	dont_move()
	#	time.sleep(0.5)
	
