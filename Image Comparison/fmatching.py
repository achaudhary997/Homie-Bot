import numpy as np
import cv2
import matplotlib.pyplot as plt
import statistics


def drawMatches(img1, kp1, img2, kp2, matches):

	rows1 = img1.shape[0]
	cols1 = img1.shape[1]
	rows2 = img2.shape[0]
	cols2 = img2.shape[1]

	out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')

	out[:rows1,:cols1] = np.dstack([img1, img1, img1])	
	out[:rows2,cols1:] = np.dstack([img2, img2, img2])
	xcoords=[]
	ycoords=[]
	for mat in matches:


		img1_idx = mat.queryIdx
		img2_idx = mat.trainIdx

	
		(x1,y1) = kp1[img1_idx].pt
		(x2,y2) = kp2[img2_idx].pt
		#print(x1,y1)
		xcoords.append(x1)
		ycoords.append(y1)
		
		cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0), 1)   
		cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)
		cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255, 0, 0), 1)


	
	cv2.imshow('Matched Features', out)
	cv2.waitKey(0)
	cv2.destroyWindow('Matched Features')
	#print(xcoords)
	#print(ycoords)
	sum_of_x = 0
	sum_of_y = 0
	for i in xcoords:
		sum_of_x+=i
	for i in ycoords:
		sum_of_y+=i
	std_dev_x = statistics.pstdev(xcoords)
	std_dev_y = statistics.pstdev(ycoords)
	print(std_dev_x)
	print(std_dev_y)
	print(statistics.mean(xcoords))
	print(statistics.mean(ycoords))
	for i in range(len(xcoords)):
		xcoords[i]=(xcoords[i]-statistics.mean(xcoords))/std_dev_x
	#print(xcoords)
	print(max(xcoords))
	print(min(xcoords))

	return out
img1 = cv2.imread('im3.jpeg',0)		
img2 = cv2.imread('img2.jpg',0) 

orb = cv2.ORB()

(kp1, des1) = orb.detectAndCompute(img1,None)
(kp2, des2)= orb.detectAndCompute(img2,None)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1,des2)
matches = sorted(matches, key = lambda x:x.distance)

img3 = drawMatches(img1,kp1,img2,kp2,matches[:100])
#plt.imshow(img3),plt.show()
