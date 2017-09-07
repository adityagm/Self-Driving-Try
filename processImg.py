import numpy as np
import cv2
from drawLanes import draw_lanes

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
	#processed_img = cv2.cvtColor(original_image, cv2.COLOR_)
	# hist = cv2.calcHist([processed_img],[0],None,[256],[0,256])
	# plt.hist(processed_img.ravel(),256,[0,256])
	# plt.title('Histogram for gray scale picture')
	# plt.show()
	#perform edge detection on processed image
	processed_img = cv2.Canny(original_image, threshold1=200, threshold2=300)
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