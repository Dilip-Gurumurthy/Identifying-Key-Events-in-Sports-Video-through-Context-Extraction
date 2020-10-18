#gets the bottom 20% of the screen automatically + find contours + print
import cv2
import datetime
import re
import numpy as np
import pytesseract
import Image
import imutils
import csv
from PIL import Image
from matplotlib import pyplot as plt

wrt = csv.writer(open("Filename.csv", "wb"))#Change file name to Match-name inn 1 or inn 2
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_eight(x):
	global nxt8
	global nxt3 
	if x == 3:
		nxt8 = 1 
		#print ("nxt = {}".format(nxt8))
	if x >= 4 and x < 8: 
		nxt3 = 1
		#print ("nxt = {}".format(nxt8))
	
	if x == 3 and nxt8 == 1 and nxt3 ==1:
		#print ("nxt = {}".format(nxt8))
		nxt8 = 0
		nxt3 = 0
		return True
	elif x >= 8 or x < 3:
		nxt8 = 0
		nxt3 = 0
		return False
	else:
		#print ("nxt = {}".format(nxt8)) 
		return False	

def is_eight1(x):
	global nxt18
	global nxt13 
	if x == 3:
		nxt18 = 1 
		#print ("nxt = {}".format(nxt8))
	if x >= 4 and x < 8: 
		nxt13 = 1
		#print ("nxt = {}".format(nxt8))
	
	if x == 3 and nxt18 == 1 and nxt13 ==1:
		#print ("nxt = {}".format(nxt8))
		nxt18 = 0
		nxt13 = 0
		return True
	elif x >= 8 or x < 3:
		nxt18 = 0
		nxt13 = 0
		return False
	else:
		#print ("nxt = {}".format(nxt8)) 
		return False

def is_eight2(x):
	global nxt28
	global nxt23 
	if x == 3:
		nxt28 = 1 
		#print ("nxt = {}".format(nxt8))
	if x >= 4 and x < 8: 
		nxt23 = 1
		#print ("nxt = {}".format(nxt8))
	
	if x == 3 and nxt28 == 1 and nxt23 ==1:
		#print ("nxt = {}".format(nxt8))
		nxt28 = 0
		nxt23 = 0
		return True
	elif x >= 8 or x < 3:
		nxt28 = 0
		nxt23 = 0
		return False
	else:
		#print ("nxt = {}".format(nxt8)) 
		return False	




scorexycount = 0
scoreprev = 0
wickets = 0
fps = 25
nxt8 = 0
nxt3 = 0
nxt18 = 0
nxt13 = 0
nxt28 = 0
nxt23 = 0

vid = cv2.VideoCapture('Video')# insert video name
framecount = 0
while(vid.isOpened()):
	(grabbed, frame) = vid.read()
	#crop = frame[645:685, 70:1215]#score
	#width, height = frame.size
	width = vid.get(3)
	height = vid.get(4)
	bot25 = (height*15)/100
	nheight = height - bot25
	crop = frame[nheight:height, 0:width]#score
	#print("{}X{}".format(vid.get(3),vid.get(4)))
	if not grabbed:
		break
	framecount = framecount+1

	if framecount%1==0:
		
		gray = cv2.cvtColor(crop,cv2.COLOR_BGR2GRAY) #these are working
		
		edges = cv2.Canny(gray,100,200)
		kernel = np.ones((2,2),np.uint8)
		#kernel2 = np.ones((1,1),np.uint8)
		dilation = cv2.dilate(edges,kernel,iterations = 2)
		
		_,contours, hierarchy = cv2.findContours(dilation,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) 

		for contour in contours:
   
			[x,y,w,h] = cv2.boundingRect(contour)
			if h<100 and w<100:
				if h>15 and w>25:
					cv2.rectangle(crop,(x,y),(x+w,y+h),(0,0,255),2)
					minicrop = crop[y:y+h, x:x+w]
					cv2.imwrite("tester2.jpg",minicrop)
		
					# Extracting data from image
					varnum= pytesseract.image_to_string(Image.open('tester2.jpg'))
					varnum= varnum.replace(" ", "")
		
					# Extracting the score
					scorepattern = re.compile(r'\d-\d|\d{2}-\d|\d{3}-\d|\d{3}-\d{2}|\d{2}-\d{2}')
					sm = scorepattern.search(varnum)
					
					if sm != None:
						#print varnum
						if varnum[1] == '-' or varnum[1] == '.':

							if is_number(varnum[2]):
								wicketpres = int(varnum[2])
								if wicketpres >= wickets and wicketpres == wickets+1:
									wickets = wicketpres
									if is_number(varnum[0]):
										scorepres = int(varnum[0])
										if is_eight(scorepres):
											scorepres = 8
											nxt8 = 0
											nxt3 = 0
							
									if scorepres >= scoreprev and scorepres < scoreprev + 7:
										scoreprev = scorepres
										vidtime = str(datetime.timedelta(seconds=framecount/fps))
										print("{}-{} frame number = {} time = {}".format(scoreprev,wickets,framecount,vidtime))
				
							if is_number(varnum[0]):
								scorepres = int(varnum[0])
								if is_eight(scorepres):
									scorepres = 8
									nxt8 = 0
									nxt3 = 0
								if scorepres >= scoreprev and scorepres < scoreprev + 7:
									scoreprev = scorepres
									vidtime = str(datetime.timedelta(seconds=framecount/fps))
									print("{}-{} frame number = {} time = {}".format(scoreprev,wickets,framecount,vidtime))
									scorexycount= scorexycount + 1
									if scorexycount >= 10:
										cv2.imshow('score area', minicrop)
										scorey = y
										scoreh = h - 2
										scorex = x
										scorew = w - 1
										break
	
	#cv2.imshow('frame2',crop)
	if scorexycount >= 10:
		vid.release()
		break

