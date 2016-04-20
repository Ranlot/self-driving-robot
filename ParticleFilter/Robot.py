#simple copy paste from class given in online course
#modified move method not to return new robot but to mutate current robot
#simplified constructor to avoid code duplication

from math import *
import random

class Robot:

	def __init__(self, obj):
		self.landmarks = obj['landmarks']
		self.world_size = obj['worldSize']
       		self.x = random.random() * self.world_size
       		self.y = random.random() * self.world_size
        	self.orientation = random.random() * 2.0 * pi
        	self.forward_noise = 0.0
        	self.turn_noise    = 0.0
        	self.sense_noise   = 0.0
		    
    	def set(self, obj):
		new_x = obj['x']
		new_y = obj['y']
		new_orientation = obj['orientation']
        	if new_x < 0 or new_x >= self.world_size:
            		raise ValueError, 'X coordinate out of bound'
        	if new_y < 0 or new_y >= self.world_size:
            		raise ValueError, 'Y coordinate out of bound'
        	if new_orientation < 0 or new_orientation >= 2 * pi:
            		raise ValueError, 'Orientation must be in [0..2pi]'
        	self.x = float(new_x)
       		self.y = float(new_y)
        	self.orientation = float(new_orientation)
    
    	def set_noise(self, obj):
		self.forward_noise = float(obj['forward'])
		self.turn_noise = float(obj['turn'])
		self.sense_noise = float(obj['sense'])

    	def sense(self):
        	Z = []
        	for i in range(len(self.landmarks)):
            		dist = sqrt((self.x - self.landmarks[i][0]) ** 2 + (self.y - self.landmarks[i][1]) ** 2)
            		dist += random.gauss(0.0, self.sense_noise)
            		Z.append(dist)
        	return Z
    
	def move(self, obj):
		turn = obj['turn']
		forward = obj['forward']
        	if forward < 0:
            		raise ValueError, 'Robot cant move backwards'         
        
        	# turn, and add randomness to the turning command
        	orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
       		orientation %= 2 * pi
        
        	# move, and add randomness to the motion command
        	dist = float(forward) + random.gauss(0.0, self.forward_noise)
        	x = self.x + (cos(orientation) * dist)
        	y = self.y + (sin(orientation) * dist)
        	x %= self.world_size    # cyclic truncate
        	y %= self.world_size
        
        	# set particle
        	#res = robot()
        	#res.set(x, y, orientation)
        	#res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        	#return res
		self.x = x
		self.y = y
		self.orientation = orientation
		
    
    	def Gaussian(self, mu, sigma, x):
        	# calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        	return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))
    
    	def measurement_prob(self, measurement):
        	# calculates how likely a measurement should be
        	prob = 1.0;
        	for i in range(len(self.landmarks)):
            		dist = sqrt((self.x - self.landmarks[i][0]) ** 2 + (self.y - self.landmarks[i][1]) ** 2)
            		prob *= self.Gaussian(dist, self.sense_noise, measurement[i])
        	return prob
    
    
    	def __repr__(self):
        	return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))


