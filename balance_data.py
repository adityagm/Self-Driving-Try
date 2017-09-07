import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle

train_data = np.load('trainingData.nyp.npy')
print(len(train_data))
# to loosen the data 
df = pd.DataFrame(train_data)
print(df.head())
# check how many go straights and left and right
print(Counter(df[1].apply(str)))

left = []
right = []
straight = []

shuffle(train_data)

for data in train_data:
	img = data[0]
	choice = data[1]
	
	if choice == [1,0,0]:
		left.append([img, choice])
	
	elif choice == [0,1,0]:
		straight.append([img, choice])
	
	elif choice == [0,0,1]:
		right.append([img, choice])
	
	else:
		print('no choice')

straight = straight[:len(left)][:len(right)]
left = left[:len(straight)]
right = right[:len(straight)]		

final_data = straight + left + right

shuffle(final_data)
print(len(final_data))
np.save('trainingData_v2.npy', final_data)