#cv2.imshow('score area', minicrop)
#if cv2.waitKey(1) & 0xFF == ord('q'):
	#break
#cv2.waitKey(0)
#vid.release()
#cv2.destroyAllWindows()

vid = cv2.VideoCapture('video')#Change to first inn or second inn clip's name
framecount = 0
scoreprev = 0
wickets = 0
fps = 25
nxt8 = 0
nxt3 = 0
nxt18 = 0
nxt13 = 0
nxt28 = 0
nxt23 = 0
while(vid.isOpened()):
	(grabbed, frame) = vid.read()
	if not grabbed:
		break
	width = vid.get(3)
	height = vid.get(4)
	bot25 = (height*15)/100
	nheight = height - bot25
	crop = frame[nheight:height, 0:width]
	
	framecount = framecount+1

	if framecount%10==0:

		#crop = frame[312:332, 44:161]#team+score
		#crop = frame[312:332, 44:90]#team name
		scorecrop = crop[scorey:scorey+scoreh, scorex:scorex+scorew]#score
		
	    	#gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
		#ret,th = cv2.threshold(gray,100,225,cv2.THRESH_BINARY)
		#th1 = imutils.resize(th, width=500)
		#th2 = cv2.medianBlur(th1,5)		
		cv2.imwrite("tester3.jpg",scorecrop)
		
		# Extracting data from image
		varnum= pytesseract.image_to_string(Image.open('tester3.jpg'))
		
		# Extracting the score
		scorepattern = re.compile(r'\d-\d|\d{2}-\d|\d{3}-\d|\d{3}-\d{2}|\d{2}-\d{2}')
		sm = scorepattern.search(varnum)

		if sm != None:
			#print varnum
			if varnum[1] == '-':

				if is_number(varnum[2]):
					wicketpres = int(varnum[2])
					if wicketpres >= wickets and wicketpres == wickets+1:
						wickets = wicketpres
						if is_number(varnum[0]):
							scorepres = int(varnum[0])
							if is_eight(scorepres):
								scorepres = 8
								nxt8 = 0
								nxt3 = 0
							
						if scorepres >= scoreprev and scorepres < scoreprev + 7:
							scoreprev = scorepres
							vidtime = str(datetime.timedelta(seconds=framecount/fps))
							wrt.writerow((scoreprev,wickets,framecount,vidtime))
							print("{}-{} frame number = {} time = {}".format(scoreprev,wickets,framecount,vidtime))
				
				if is_number(varnum[0]):
					scorepres = int(varnum[0])
					if is_eight(scorepres):
						scorepres = 8
						nxt8 = 0
						nxt3 = 0
					if scorepres > scoreprev and scorepres < scoreprev + 7:
						scoreprev = scorepres
						vidtime = str(datetime.timedelta(seconds=framecount/fps))
						wrt.writerow((scoreprev,wickets,framecount,vidtime))
						print("{}-{} frame number = {} time = {}".format(scoreprev,wickets,framecount,vidtime))
						
						

			elif varnum[2] == '-':
				if is_number(varnum[3]):
					wicketpres = int(varnum[3])
					if wicketpres >= wickets and wicketpres == wickets+1:
						wickets = wicketpres
						if is_number(varnum[0]) and is_number(varnum[1]):
							scorepres1 = int(varnum[0])
							if is_eight(scorepres1):
								scorepres1 = 8
								nxt8 = 0
								nxt3 = 0
							scorepres2 = int(varnum[1])
							if is_eight1(scorepres2):
								scorepres2 = 8
								nxt18 = 0
								nxt13 = 0
							scorepres = (scorepres1*10) + scorepres2 
							if scorepres >= scoreprev and scorepres < scoreprev + 7:
								scoreprev = scorepres
								vidtime = str(datetime.timedelta(seconds=framecount/fps))
								wrt.writerow((scoreprev,wickets,framecount,vidtime))
								print("{}-{} frame number = {} time = {}".format(scoreprev,wickets,framecount,vidtime))

				if is_number(varnum[0]) and is_number(varnum[1]):
					scorepres1 = int(varnum[0])
					if is_eight(scorepres1):
						scorepres1 = 8
						nxt8 = 0
						nxt3 = 0
					scorepres2 = int(varnum[1])
					if is_eight1(scorepres2):
						scorepres2 = 8
						nxt18 = 0
						nxt13 = 0
					scorepres = (scorepres1*10) + scorepres2 
					if scorepres > scoreprev and scorepres < scoreprev + 7:
						scoreprev = scorepres
						vidtime = str(datetime.timedelta(seconds=framecount/fps))
						wrt.writerow((scoreprev,wickets,framecount,vidtime))
						print("{}-{} frame number = {} time = {}".format(scoreprev,wickets,framecount,vidtime))

			elif varnum[3] == '-' or varnum[3] == ' ':
				if is_number(varnum[4]):
					wicketpres = int(varnum[4])
					if wicketpres >= wickets and wicketpres == wickets+1:
						wickets = wicketpres
						if is_number(varnum[0]) and is_number(varnum[1]) and is_number(varnum[2]):
							scorepres1 = int(varnum[0])
							if is_eight(scorepres1):
								scorepres1 = 8
								nxt8 = 0
								nxt3 = 0
							scorepres2 = int(varnum[1])
							if is_eight1(scorepres2):
								scorepres2 = 8
								nxt18 = 0
								nxt13 = 0
							scorepres3 = int(varnum[2])
							if is_eight2(scorepres3):
								scorepres3 = 8
								nxt28 = 0
								nxt23 = 0
							
							scorepres = (scorepres1*100) + (scorepres2*10) + scorepres3   
							if scorepres >= scoreprev and scorepres < scoreprev + 7:
								scoreprev = scorepres
								vidtime = str(datetime.timedelta(seconds=framecount/fps))
								wrt.writerow((scoreprev,wickets,framecount,vidtime))
								print("{}-{} frame number = {} time = {}".format(scoreprev,wickets,framecount,vidtime))

				if is_number(varnum[0]) and is_number(varnum[1]) and is_number(varnum[2]):
					scorepres1 = int(varnum[0])
					if is_eight(scorepres1):
						scorepres1 = 8
						nxt8 = 0
						nxt3 = 0
					scorepres2 = int(varnum[1])
					if is_eight1(scorepres2):
						scorepres2 = 8
						nxt18 = 0
						nxt13 = 0
					scorepres3 = int(varnum[2])
					if is_eight2(scorepres3):
						scorepres3 = 8
						nxt28 = 0
						nxt23 = 0
					scorepres = (scorepres1*100) + (scorepres2*10) + scorepres3   
					if scorepres > scoreprev and scorepres < scoreprev + 7:
						scoreprev = scorepres
						vidtime = str(datetime.timedelta(seconds=framecount/fps))
						wrt.writerow((scoreprev,wickets,framecount,vidtime))
						print("{}-{} frame number = {} time = {}".format(scoreprev,wickets,framecount,vidtime))
						

				
		

	    	#cv2.imshow('frame',th2)
		#cv2.imshow('frame2',scorecrop)

	    	if cv2.waitKey(1) & 0xFF == ord('q'):
			break

vid.release()
cv2.destroyAllWindows()


