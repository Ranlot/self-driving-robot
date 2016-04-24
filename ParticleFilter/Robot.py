import random
from math import *
from operator import mul
from scipy.stats import norm

class Robot:
    def __init__(self, obj, length=20.0):
	self.landmarks = obj['landmarks']
	self.world_size = obj['worldSize']
        self.x = random.random() * self.world_size
        self.y = random.random() * self.world_size
	self.length = length
        self.orientation = random.random() * 2.0 * pi
        self.bearing_noise = 0.0;
        self.steering_noise = 0.0;
        self.distance_noise = 0.0;
    
    def set(self, new_x, new_y, new_orientation):
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
	self.bearing_noise = float(obj['bearing'])
	self.steering_noise = float(obj['steering'])
	self.distance_noise = float(obj['distance'])
   
    def __distanceRobotToLandmark(self, obj):
	noiseLessEuclideanDistance = hypot(obj['robotX'] - obj['landmarkX'], obj['robotY'] - obj['landmarkY']) 
	return noiseLessEuclideanDistance + random.gauss(0.0, self.sense_noise)

    def oldSense(self):
	robotAndLandmarks = [{'robotX': self.x, 'robotY': self.y, 'landmarkX': landmark[0], 'landmarkY': landmark[1]} for landmark in self.landmarks]
	return map(self.__distanceRobotToLandmark, robotAndLandmarks)


    def sense(self, noise = 1):
	Z = []
	for l in self.landmarks:
		direction = atan2(l[0] - self.y, l[1] - self.x)
		bearing = direction - self.orientation
		if noise == 1:
			bearing += random.gauss(0, self.bearing_noise)
		Z.append(bearing % (2 * pi))
		
	return Z

    def measurement_prob(self, measurements):
	predicted_measurements = self.sense(0) # Our sense function took 0 as an argument to switch off noise.
	error = 1.0
        for i in range(len(measurements)):
		error_bearing = abs(measurements[i] - predicted_measurements[i])
            	error_bearing = (error_bearing + pi) % (2.0 * pi) - pi # truncate

		error *= (exp(- (error_bearing ** 2) / (self.bearing_noise ** 2) / 2.0) / sqrt(2.0 * pi * (self.bearing_noise ** 2)))

	return error


    def move(self, motion):
	result = Robot({'landmarks':self.landmarks, 'worldSize':self.world_size}, self.length)
	result.set_noise({'bearing':self.bearing_noise, 'steering':self.steering_noise, 'distance':self.distance_noise})
	
	# bicycle model
	alpha = random.gauss(motion[0], self.steering_noise)
	d = random.gauss(motion[1], self.distance_noise)
	beta = d * tan(alpha) / self.length
		
	if abs(beta) < 0.001:
		# no movement
		result.x = self.x + d * cos(self.orientation)
		result.y = self.y + d * sin(self.orientation)
	else:
		R = d / beta
		cx = self.x - sin(self.orientation) * R
		cy = self.y + cos(self.orientation) * R
		result.x = cx + sin(self.orientation + beta) * R
		result.y = cy - cos(self.orientation + beta) * R
		
	result.orientation = (self.orientation + beta) % (2*pi)
	return result


    def oldMove(self, obj):
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
        res = Robot({'landmarks':self.landmarks, 'worldSize':self.world_size})
        res.set(x, y, orientation)
        res.set_noise({'forward': self.forward_noise, 'turn': self.turn_noise, 'sense': self.sense_noise})
        return res
	
    def getParticleWeight(self, robotMeasurement):
	particleMeasurement = map(lambda landmark: hypot(self.x - landmark[0], self.y - landmark[1]), self.landmarks)
	gaussianMismatchWeight = norm.pdf(x=particleMeasurement, loc=robotMeasurement, scale=self.sense_noise)
	return reduce(mul, gaussianMismatchWeight, 1.0)

    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))

