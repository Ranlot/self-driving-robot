# Please only modify the indicated area below!

from math import *
import random
from Robot import Robot
import numpy as np

landmarks  = [[0.0, 100.0], [0.0, 0.0], [100.0, 0.0], [100.0, 100.0]]
worldSize = 100.0

max_steering_angle = pi / 4.0 
bearing_noise = 0.1 
steering_noise = 0.1 
distance_noise = 5.0 

tolerance_xy = 15.0 # Tolerance for localization in the x and y directions.
tolerance_orientation = 0.25 # Tolerance for orientation.

numbOfParticles = 1000

def extractPositions(particles):
	x = 0.0
    	y = 0.0
    	orientation = 0.0
    	for i in range(len(particles)):
        	x += particles[i].x
        	y += particles[i].y
        	# orientation is cyclic
        	orientation += (((particles[i].orientation - particles[0].orientation + pi) % (2.0 * pi)) + particles[0].orientation - pi)
  	return [x / len(particles), y / len(particles), orientation / len(particles)]

def generate_ground_truth(motions, landmarks, worldSize):

	myrobot = Robot({'landmarks':landmarks, 'worldSize':worldSize})
    	myrobot.set_noise({'bearing':bearing_noise, 'steering': steering_noise, 'distance': distance_noise})

    	Z = []
    	T = len(motions)

    	for t in range(T):
        	myrobot = myrobot.move(motions[t])
        	Z.append(myrobot.sense())
    	return [myrobot, Z]


def check_output(final_robot, estimated_position):

	error_x = abs(final_robot.x - estimated_position[0])
    	error_y = abs(final_robot.y - estimated_position[1])
    	error_orientation = abs(final_robot.orientation - estimated_position[2])
    	error_orientation = (error_orientation + pi) % (2.0 * pi) - pi
    	correct = error_x < tolerance_xy and error_y < tolerance_xy and error_orientation < tolerance_orientation
    	return correct

def particleFilter(motions, measurements, N=numbOfParticles):
	# 1) make particles
	particles = [Robot({'landmarks':landmarks, 'worldSize':worldSize}) for particle in range(numbOfParticles)]	
	[particle.set_noise({'bearing': bearing_noise, 'steering': steering_noise, 'distance': distance_noise}) for particle in particles]


	for motion, measurement in zip(motions, measurements):

		particles = [particle.move(motion) for particle in particles]
		particleWeights = [particle.measurement_prob(measurement) for particle in particles]
		particleWeights = map(lambda weight: weight / sum(particleWeights), particleWeights)

		particles = np.random.choice(a=particles, size=len(particles), replace=True, p=particleWeights)

	return extractPositions(particles)


motions = [[2. * pi / 20, 12.] for row in range(6)]
x = generate_ground_truth(motions, landmarks, worldSize)
final_robot = x[0]
measurements = x[1]
estimated_position = particleFilter(motions, measurements)

print 'Ground truth:\t', final_robot
print 'Particle filter:\t', estimated_position
print 'Code check:\t', check_output(final_robot, estimated_position)
