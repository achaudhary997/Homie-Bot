import track
import time
listObj = ['croppednew.png', 'rubux.png', 'coke.png', 'coke2.png']
listObjThresh = [11, 11, 8, 10]
flag = 0
while True: 
	for i in listObj:
		ret = track.trackObject(i)
		if ret == True:
			print "Found "+i
			flag = 1
			break
		else:
			print "Bhadwe"
	if flag == 1:
		break