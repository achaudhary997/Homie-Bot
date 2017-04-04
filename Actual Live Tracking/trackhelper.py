import track
import time
import glob
import speech_recognition as sr 
import os

r=sr.Recognizer()

with sr.Microphone() as source:
	os.system("./speech.sh Say Something")
	audio=r.listen(source)

inputString = r.recognize_google(audio)
inputString = inputString.lower()
listObj = {'bottle':11, 'book':11, 'cube':8, 'mug':5, 'perfume':6, 'mouse':6}
flag = 0
objectToFind = ""
if "botal" in inputString or "portal" in inputStrings:
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
			ret = track.trackObject(i,objectThreshold)
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
