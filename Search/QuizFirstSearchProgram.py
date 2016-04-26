from operator import add

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]

currentStatus = [{'weight': 0, 'position': [0, 0]}]

goal = [4, 5]

cost = 1

delta = [[-1, 0], # go up
         [ 0,-1], # go left
         [ 1, 0], # go down
         [ 0, 1]] # go right

listOfVisitedSites = [currentStatus[0]['position']]

extractXandY = lambda position: (position[0], position[1])

def validBoundaryChecker(position):
	xpos, ypos = extractXandY(position)
	return (xpos >= 0 and xpos < len(grid)) and (ypos >= 0 and ypos < len(grid[0]))

def gridWallChecker(position):
	xpos, ypos = extractXandY(position)
	return grid[xpos][ypos] == 0

def boundaryAndWallChecker(position):
	return validBoundaryChecker(position) and gridWallChecker(position)

def expandPositions(status):

	currentPosition = status['position']
	currentWeight = status['weight']

	possiblePositions = [map(add, currentPosition, move) for move in delta]
	boundaryAndWallFilter = filter(boundaryAndWallChecker, possiblePositions)
	previouslyVisitedFilter = filter(lambda position: position not in listOfVisitedSites, boundaryAndWallFilter)

	return [{'weight': currentWeight + cost, 'position': position} for position in previouslyVisitedFilter]

def processStatus(status):
	visitedSites = expandPositions(status)
	[listOfVisitedSites.append(site['position']) for site in visitedSites]
	return visitedSites

while True:
	print currentStatus
	currentStatus = sorted(currentStatus, key=lambda x: x['weight'])
	currentStatus = sum(map(processStatus, currentStatus), [])

	if True in [status['position'] == goal for status in currentStatus]:
		print 'Success', currentStatus		
		break

	if len(currentStatus) == 0:
		print 'Failure to find a path'
		break	

