import matplotlib.pyplot as plt
import seaborn as sns
import operator
import numpy as np

def overlayWorldMap(worldMap, locationProbs):
	sizeVertical = len(worldMap)
	return map(lambda row: zip(worldMap[row], locationProbs[row]), range(sizeVertical))

def deInterLeaver(coLocationGrid):
	return [map(lambda cell: cell[1], row) for row in coLocationGrid]

#defining closure function
def measurementProcessor(measurement, probSensorIsRight):
	def processRow(colocationRow):
		return map(lambda cell: probSensorIsRight * cell[1] if cell[0] == measurement else (1 - probSensorIsRight) * cell[1], colocationRow)
	return processRow

#using numpy array would look more simple, yes...???
def locationNormalizer(locationProbs):
	normalizingConstant, sizeVertical_t = sum(map(sum, locationProbs)), len(locationProbs)
	if normalizingConstant == 0.0:	raise ValueError('worldMap probably inconsistent with measurements & moves')
	return [map(lambda cell: cell / normalizingConstant, locationProbs[row]) for row in range(sizeVertical_t)]

def localize(measurement, probSensorIsRight, coLoc):
	newLocation = locationNormalizer(map(measurementProcessor(measurement, probSensorIsRight), coLoc))
	return newLocation

def shift(locationRow, n, move):
	if move == 'right':	pivot = len(locationRow) - n
	else:			pivot = n
	return locationRow[pivot::] + locationRow[:pivot:]

def horizontalMove(locationRow, move, probMoveIsSuccessful):
	failedMove = map(lambda cell: (1 - probMoveIsSuccessful) * cell, locationRow)
	successfulMove = map(lambda cell: probMoveIsSuccessful * cell, shift(locationRow, 1, move))
	return map(operator.add, failedMove, successfulMove)

def locationFlipper(locationProbs):
	return map(list, zip(*locationProbs))

def executeMove(move, probMoveIsSuccessful, locationProbs):
	if move == 'stay':
		return locationProbs
	if move == 'left' or move == 'right':		
		return locationNormalizer(map(lambda locationRow: horizontalMove(locationRow, move, probMoveIsSuccessful), locationProbs))
	elif move == 'up' or move == 'down':
		transposeLocationMatrix, transposeMove = locationFlipper(locationProbs), 'right' if move == 'down' else 'left'
		transposedResult = locationNormalizer(map(lambda locationRow: horizontalMove(locationRow, transposeMove, probMoveIsSuccessful), transposeLocationMatrix))
		return map(list, zip(*transposedResult))
	else:
		raise ValueError('move not supported')

#------------------------------------------------
# there is an open seaborn bug regarding ticklabels
# https://github.com/mwaskom/seaborn/issues/837
# maybe make provide a PR
#------------------------------------------------
def locationPrinter(worldMap, locationProbs, message, frameDir, debug=False):
	sizeHorizontal, sizeVertical = len(worldMap[0]), len(worldMap)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	plt.title('%s' % message)
	ax = sns.heatmap(np.array(locationProbs), annot=True, cmap="YlGnBu", linecolor='k', linewidths=1, xticklabels=['']*sizeHorizontal, yticklabels=['']*sizeVertical)
	fig.savefig('%s/%s.png' % (frameDir, message))
	plt.close()
	if debug:	locationPrint = overlayWorldMap(worldMap, locationProbs)
	else:		locationPrint = locationProbs
	for cell in locationPrint:	print cell
	print '\n'

def generalStep(probMoveIsSuccessful, probSensorIsRight, worldMap, frameDir):
	def step(move, measurement, locationProbs, message):
		if measurement not in ['green', 'red']:
			raise ValueError('color does not exist')
		locationAfterMove = executeMove(move, probMoveIsSuccessful, locationProbs)
		posteriorLocation = localize(measurement, probSensorIsRight, overlayWorldMap(worldMap, locationAfterMove))
		locationPrinter(worldMap, posteriorLocation, message, frameDir, True)
		return posteriorLocation
	return step

