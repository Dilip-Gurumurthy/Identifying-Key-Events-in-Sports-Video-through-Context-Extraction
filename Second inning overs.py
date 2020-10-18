# o.o + from## test 1
import cv2
import datetime
import csv
import re
import numpy as np
import pytesseract
import Image
import imutils
from PIL import Image
from matplotlib import pyplot as plt

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

wrt = csv.writer(open("Filename.csv", "wb"))# Change to match_name_ovrinn2.csv
#8888888888888888888888888888888888888888888888888888888 overs 0.0 init 8888888888888888888888888888888888888888888888888888888888        
scoreprev = 0
ballno = 0
overno = 0
fps = 25
nnull = 0
nnull2 = 0
overno = 0
fcounter = 0
#scounter = 0

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
	crop2 = frame[nheight:height, 0:width]
	#print("{}X{}".format(vid.get(3),vid.get(4)))
	if not grabbed:
		break
	framecount = framecount+1

	if framecount%1==0 and framecount > 3000:
		
		gray = cv2.cvtColor(crop,cv2.COLOR_BGR2GRAY) #these are working
		
		edges = cv2.Canny(gray,100,200)
		kernel = np.ones((2,2),np.uint8)
		#kernel2 = np.ones((1,1),np.uint8)
		dilation = cv2.dilate(edges,kernel,iterations = 2)
		#cv2.imshow('frame3',dilation)
		_,contours, hierarchy = cv2.findContours(dilation,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) 

		for contour in contours:
   
			[x,y,w,h] = cv2.boundingRect(contour)
			#y = y-10
			#x = x-10
			#h = h + 7
			#w = w + 10
			if h<100 and w<100:
				if h>10 and w>15:
					
					cv2.rectangle(crop,(x,y),(x+w,y+h),(0,0,255),2)
					if (y - 10>0) and (x - 10>0) and (h + 10<bot25) and (w + 10<width):
					#cv2.rectangle(crop,(nx,ny),(nx+nw,ny+nh,(0,0,255),2)
						scorey = y-10
						scorex = x-10
						scoreh = h + 15
						scorew = w + 20
					#minicrop = crop2[y:y+h, x:x+w]
					minicrop = crop2[scorey:scorey+scoreh, scorex:scorex+scorew]
					
					gray = cv2.cvtColor(minicrop, cv2.COLOR_BGR2GRAY)
					th1 = imutils.resize(gray, width=800)
					ret,th2 = cv2.threshold(th1,100,225,cv2.THRESH_BINARY)
					ret,th3 = cv2.threshold(th2,127,255,cv2.THRESH_BINARY_INV)
		
					th4 = cv2.medianBlur(th3,9)
					th5 = cv2.bilateralFilter(th4,9,75,75)
					#cv2.imshow('frame3',th5)
					#minicrop = crop[ny:ny+nh, nx:nx+nw]
					cv2.imwrite("tester7.jpg",th5)
		
					# Extracting data from image
					varnum= pytesseract.image_to_string(Image.open('tester7.jpg'))
					varnum= varnum.replace(" ", "")
					stlen = len(varnum)
		
					# Extracting the score
					#overpattern = re.compile(r'OVERS:\d|OVERS:\d.\d|OVERS:\d{2}.\d|OVERS;\d|OVERS;\d.\d|OVERS;\d{2}.\d|OVERS:\d,\d|OVERS:\d{2},\d|OVERS;\d,\d|OVERS;\d{2},\d')
					
					overpattern = re.compile(r'\d|\d.\d|\d{2}.\d|\d,\d|\d{2},\d')
					om = overpattern.search(varnum)
					
					if om != None:
						#print varnum
						#if stlen == 10:
						#cv2.imshow('mini',minicrop)
						try:
							if varnum[1] == '.' or varnum[1] == ',':
								nnull = 1
							else:
							 	nnull = 0
						except IndexError:
							continue
				
						if nnull == 1:
							if stlen >= 3:
								if is_number(varnum[0]):
									overpres = int(varnum[0])
									if overpres > overno and overpres == overno + 1:
										overno = overpres
										ballno = 0
										ballnum = (overno*6) + ballno
										vidtime = str(datetime.timedelta(seconds=framecount/fps))
										#c.execute("INSERT INTO OVERSSAMP1 VALUES (?, ?, ?, ?);", (overno,ballno,vidtime,framecount))
										#conn.commit()
										fcounter = fcounter +1
										print("OVERS {}.{}  Ball number = {} \t Time = {} \t Frame = {}".format(overno,ballno,ballnum,vidtime,framecount))

							if stlen >= 3:
								if is_number(varnum[2]):
									ballpres = int(varnum[2])
									if ballpres >= ballno:
										ballno = ballpres
										ballnum = (overno*6) + ballno
										vidtime = str(datetime.timedelta(seconds=framecount/fps))
										#c.execute("INSERT INTO OVERSSAMP1 VALUES (?, ?, ?, ?);", (overno,ballno,vidtime,framecount))
										#conn.commit()
										fcounter = fcounter +1
										print("OVERS {}.{}  Ball number = {} \t Time = {} \t Frame = {}".format(overno,ballno,ballnum,vidtime,framecount))
										if fcounter>10:
											#cv2.imshow('overs',minicrop)
											fovery = scorey 
											foverh = scoreh
											foverx = scorex 
											foverw = scorew	
											break
						
						
					
	#cv2.imshow('frame2',crop)
	if fcounter>10:
		vid.release()
		break
		
#DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD FROM ## INIT DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD;D

scoreprev = 0
ballno = 0
overno = 0
fps = 25
nnull = 0
nnull2 = 0
overno = 0
flag = 0
scounter =0

vid = cv2.VideoCapture('video')# insert video name
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
	crop2 = frame[nheight:height, 0:width]
	#print("{}X{}".format(vid.get(3),vid.get(4)))
	if not grabbed:
		break
	framecount = framecount+1

	if framecount%1==0: #and framecount > 30000:
		
		gray = cv2.cvtColor(crop,cv2.COLOR_BGR2GRAY) #these are working
		
		edges = cv2.Canny(gray,100,200)
		kernel = np.ones((2,2),np.uint8)
		#kernel2 = np.ones((1,1),np.uint8)
		dilation = cv2.dilate(edges,kernel,iterations = 4)
		#cv2.imshow('frame3',dilation)
		_,contours, hierarchy = cv2.findContours(dilation,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) 

		for contour in contours:
   
			[x,y,w,h] = cv2.boundingRect(contour)
			#y = y-10
			#x = x-10
			#h = h + 7
			#w = w + 10
			if h<100 and w<100:
				if h>10 and w>30:
					
					cv2.rectangle(crop,(x,y),(x+w,y+h),(0,0,255),2)
					if (y - 5>0) and (x - 5>0) and (h + 10<bot25) and (w + 50<width):
					#cv2.rectangle(crop,(nx,ny),(nx+nw,ny+nh,(0,0,255),2)
						nscorey = y-5
						nscorex = x-5
						nscoreh = h + 3
						nscorew = w + 50	
						flag = 1
					#minicrop = crop2[y:y+h, x:x+w]
					if flag == 1:
						minicrop = crop2[nscorey:nscorey+nscoreh, nscorex:nscorex+nscorew]
						flag = 0
					else:
						minicrop = crop2[y:y+h, x:x+w]
						
					gray = cv2.cvtColor(minicrop, cv2.COLOR_BGR2GRAY)
					th1 = imutils.resize(gray, width=400)
					ret,th2 = cv2.threshold(th1,100,225,cv2.THRESH_BINARY)
					ret,th3 = cv2.threshold(th2,127,255,cv2.THRESH_BINARY_INV)
		
					th4 = cv2.medianBlur(th3,9)
					th5 = cv2.bilateralFilter(th4,9,75,75)
					#cv2.imshow('frame3',th5)
					#minicrop = crop[ny:ny+nh, nx:nx+nw]
					cv2.imwrite("tester7.jpg",th5)
		
					# Extracting data from image
					varnum= pytesseract.image_to_string(Image.open('tester7.jpg'))
					varnum= varnum.replace(" ", "")
					
					stlen = len(varnum)
					#print varnum,stlen
					
					#overpattern = re.compile(r'\d.\d|\d{2}.\d|\d,\d|\d{2},\d')
					overpattern = re.compile(r'FROM\d\d\d|FROM\d\d|FROM\d|FR0M\d\d\d|FR0M\d\d|FR0M\d')
					om = overpattern.search(varnum)
					
					if om != None:
						#print varnum,stlen
						#if stlen == 10:
						if stlen == 7:
							if is_number(varnum[4]) and is_number(varnum[5]) and is_number(varnum[6]):
								ones = int(varnum[6])
								tens = int(varnum[5])
								hudrs = int(varnum[4])
								ballremn = (hudrs*100)+(tens*10)+ones
								ballnum = 120 - ballremn
								vidtime = str(datetime.timedelta(seconds=framecount/fps))
								scounter = scounter +1
								print("Ball number = {} \t Time = {} \t Frame = {}".format(ballnum,vidtime,framecount))
						if stlen == 6:
							if is_number(varnum[4]) and is_number(varnum[5]):
								ones = int(varnum[5])
								tens = int(varnum[4])
								ballremn = (tens*10)+ones
								ballnum = 120 - ballremn
								vidtime = str(datetime.timedelta(seconds=framecount/fps))
								scounter = scounter +1
								print("Ball number = {} \t Time = {} \t Frame = {}".format(ballnum,vidtime,framecount))
								if scounter>10:
									#cv2.imshow('overs2',th5)
									sovery = nscorey 
									soverh = nscoreh
									soverx = nscorex 
									soverw = nscorew	
									break
						
						
					
	#cv2.imshow('frame2',crop)
	if scounter>10:
		vid.release()
		break
	
