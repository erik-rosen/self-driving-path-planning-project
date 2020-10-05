import matplotlib.pyplot as plt
from matplotlib.path import Path
import csv
import random
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental.preprocessing import Normalization
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

vehicles = {}
x = []
x_train_dict = {}
x_test_dict = {}
labels = []
lane_switches = []
snippet_size = 10;
max_delta_t = 3000;
max_delta_s = 20;
predict_points_in_future = 5
lane_0_center = 2
lane_1_center = 6
lane_2_center = 10

def getClosestLane(d):
	distance_to_lane_0_center = abs(d-lane_0_center)
	distance_to_lane_1_center = abs(d-lane_1_center)
	distance_to_lane_2_center = abs(d-lane_2_center)
	if (distance_to_lane_0_center<distance_to_lane_2_center and distance_to_lane_0_center<distance_to_lane_1_center):
		return 0
	if (distance_to_lane_1_center<distance_to_lane_0_center and distance_to_lane_1_center<distance_to_lane_2_center):
		return 1
	if (distance_to_lane_2_center<distance_to_lane_1_center and distance_to_lane_2_center<distance_to_lane_0_center):
		return 2
	else:
		 raise Exception("No lane closest?")



with open('data/other_vehicles.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        timestamp = int(row[0]);
        vehicle_id = int(row[1]);
        t = float(row[0])
        s = float(row[6])
        d = float(row[7])
        s_dot = float(row[8])
        d_dot = float(row[9])
        if not (vehicle_id in vehicles):
        	vehicles[vehicle_id] = []
        vehicles[vehicle_id].append([t,s,d,s_dot,d_dot])
        

for vehicle_id in vehicles:
	verts = np.array(vehicles[vehicle_id])
	#print(verts.shape)
	#plt.plot(verts[:, 1], verts[:, 2])
	for snippet_start in range(0, verts.shape[0], 1):
		## Check that the snippet does not have any wierd discontinuties
		snippet = verts[snippet_start:snippet_start+snippet_size]
		if snippet[0,2]<0 or abs(snippet[0,2])>12:
			print("point off grid - discard")
			continue

		if snippet.shape[0] < predict_points_in_future:
			print("snippet too short")
			continue;
		delta_t_arr = (snippet[:,0] - np.roll(snippet[:,0],1))[1:]
		delta_s_arr = (snippet[:,1] - np.roll(snippet[:,1],1))[1:]
		if(np.max(delta_t_arr)>max_delta_t):
			print("discarding snippet due to timestamp jump")
			#plt.plot(snippet[:, 1], snippet[:, 2],'r+')
			continue;
		if(np.max(delta_s_arr)>max_delta_s):
			print("discarding snippet due to distance jump")
			#plt.plot(snippet[:, 1], snippet[:, 2],'r.')
			continue;
		if(np.min(delta_s_arr)<0):
			print("discarding snippet due to negative distance")
			#plt.plot(snippet[:, 1], snippet[:, 2],'r.')
			continue;

		future_lane_style = {
  			0: 'r+',
 			1: 'g+',
  			2: 'b+'
		}

		switch_lane_in_snippet = False
		if(np.max(snippet[:,2])-np.min(snippet[:,2])>3.5):
			switch_lane_in_snippet = True

		label = getClosestLane(snippet[predict_points_in_future-1,2])
		plt.plot(snippet[0, 1], snippet[0, 2], future_lane_style[label])
		x.append([snippet[0, 2], snippet[0, 3],snippet[0, 4]])
		labels.append(label)
		lane_switches.append(switch_lane_in_snippet)


#balance training set such that it contains an equal amount of lane switches as going straight
while lane_switches.count(True)<lane_switches.count(False):
	print(lane_switches.count(True) / (lane_switches.count(False)+lane_switches.count(True)))
	ii = np.where(np.array(lane_switches) == False)[0]
	print(ii)
	i = random.choice(ii)
	lane_switches.pop(i)
	labels.pop(i)
	x.pop(i)


x = np.array(x)
y = tf.keras.utils.to_categorical(np.array(labels))





model = Sequential()
model.add(Dense(20, input_dim=3, activation='relu'))
model.add(Dense(40, activation='relu'))
model.add(Dense(20, activation='relu'))
model.add(Dense(3, activation='softmax'))



# Compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(x, y, batch_size=200, verbose=1, epochs=100, validation_split=0.20)


