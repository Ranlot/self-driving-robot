#simplified version of class provided in online course

from math import *
import random
from scipy.stats import norm
from operator import mul

class Robot:

	def __init__(self, obj):
		self.landmarks = obj['landmarks']
		self.world_size = obj['worldSize']
       		self.x = random.random() * self.world_size
       		self.y = random.random() * self.world_size
        	self.orientation = random.random() * 2.0 * pi
        	self.forward_noise = 0.0
        	self.turn_noise    = 0.0
        	self.sense_noise   = 5.0
		    
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


	def __distanceRobotToLandmark(self, obj):
		noiseLessEuclideanDistance = hypot(obj['robotX'] - obj['landmarkX'], obj['robotY'] - obj['landmarkY']) 
		return noiseLessEuclideanDistance + random.gauss(0.0, self.sense_noise)

	def sense(self):
		robotAndLandmarks = [{'robotX': self.x, 'robotY': self.y, 'landmarkX': landmark[0], 'landmarkY': landmark[1]} for landmark in self.landmarks]
		return map(self.__distanceRobotToLandmark, robotAndLandmarks)

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
        
		self.x = x
		self.y = y
		self.orientation = orientation
		
	def getParticleWeight(self, robotMeasurement):
		particleMeasurement = map(lambda landmark: hypot(self.x - landmark[0], self.y - landmark[1]), self.landmarks)
		gaussianMismatchWeight = norm.pdf(x=particleMeasurement, loc=robotMeasurement, scale=self.sense_noise)
		return reduce(mul, gaussianMismatchWeight, 1)
    
    	def __repr__(self):
        	return '[x=%.6s y=%.6s heading=%.6s]' % (str(self.x), str(self.y), str(self.orientation))


