import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from matrixClassFromCourse import matrix
import imageio
import glob
import os

from plotterFunctions import *

def estimateBasedOnMeasurement(currentEstimate, currentUncertainty, measurement, measurementProjectionMatrix, measurementNoiseMatrix):
	error = measurement.transpose() - (measurementProjectionMatrix * currentEstimate)	#error between measurement and current estimate (because of specific H, th estimate is just the position
	S = measurementProjectionMatrix * currentUncertainty * measurementProjectionMatrix.transpose() + measurementNoiseMatrix
	KalmanGain = currentUncertainty * measurementProjectionMatrix.transpose() * S.inverse()
	
	updatedEstimate = currentEstimate + (KalmanGain * error)
	updatedUncertainty = (identityMatrix - (KalmanGain * measurementProjectionMatrix)) * currentUncertainty

	return updatedEstimate, updatedUncertainty

def makePrediction(currentEstimate, currentUncertainty, stateTransitionMatrix, externalBias):
	updatedEstimate	= stateTransitionMatrix * currentEstimate + externalBias
	updatedUncertainty = stateTransitionMatrix * currentUncertainty * stateTransitionMatrix.transpose()

	return updatedEstimate, updatedUncertainty


#------------------------------------------------
frameDir, animationDir = 'KalmanFilter/Frames', 'KalmanFilter/Animation'
if not os.path.exists(frameDir):        os.makedirs(frameDir)
if not os.path.exists(animationDir):    os.makedirs(animationDir)
#------------------------------------------------

measurements = [[x, 0.5*x] for x in range(3)]
initialXposition, initialYposition, initialXposUncertainty, initialYposUncertainty = -1., -0.5, 0., 0.
initialXvelocity, initialYvelocity, initialXvelUnvertainty, initialYvelUnvertainty = 0., 0., 1000., 1000.

measurements = map(lambda measurement: matrix([measurement]), measurements)

xpos = [measurement.value[0][0] for measurement in measurements]
ypos = [measurement.value[0][1] for measurement in measurements]

timeDiffBetweenMeasurements = 1.0
noisePositionMeasurement = 1.

currentEstimate = matrix([[initialXposition], [initialYposition], [initialXvelocity], [initialYvelocity]]) 
currentUncertainty = matrix([[0., 0., 0., 0.], [0., 0., 0., 0.], [0., 0., initialXvelUnvertainty, 0.], [0., 0., 0., initialYvelUnvertainty]]) 

externalBias = matrix([[0.], [0.], [0.], [0.]])
stateTransitionMatrix = matrix([[1., 0., timeDiffBetweenMeasurements, 0.], [0., 1., 0., timeDiffBetweenMeasurements], [0., 0., 1., 0.], [0., 0., 0., 1.]])

measurementProjectionMatrix = matrix([[1., 0., 0., 0.], [0., 1., 0., 0.]]) # measurement function that can only observe the positions
measurementNoiseMatrix = matrix([[noisePositionMeasurement, 0.], [0., noisePositionMeasurement]]) # measurement uncertainty ; position only

identityMatrix = matrix([[1., 0., 0., 0.], [0., 1., 0., 0.], [0., 0., 1., 0.], [0., 0., 0., 1.]]) 

#TODO: make all this nicer with recursion and without mutated variables
for measurementID, measurement in enumerate(measurements):
	#first; make a prediction about next location
	currentEstimate, currentUncertainty = makePrediction(currentEstimate, currentUncertainty, stateTransitionMatrix, externalBias)
	#second; adjust the estimate based on the actual measurement
	currentEstimate, currentUncertainty = estimateBasedOnMeasurement(currentEstimate, currentUncertainty, measurement, measurementProjectionMatrix, measurementNoiseMatrix)
	plotMaker(measurementID+1, xpos, ypos, frameDir)

#make a final prediction for which we don't have a measurement
currentEstimate, currentUncertainty = makePrediction(currentEstimate, currentUncertainty, stateTransitionMatrix, externalBias)
plotPrediction(4, xpos, ypos, currentEstimate.value[0][0], currentEstimate.value[1][0], currentEstimate.value[2][0], currentEstimate.value[3][0], frameDir)
 
allFrames = map(lambda img: imageio.imread(img), sorted(glob.glob('%s/*.png' % frameDir)))
imageio.mimwrite('%s/animatedKF.gif' % animationDir, allFrames, duration= [1]*(len(allFrames)-1) + [4])

