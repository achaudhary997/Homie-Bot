import track
import time
import glob
inputString = "find my perfume"
listObj = {'bottle':11, 'book':11, 'cube':8, 'mug':5, 'perfume':6}
flag = 0
objectToFind = ""
for i in listObj:
	if i in inputString:
		objectToFind = i
		objectThreshold = listObj[i]
		break
print (objectThreshold)
if objectToFind != "":
	img_files=glob.glob(objectToFind+'/*')
	flag = 0
	flag1 = 0
	count = 0
	while True: 
		for i in img_files:
			start_time = time.time()
			print "[*] Trying image " + i
			ret = track.trackObject(i,objectThreshold)
			if ret == True:
				print "Found " + objectToFind
				flag = 1
				break
			else:
				print "Bhadwe"
		if(flag == 1):
			break

else:
	print "Object not in database."
