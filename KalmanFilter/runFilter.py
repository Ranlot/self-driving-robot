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


def kalmanFilter(measurement, currentEstimate, currentUncertainty):
		currentEstimate, currentUncertainty = estimateBasedOnMeasurement(currentEstimate, currentUncertainty, measurement, measurementProjectionMatrix, measurementNoiseMatrix)
		currentEstimate, currentUncertainty = makePrediction(currentEstimate, currentUncertainty, stateTransitionMatrix, externalBias)
		return currentEstimate, currentUncertainty

measurements = [1, 2, 3]
#measurements = [1] * 1
measurements = map(lambda measurement: matrix([[measurement]]), measurements)

currentEstimate = matrix([[0.], [0.]]) 
currentUncertainty = matrix([[1000., 0.], [0., 1000.]]) # very high initial uncertainty on position and velocity (no correlation)
externalBias = matrix([[0.], [0.]])
stateTransitionMatrix = matrix([[1., 1.], [0, 1.]])

measurementProjectionMatrix = matrix([[1., 0.]]) # measurement function that can only observe the velocity
measurementNoiseMatrix = matrix([[1.]]) # measurement uncertainty ; position only

identityMatrix = matrix([[1., 0.], [0., 1.]]) 

#print kalman_filter(x, P)
# output should be:
# x: [[3.9996664447958645], [0.9999998335552873]]
# P: [[2.3318904241194827, 0.9991676099921091], [0.9991676099921067, 0.49950058263974184]]

for measurement in measurements:
	currentEstimate, currentUncertainty = kalmanFilter(measurement, currentEstimate, currentUncertainty)
	print currentEstimate, currentUncertainty


