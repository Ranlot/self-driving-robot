import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from matrixClassFromCourse import matrix
import imageio
import glob

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


def plotMaker(index, xpos, ypos):
	plMeasured = plt.scatter(xpos[:index], ypos[:index], c='black', marker='o', s=120, label='measured')
	plt.legend(loc='lower right', scatterpoints=1, shadow=True)
	plt.title('time = %d' % index); plt.grid()
	plt.xlabel('position in x'); plt.ylabel('position in y')
	plt.xlim([-0.3, 3.3]); plt.ylim([-0.3, 1.9])
	plt.savefig('Frames/%d.png' % index)
	plt.close()


def plotPrediction(predictionTime, xpos, ypos, predictionX, predictionY, predictedXvelocity, predictedYvelocity):
	plMeasured = plt.scatter(xpos, ypos, c='black', marker='o', s=120, label='measured')
	plPredicted = plt.scatter([predictionX], [predictionY], c='orange', marker='D', s=120, label='measured')
	plt.legend((plMeasured, plPredicted), ('measured', 'KF prediction\nx = %.1f; vx = %.1f\ny = %.1f ; vy = %.1f' % (predictionX, predictedXvelocity, predictionY, predictedYvelocity)), scatterpoints=1, loc='lower right')
	plt.title('time = %d ; Kalman Filter prediction' % predictionTime); plt.grid()
	plt.xlabel('position in x'); plt.ylabel('position in y')
	plt.xlim([-0.3, 3.3]); plt.ylim([-0.3, 1.9])
	plt.savefig('Frames/%d.png' % predictionTime)
	plt.close()


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
	plotMaker(measurementID+1, xpos, ypos)

#make a final prediction for which we don't have a measurement
currentEstimate, currentUncertainty = makePrediction(currentEstimate, currentUncertainty, stateTransitionMatrix, externalBias)
plotPrediction(4, xpos, ypos, currentEstimate.value[0][0], currentEstimate.value[1][0], currentEstimate.value[2][0], currentEstimate.value[3][0])
 
allFrames = map(lambda img: imageio.imread(img), sorted(glob.glob('Frames/*.png')))
imageio.mimwrite('Animation/animatedKF.gif', allFrames, duration= [1]*(len(allFrames)-1) + [4])

