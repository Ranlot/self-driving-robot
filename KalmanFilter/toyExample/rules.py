

def localize(priorMean, priorVariance, measuredPosition, measurementUncertainty):
	posteriorMean = (measurementUncertainty * priorMean + priorVariance * measuredPosition) / (priorVariance + measurementUncertainty)
	posteriorVariance = 1.0 / (1.0 / priorVariance + 1.0 / measurementUncertainty)
	return posteriorMean, posteriorVariance

def executeMove(priorMean, priorVariance, moveBy, moveUncertainty):
	posteriorMean = priorMean + moveBy
	posteriorVariance = priorVariance + moveUncertainty
	return posteriorMean, posteriorVariance

initialBeliefMean = 0.
initialBeliefUncertainty = 0.0001

measurements = [5., 6., 7., 9., 10.]
#measurements = [5., 5., 5., 5., 5.]
measurementUncertainty = 4. #measurement standard deviation

moves = [1., 1., 2., 1., 1.]
moveUncertainty = 2.

positionMean, positionUncertainty = initialBeliefMean, initialBeliefUncertainty
print 'initial belief', positionMean, positionUncertainty
for stepID, (measurement, move) in enumerate(zip(measurements, moves)):
	positionMean, positionUncertainty = localize(positionMean, positionUncertainty, measurement, measurementUncertainty)
	print 'after measurement\t', positionMean, positionUncertainty
	positionMean, positionUncertainty = executeMove(positionMean, positionUncertainty, move, moveUncertainty)
	print 'after move\t\t', positionMean, positionUncertainty
