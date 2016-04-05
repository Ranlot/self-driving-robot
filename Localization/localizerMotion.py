import itertools
#------------------------------------------------
def interLeaver(locationGrid):
	return map(lambda row: zip(worldMap[row], locationGrid[row]), range(sizeVertical))

def deInterLeaver(coLocationGrid):
	return [map(lambda cell: cell[1], row) for row in coLocationGrid]

#defining closure function
def measurementProcessor(measurement, probSensorIsRight):
	def processRow(colocationRow):
		return map(lambda cell: probSensorIsRight * cell[1] if cell[0] == measurement else (1 - probSensorIsRight) * cell[1], colocationRow)
	return processRow

#using numpy array would look more simple, yes...???
def locationNormalizer(locationMatrix):
	normalizingConstant, sizeVertical = sum(map(sum, locationMatrix)), len(locationMatrix)
	if normalizingConstant == 0.0:	raise ValueError('worldMap probably inconsistent with measurements & moves')
	return [map(lambda cell: cell / normalizingConstant, locationMatrix[row]) for row in range(sizeVertical)]	

def localize(measurement, probSensorIsRight, coLoc):
	newLocation = locationNormalizer(map(measurementProcessor(measurement, probSensorIsRight), coLoc))
	return newLocation

def shift(locationRow, n, direction):
	if direction == 'right':	pivot = len(locationRow) - n
	else:				pivot = n
	return locationRow[pivot::] + locationRow[:pivot:]

def horizontalMove(locationRow, direction, probMoveIsSuccessful):
	failedMove = map(lambda cell: (1 - probMoveIsSuccessful) * cell, locationRow)
	successfulMove = map(lambda cell: probMoveIsSuccessful * cell, shift(locationRow, 1, direction))
	return [x + y for (x, y) in zip(failedMove, successfulMove)]

def locationFlipper(locationMatrix):
	return map(list, zip(*locationMatrix))
	
def executeMove(move, locationMatrix):
	if move == 'stay':
		return locationMatrix
	if move == 'left' or move == 'right':		
		return locationNormalizer(map(lambda locationRow: horizontalMove(locationRow, move, probMoveIsSuccessful), locationMatrix))
	elif move == 'up' or move == 'down':
		transposeLocationMatrix, transposeMove = locationFlipper(locationMatrix), 'right' if move == 'down' else 'left'
		transposedResult = locationNormalizer(map(lambda locationRow: horizontalMove(locationRow, transposeMove, probMoveIsSuccessful), transposeLocationMatrix))
		return map(list, zip(*transposedResult))
	else:
		raise ValueError('move not supported')

def locationPrinter(locationMatrix, debug=False):
	if debug:	locationPrint = interLeaver(locationMatrix)
	else:		locationPrint = locationMatrix
	for cell in locationPrint:	print cell
	print '\n'

def step(move, measurement, locationMatrix):
	makeTheMove = executeMove(move, locationMatrix)
	posteriorLocation = localize(measurement, probSensorIsRight, interLeaver(makeTheMove))
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
