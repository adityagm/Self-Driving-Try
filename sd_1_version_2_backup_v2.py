import numpy as np
from PIL import ImageGrab
import cv2
import time
from directScanKeys import ReleaseKey, PressKey, W, A, S, D
import pyautogui
from numpy import ones,vstack
from numpy.linalg import lstsq
from numpy import polyfit
from statistics import mean
from matplotlib import pyplot as plt
from getKeys import key_check
#import highgui
#just a countdown

def keys_to_output(keys):
	#[A,W,D]
	output = [0,0,0]
	
	if 'A' in keys:
		output[0] = 1
	elif 'D' in keys:
		output[2] = 1
	else
		output[1] = 1
		
	return output

for i in list(range(4))[::-1]:
	print(i+1)
	time.sleep(1)

def average_lane(lane_data):
	x1s = []
	y1s = []
	x2s = []
	y2s = []
	print("inside avaerage lane")
	# input("enter")
	for data in lane_data:
		x1s.append(data[2][0])
		y1s.append(data[2][1])
		x2s.append(data[2][2])
		y2s.append(data[2][3])
	return int(mean(x1s)), int(mean(y1s)), int(mean(x2s)), int(mean(y2s))
	
def draw_lines(img, lines):
	try:#if failed then call exception
		for line in lines:
			coords = line[0]
			cv2.line(img, (coords[0], coords[1]), (coords[2],coords[3]), [255, 255, 255], 3) 
	except:
		pass

def draw_lanes(image, lines):
	try:
		
		#finds maximum y value for a lane marker
		#horizon will remain the same, since we do not know its location
		ys = []
		for i in lines:
			for ii in i:
				ys += [ii[1],ii[3]] #(x,y)=[ii[0],ii[1]]
		
		min_y = min(ys)
		# print(min_y)
		max_y = 480
		# print(max_y)
		new_lines = []
		line_dict = {}
		
		for idx, i in enumerate(lines):
			for xyxy in i:
				# calculating the definition of line
				x_coords = (xyxy[0], xyxy[2])
				
				# y coordinates can ben equal hence lstsq generates 0 slope which will backfire, hence the following if condition
				
				y_coords = (xyxy[1],xyxy[3])
				A = vstack([x_coords,ones(len(x_coords))]).T
				
				m, b = polyfit(x_coords, y_coords,1)
				
				#calculating new xs
				x1 = (min_y-b) / m
				x2 = (max_y-b) / m
				print(x1,x2)
				
				line_dict[idx] = [m,b,[int(x1), min_y, int(x2), max_y]]
				
				new_lines.append([int(x1), min_y, int(x2), max_y])
				
		final_lanes={}
		
		for idx in line_dict:
			final_lanes_copy = final_lanes.copy()
			m = line_dict[idx][0]
			
			b = line_dict[idx][1]
			line = line_dict[idx][2]
			print("m=",m)
			print("b=",b)
			# input("press enter")
			if len(final_lanes) == 0:
			
				final_lanes[m] = [ [m,b,line] ]
				
			else:
				
				found_copy = False
				
				for other_ms in final_lanes_copy:
					
					if not found_copy:
						if abs(other_ms*1.2) > abs(m) > abs(other_ms*0.8):
							if abs(final_lanes_copy[other_ms][0][1]*1.2) >abs(m) >abs(final_lane_copy[other_ms][0][1]*0.8):
								# print('in line 101')
								final_lanes[other_ms].append([m,b,line])
								found_copy = True
								break
						else:
							# print('in line 106')
							final_lanes[m]= [ [m,b,line] ]
								
		line_counter = {}
			
		for lanes in final_lanes:
			line_counter[lanes] = len(final_lanes[lanes])
			top_lanes = sorted(line_counter.items(), key = lambda item: item[1])[::-1][:2]
			lane1_id = top_lanes[0][0]
			lane2_id = top_lanes[1][0]
				
		l1_x1, l1_y1, l1_x2, l1_y2 = average_lane(final_lanes[lane1_id])
		l2_x1, l2_y1, l2_x2, l2_y2 = average_lane(final_lanes[lane2_id])
			
		return [l1_x1, l1_y1, l1_x2, l1_y2], [l2_x1, l2_y1, l2_x2, l2_y2], lane1_id, lane2_id
			
	except Exception as e:
		print(str(e))
    
def roi(img, vertices):
	#blank mask
	mask = np.zeros_like(img)
	#filling pixels inside polygons defined by vertices with fill colour
	cv2.fillPoly(mask, vertices, 255)
	#returning the image where only masked pixels are non-zero
	masked = cv2.bitwise_and(img, mask)
	return masked

def process_img(original_image):
	
	#convert image to greyscale
	processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
	# hist = cv2.calcHist([processed_img],[0],None,[256],[0,256])
	# plt.hist(processed_img.ravel(),256,[0,256])
	# plt.title('Histogram for gray scale picture')
	# plt.show()
	#perform edge detection on processed image
	processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
	#add gaussian blur before passing image to hough lines so that the lines could be better detected
	processed_img = cv2.GaussianBlur(processed_img, (5,5), 0)
	vertices = np.array([[0,0],[0,200],[128,200],[514,200],[640,200],[640,0]],np.int32)
	processed_img = roi(processed_img,[vertices])
	
	#hough lines
	lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 180, np.array([]), 150, 5)
	m1 = 0
	m2 = 0 
	try:
		#print ("inside draw lanes")
		l1, l2 , m1 , m2 = draw_lanes(original_image,lines)
		print(l1)
		print(l2)
		print(m1)
		print(m2)
		
		cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), [0,255,0], 30)
		cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), [0,255,0], 30)
	except Exception as e:
		print(str(e))
		pass
	try:
		for coords in lines:
			coords = coords[0]
			try:
				cv2.line(processed_img, (coords[0], coords[1]), (coords[2], coords[3]), [255,0,0], 3)
			except Exception as e:
				print(str(e))
	except Exception as e:
		pass
		
	return processed_img, original_image, m1, m2
	#now, lines is matrix, hence we need to draw the lines between the points of the matrix
	#draw_lines(processed_img, lines)
	#return processed_img

last_time = time.time()

# following four functions to send corresponding key signals to the game 

def straight():
	PressKey(W)
	ReleaseKey(A)
	ReleaseKey(D)

def left():
	PressKey(A)
	ReleaseKey(W)
	ReleaseKey(D)

def right():
	PressKey(D)
	ReleaseKey(W)
	ReleaseKey(A)
	ReleaseKey(D)

def slow():
	ReleaseKey(A)
	ReleaseKey(W)
	ReleaseKey(D)

while(True):
	# convert the captured screenshot to numpy array, and then change the colour configuration of the same by calling color_BGR2RGB
	frame = np.array(ImageGrab.grab(bbox=(0,40,640,480)))
	new_screen, image, m1, m2 = process_img(frame)

	# following two lines causing too much delay, hence commented. just change printscreen_pil to numpy array directly in the function
	# printScreen_numpy = np.array(printScreen_pil.getdata(),dtype='uint8')\
	# .reshape((printScreen_pil.size[1],printScreen_pil.size[0],3))
	print('loop took {} seconds'.format(time.time()-last_time))
	last_time = time.time()
	cv2.imshow('window',new_screen)
	cv2.imshow('window2',cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
	# send corresponding keys to the game based on the slope data 
	if m1 < 0 and m2 < 0:
		right()
	elif m1 > 0 and m2 >0:
		left()
	else:
		straight()
		
	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break