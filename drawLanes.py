import numpy as np
import cv2
from numpy import ones,vstack
from numpy import polyfit
from statistics import mean

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