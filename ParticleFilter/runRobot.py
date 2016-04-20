from math import *
from Robot import Robot

'''
def eval(r, p):
	sum = 0.0;
    	for i in range(len(p)): # calculate mean error
        	dx = (p[i].x - r.x + (self.world_size/2.0)) % self.world_size - (self.world_size/2.0)
        	dy = (p[i].y - r.y + (self.world_size/2.0)) % self.world_size - (self.world_size/2.0)
        	err = sqrt(dx * dx + dy * dy)
        	sum += err
    	return sum / float(len(p))
'''


landmarks  = [[20.0, 20.0], [80.0, 80.0], [20.0, 80.0], [80.0, 20.0]]
worldSize = 100.0

robot = Robot({'landmarks':landmarks, 'worldSize':worldSize})

#robot.set_noise({'forward': 5, 'turn': 0.1, 'sense': 5})
robot.set({'x': 30, 'y': 50, 'orientation': pi / 2})
print robot
robot.move({'turn': - pi / 2, 'forward': 15})
print robot
print robot.sense()
robot.move({'turn': - pi / 2, 'forward': 10})
print robot
print robot.sense()
