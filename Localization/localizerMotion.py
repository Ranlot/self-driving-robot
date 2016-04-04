import itertools
#------------------------------------------------
def interLeaver(locationGrid):
	return map(lambda row: zip(colors[row], locationGrid[row]), range(sizeOfGrid))

def deInterLeaver(coLocationGrid):
	return [map(lambda cell: cell[1], row) for row in coLocationGrid]

#defining closure function
def measurementProcessor(measurement, probSensorIsRight):
	def processRow(colocationRow):
		return map(lambda cell: probSensorIsRight * cell[1] if cell[0] == measurement else (1 - probSensorIsRight) * cell[1], colocationRow)
	return processRow

#using numpy array would look more simple, yes...???
def locationNormalizer(locationMatrix):
	normalizingConstant = sum(map(sum, locationMatrix))
	return [map(lambda cell: cell / normalizingConstant, locationMatrix[row]) for row in range(sizeOfGrid)]	

def localize(measurement, coLoc):
	newLocation = locationNormalizer(map(measurementProcessor(measurement, sensor_right), coLoc))
	return interLeaver(newLocation)
#------------------------------------------------
sizeOfGrid = 3

colors = [['G', 'G', 'G'],
          ['G', 'R', 'G'],
          ['G', 'G', 'G']]

assert sum([len(colors[x]) == sizeOfGrid for x in range(sizeOfGrid)]) == sizeOfGrid
#------------------------------------------------
sensor_right = 1.0
p_move = 1.0
#------------------------------------------------
flatInitProb = 1 / (float(sizeOfGrid) ** 2)
flatRow = [flatInitProb for cell in range(sizeOfGrid)]
flatLandscape = list(itertools.repeat(flatRow, sizeOfGrid))
#------------------------------------------------
measurements = ['R']
motions = [[0, 0]]
#------------------------------------------------
initialCoLocation = interLeaver(flatLandscape)
#------------------------------------------------
result = localize(measurements[0], initialCoLocation)
print result
#------------------------------------------------

