from matrixClassFromCourse import matrix

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


measurements = [[5., 10.], [6., 8.], [7., 6.], [8., 4.], [9., 2.], [10., 0.]]
initialXposition, initialYposition, initialXposUncertainty, initialYposUncertainty = 4., 12., 0., 0.
initialXvelocity, initialYvelocity, initialXvelUnvertainty, initialYvelUnvertainty = 0., 0., 1000., 1000.

#measurements = [[1., 4.], [6., 0.], [11., -4.], [16., -8.]]
#initialXposition, initialYposition, initialXposUncertainty, initialYposUncertainty = -4., 8., 0., 0.
#initialXvelocity, initialYvelocity, initialXvelUnvertainty, initialYvelUnvertainty = 0., 0., 1000., 1000.

#measurements = [[1., 17.], [1., 15.], [1., 13.], [1., 11.]]
#initialXposition, initialYposition, initialXposUncertainty, initialYposUncertainty = 1., 19., 0., 0.
#initialXvelocity, initialYvelocity, initialXvelUnvertainty, initialYvelUnvertainty = 0., 0., 1000., 1000.

measurements = map(lambda measurement: matrix([measurement]), measurements)

timeDiffBetweenMeasurements = 0.1
noisePositionMeasurement = 0.1

currentEstimate = matrix([[initialXposition], [initialYposition], [initialXvelocity], [initialYvelocity]]) 
currentUncertainty = matrix([[0., 0., 0., 0.], [0., 0., 0., 0.], [0., 0., initialXvelUnvertainty, 0.], [0., 0., 0., initialYvelUnvertainty]]) 

externalBias = matrix([[0.], [0.], [0.], [0.]])
stateTransitionMatrix = matrix([[1., 0., timeDiffBetweenMeasurements, 0.], [0., 1., 0., timeDiffBetweenMeasurements], [0., 0., 1., 0.], [0., 0., 0., 1.]])

measurementProjectionMatrix = matrix([[1., 0., 0., 0.], [0., 1., 0., 0.]]) # measurement function that can only observe the positions
measurementNoiseMatrix = matrix([[noisePositionMeasurement, 0.], [0., noisePositionMeasurement]]) # measurement uncertainty ; position only

identityMatrix = matrix([[1., 0., 0., 0.], [0., 1., 0., 0.], [0., 0., 1., 0.], [0., 0., 0., 1.]]) 

estimatedPositions = []

#TODO: make all this nicer with recursion and without mutated variables
print 'initial', currentEstimate
for measurementID, measurement in enumerate(measurements):
	#first; make a prediction about next location
	currentEstimate, currentUncertainty = makePrediction(currentEstimate, currentUncertainty, stateTransitionMatrix, externalBias)
	#second; adjust the estimate based on the actual measurement
	currentEstimate, currentUncertainty = estimateBasedOnMeasurement(currentEstimate, currentUncertainty, measurement, measurementProjectionMatrix, measurementNoiseMatrix)
	print 'new estimate', currentEstimate

