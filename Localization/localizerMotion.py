import itertools
#------------------------------------------------
def overlayWorldMap(locationProbs):
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
	else:				pivot = n
	return locationRow[pivot::] + locationRow[:pivot:]

def horizontalMove(locationRow, move, probMoveIsSuccessful):
	failedMove = map(lambda cell: (1 - probMoveIsSuccessful) * cell, locationRow)
	successfulMove = map(lambda cell: probMoveIsSuccessful * cell, shift(locationRow, 1, move))
	return [x + y for (x, y) in zip(failedMove, successfulMove)]

def locationFlipper(locationProbs):
	return map(list, zip(*locationProbs))
	
def executeMove(move, locationProbs):
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

def locationPrinter(locationProbs, debug=False):
	if debug:	locationPrint = overlayWorldMap(locationProbs)
	else:		locationPrint = locationProbs
	for cell in locationPrint:	print cell
	print '\n'

def step(move, measurement, locationProbs):
	locationAfterMove = executeMove(move, locationProbs)
	posteriorLocation = localize(measurement, probSensorIsRight, overlayWorldMap(locationAfterMove))
	locationPrinter(posteriorLocation, True)
	return posteriorLocation
#------------------------------------------------
worldMap = [['R', 'G', 'G', 'R', 'R'], ['R', 'R', 'G', 'R', 'R'], ['R', 'R', 'G', 'G', 'R'], ['R', 'R', 'R', 'R', 'R']]
#------------------------------------------------
sizeHorizontal, sizeVertical = len(worldMap[0]), len(worldMap)
assert [len(row) for row in worldMap] == [sizeHorizontal] * sizeVertical
#------------------------------------------------
probSensorIsRight = 0.7
probMoveIsSuccessful = 0.8
#------------------------------------------------
flatInitProb = 1 / (float(sizeHorizontal * sizeVertical))
flatRow = [flatInitProb for cell in range(sizeHorizontal)]
flatLandscape = list(itertools.repeat(flatRow, sizeVertical))
#------------------------------------------------
measurements = ['R']
motions = [[0, 0]]
#------------------------------------------------
locationPrinter(flatLandscape, True)
l0 = step('stay', 'G', flatLandscape)
l1 = step('right', 'G', l0)
l2 = step('down', 'G', l1)
l3 = step('down', 'G', l2)
l4 = step('right', 'G', l3)
#------------------------------------------------