#************************************************************************************** overs 0 . 0  MAIN ********************

framecount = 0
scoreprev = 0
ballno = 0
overno = 0
fps = 25
nnull = 0
nnull2 = 0
overno = 0
changeover = 0
lastball=20

vid = cv2.VideoCapture('video')#insert video name
while(vid.isOpened()):
	(grabbed, frame) = vid.read()
	if not grabbed:
		break
		
	width = vid.get(3)
	height = vid.get(4)
	bot25 = (height*15)/100
	nheight = height - bot25
	crop = frame[nheight:height, 0:width]#score
	framecount = framecount+1

	if framecount%10==0 and changeover == 0:

		
		
		overcrop = crop[fovery:fovery+foverh, foverx:foverx+foverw]
		gray = cv2.cvtColor(overcrop, cv2.COLOR_BGR2GRAY)
		th1 = imutils.resize(gray, width=800)
		ret,th2 = cv2.threshold(th1,100,225,cv2.THRESH_BINARY)
		ret,th3 = cv2.threshold(th2,127,255,cv2.THRESH_BINARY_INV)
		
		th4 = cv2.medianBlur(th3,9)
		th5 = cv2.bilateralFilter(th4,9,75,75)
				
		cv2.imwrite("tester.jpg",th5)
	
		
		# Extracting data from image
		var= pytesseract.image_to_string(Image.open('tester.jpg'))
		varnum= var.replace(" ","")
		stlen = len(varnum)
		#print("len = {}".format(stlen))
		
		overpattern = re.compile(r'\d|\d.\d|\d{2}.\d|\d,\d|\d{2},\d')
		om = overpattern.search(varnum)

		if om != None:
			#print varnum
			#if stlen == 10:
			
			try:
				if varnum[1] == '.' or varnum[1] == ',':# or stlen <= 2:
					nnull = 1
				else:
				 	nnull = 0
			except IndexError:
				continue
			#print("stlen = {}".format(stlen))	
			if nnull == 1:
				if stlen >= 1:
					#print("stlen = {}".format(stlen))
					if is_number(varnum[0]):
						overpres = int(varnum[0])
					#elif varnum[0] == 'l':
						#overpres = 1
						if overpres > overno and overpres == overno + 1:
							overno = overpres
							ballno = 0
							ballnum = (overno*6) + ballno
							vidtime = str(datetime.timedelta(seconds=framecount/fps))
							if ballnum>=20:
								changeover = 1
							#c.execute("INSERT INTO OVERSSAMP1 VALUES (?, ?, ?, ?);", (overno,ballno,vidtime,framecount))
							#conn.commit()
							wrt.writerow((overno,ballno,ballnum,vidtime,framecount))
							print("OVERS {}.{}  Ball number = {} \t Time = {} \t Frame = {}".format(overno,ballno,ballnum,vidtime,framecount))

				if stlen >= 3:
					if is_number(varnum[2]):
						ballpres = int(varnum[2])
						if ballpres > ballno:
							ballno = ballpres
							ballnum = (overno*6) + ballno
							vidtime = str(datetime.timedelta(seconds=framecount/fps))
							if ballnum>=20:
								changeover = 1
							#c.execute("INSERT INTO OVERSSAMP1 VALUES (?, ?, ?, ?);", (overno,ballno,vidtime,framecount))
							#conn.commit()
							wrt.writerow((overno,ballno,ballnum,vidtime,framecount))
							print("OVERS {}.{}  Ball number = {} \t Time = {} \t Frame = {}".format(overno,ballno,ballnum,vidtime,framecount))
				
			#two digit			
			try:
				if (varnum[2] == '.' or varnum[2] == ',') and overno >= 9:
					nnull2 = 1
				else:
				 	nnull2 = 0
			except IndexError:
				continue	
			
			if nnull2 == 1:
				if stlen >= 2:
					if is_number(varnum[0]) and is_number(varnum[1]):
						overpres1 = int(varnum[0])
						overpres2 = int(varnum[1])
						overpres = overpres1*10 + overpres2
						if overpres > overno and overpres == overno + 1:
							overno = overpres
							ballno = 0
							ballnum = (overno*6) + ballno
							vidtime = str(datetime.timedelta(seconds=framecount/fps))
							if ballnum>=20:
								changeover = 1
							#c.execute("INSERT INTO OVERSSAMP1 VALUES (?, ?, ?, ?);", (overno,ballno,vidtime,framecount))
							#conn.commit()
							wrt.writerow((overno,ballno,ballnum,vidtime,framecount))
							print("OVERS {}.{}  Ball number = {} \t Time = {} \t Frame = {}".format(overno,ballno,ballnum,vidtime,framecount))

				if stlen >= 4:
					if is_number(varnum[3]):
						ballpres = int(varnum[3])
						if ballpres > ballno:
							ballno = ballpres
							ballnum = (overno*6) + ballno
							vidtime = str(datetime.timedelta(seconds=framecount/fps))
							if ballnum>=20:
								changeover = 1
							#c.execute("INSERT INTO OVERSSAMP1 VALUES (?, ?, ?, ?);", (overno,ballno,vidtime,framecount))
							#conn.commit()
							wrt.writerow((overno,ballno,ballnum,vidtime,framecount))
							print("OVERS {}.{}  Ball number = {} \t Time = {} \t Frame = {}".format(overno,ballno,ballnum,vidtime,framecount))	
					

#DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD FROM ## MAIN DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD;D



	if framecount%10==0 and changeover == 1: #and framecount > 30000:
		
		overcrop = crop[sovery:sovery+soverh, soverx:soverx+soverw]
		gray = cv2.cvtColor(overcrop, cv2.COLOR_BGR2GRAY)
		th1 = imutils.resize(gray, width=400)
		ret,th2 = cv2.threshold(th1,100,225,cv2.THRESH_BINARY)
		ret,th3 = cv2.threshold(th2,127,255,cv2.THRESH_BINARY_INV)
		th4 = cv2.medianBlur(th3,9)
		th5 = cv2.bilateralFilter(th4,9,75,75)
					
		cv2.imwrite("tester7.jpg",th5)
		
					# Extracting data from image
		varnum= pytesseract.image_to_string(Image.open('tester7.jpg'))
		varnum= varnum.replace(" ", "")
					
		stlen = len(varnum)
					
		overpattern = re.compile(r'FROM\d\d\d|FROM\d\d|FROM\d|FR0M\d\d\d|FR0M\d\d|FR0M\d')
		om = overpattern.search(varnum)
					
		if om != None:
						
			if stlen == 7:
				if is_number(varnum[4]) and is_number(varnum[5]) and is_number(varnum[6]):
					ones = int(varnum[6])
					tens = int(varnum[5])
					hudrs = int(varnum[4])
					ballremn = (hudrs*100)+(tens*10)+ones
					ballnum = 120 - ballremn
					vidtime = str(datetime.timedelta(seconds=framecount/fps))
					if ballnum>lastball and ballnum < lastball + 2:
						lastball = ballnum
						overno = int(ballnum/6)
						ballofovr = ballnum % 6
						#print("Ball number = {} \t Time = {} \t Frame = {}".format(ballnum,vidtime,framecount))
						wrt.writerow((overno,ballofovr,ballnum,vidtime,framecount))
						print("OVERS {}.{}  Ball number = {} \t Time = {} \t Frame = {}".format(overno,ballofovr,ballnum,vidtime,framecount))	
			if stlen == 6:
				if is_number(varnum[4]) and is_number(varnum[5]):
					ones = int(varnum[5])
					tens = int(varnum[4])
					ballremn = (tens*10)+ones
					ballnum = 120 - ballremn
					vidtime = str(datetime.timedelta(seconds=framecount/fps))
					if ballnum>lastball and ballnum < lastball + 2:
						lastball = ballnum
						overno = int(ballnum/6)
						ballofovr = ballnum % 6
						#print("Ball number = {} \t Time = {} \t Frame = {}".format(ballnum,vidtime,framecount))
						wrt.writerow((overno,ballofovr,ballnum,vidtime,framecount))
						print("OVERS {}.{}  Ball number = {} \t Time = {} \t Frame = {}".format(overno,ballofovr,ballnum,vidtime,framecount))	
			if stlen == 5:
				if is_number(varnum[4]):
					ones = int(varnum[4])
					ballremn = ones
					ballnum = 120 - ballremn
					vidtime = str(datetime.timedelta(seconds=framecount/fps))
					if ballnum>lastball and ballnum < lastball + 2:
						lastball = ballnum
						overno = int(ballnum/6)
						ballofovr = ballnum % 6
						#print("Ball number = {} \t Time = {} \t Frame = {}".format(ballnum,vidtime,framecount))
						wrt.writerow((overno,ballofovr,ballnum,vidtime,framecount))
						print("OVERS {}.{}  Ball number = {} \t Time = {} \t Frame = {}".format(overno,ballofovr,ballnum,vidtime,framecount))	
						
					
		#cv2.imshow('Ballnum',overcrop)

	    	if cv2.waitKey(1) & 0xFF == ord('q'):
			break

vid.release()
cv2.destroyAllWindows()


