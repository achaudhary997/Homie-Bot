import track
import time
import glob
import speech_recognition as sr 
import os

r=sr.Recognizer()

with sr.Microphone() as source:
	print("say something")
	audio=r.listen(source)

inputString = r.recognize_google(audio)
listObj = {'bottle':11, 'book':11, 'cube':8, 'mug':5, 'perfume':6, 'mouse':6}
flag = 0
objectToFind = ""
for i in listObj:
	if i in inputString:
		objectToFind = i
		objectThreshold = listObj[i]
		break
if objectToFind != "":
	img_files=glob.glob(objectToFind+'/*')
	flag = 0
	flag1 = 0
	count = 0
	while True: 
		for i in img_files:
			start_time = time.time()
			print "[+] Trying image " + i
			ret = track.trackObject(i,objectThreshold)
			if ret == True:
				print "Found " + objectToFind
				try:
					os.system('espeak "' + "found " + objectToFind + '"') 
				except sr.UnknownValueError:
					print("[-] Error")
				except sr.RequestError as e:
					print "[-] Error"
				flag = 1
				break
			else:
				try:
					os.system('espeak "' + "lol hogaya" + '"') 
				xcept sr.UnknownValueError:
					print("[-] Error")
				except sr.RequestError as e:
					print "[-] Error"
		if(flag == 1):
			break

else:
	try:
		os.system('espeak "' + "Object not in Database" + '"') 
	except sr.UnknownValueError:
		print("[-] Error")
	except sr.RequestError as e:
		print "[-] Error"
