# Please only modify the indicated area below!

from math import *
import random
from Robot import Robot
import numpy as np

landmarks  = [[20.0, 20.0], [80.0, 80.0], [20.0, 80.0], [80.0, 20.0]]
worldSize = 100.0
numbOfParticles = 1000

def eval(r, p):
	sum = 0.0;
    	for i in range(len(p)): # calculate mean error
        	dx = (p[i].x - r.x + (worldSize/2.0)) % worldSize - (worldSize/2.0)
        	dy = (p[i].y - r.y + (worldSize/2.0)) % worldSize - (worldSize/2.0)
        	err = sqrt(dx * dx + dy * dy)
        	sum += err
    	return sum / float(len(p))


#def cyclicDistance(coord1, coord2):
#	return (coord1 - coord2 + (worldSize/2.0)) % worldSize - (worldSize/2.0)

#def myEval(robot, particles):
#	dx = map(lambda particle: particle.x, robot.x, particles)
#	dy = map(lambda particle: particle.y, robot.y, particles)
#	[x*x for x in dx]
#	[x*x for x in dy]	

robot = Robot({'landmarks':landmarks, 'worldSize':worldSize})
robot = robot.move({'turn': 0.1, 'forward': 5.0})
robotMeasurement = robot.sense()

particles = [Robot({'landmarks':landmarks, 'worldSize':worldSize}) for particle in range(numbOfParticles)]
[particle.set_noise({'forward': 0.05, 'turn': 0.05, 'sense': 5.0}) for particle in particles]

print eval(robot, particles)

for timeStamp in range(10):
	robot = robot.move({'turn': 0.1, 'forward': 5.0})
	robotMeasurement = robot.sense()

	particles = [particle.move({'turn': 0.1, 'forward': 5.0}) for particle in particles]

	particleWeights = [particle.getParticleWeight(robotMeasurement) for particle in particles]
	particleWeights = map(lambda weight: weight / sum(particleWeights), particleWeights)

	particles = np.random.choice(a=particles, size=len(particles), replace=True, p=particleWeights)
	print eval(robot, particles)

print robot
print particles[:20]
