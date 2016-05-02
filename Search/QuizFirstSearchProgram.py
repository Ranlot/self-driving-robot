from operator import add, sub
from numpy import abs

#-----------------------------------------------------------------
#-----------------------------------------------------------------
def gridShower(grid):
	for row in grid:	print row
	print '\n'

def manhattanDistance(startPosition, targetPosition):
	return abs(startPosition[0] - targetPosition[0]) + abs(startPosition[1] - targetPosition[1])		

extractXandY = lambda position: (position[0], position[1])

def validBoundaryChecker(position):
	xpos, ypos = extractXandY(position)
	return (xpos >= 0 and xpos < len(grid)) and (ypos >= 0 and ypos < len(grid[0]))

def gridWallChecker(position):
	xpos, ypos = extractXandY(position)
	return grid[xpos][ypos] == 0

def boundaryAndWallChecker(position):
	return validBoundaryChecker(position) and gridWallChecker(position)

def neighborFinder(position):
	possiblePositions = [map(add, position, move) for move in allowedMoves]
	boundaryAndWallFilter = filter(boundaryAndWallChecker, possiblePositions)
	return boundaryAndWallFilter

def expandPositions(status):
	currentPosition = status['position']
	currentWeight = status['weight']
	boundaryAndWallFilter = neighborFinder(currentPosition)
	previouslyVisitedFilter = filter(lambda position: position not in closedSet, boundaryAndWallFilter)
	return [{'weight': currentWeight + naiveManhanttanHeuristics[position[0]][position[1]], 'position': position} for position in previouslyVisitedFilter]

def processStatus(status):
	visitedSites = expandPositions(status)
	[closedSet.append(site['position']) for site in visitedSites]
	return visitedSites

def findBestNeighborAndMove(weightGrid, position):
	neighbors = map(lambda cell: (weightGrid[cell[0]][cell[1]], cell), neighborFinder(position))
	neighbors = filter(lambda neighbor: weightGrid[neighbor[1][0]][neighbor[1][1]] != -1, neighbors) #-1 means unexpanded node
	neighbors.sort()
	bestNeighbor = neighbors[0][1]
	bestMove = [move[0] for move in metaMoves if move[1] == map(sub, position, bestNeighbor)]
	return {'bestNeighbor':bestNeighbor, 'bestMove':bestMove}

def expandNodes(openSet):
	sortedOpenSet = sorted(openSet, key=lambda x: x['weight'], reverse=False)
	bestCandidateForExansion = sortedOpenSet[0]
	xpos, ypos = extractXandY(bestCandidateForExansion['position'])
	weightGrid[xpos][ypos] = bestCandidateForExansion['weight']
	expandedSites = expandPositions(bestCandidateForExansion)
	[closedSet.append(site['position']) for site in expandedSites]
	newOpenSet = openSet[1:] + expandedSites
	newOpenSet = sorted(newOpenSet, key=lambda x: x['weight'], reverse=False)
	return newOpenSet
#-----------------------------------------------------------------
#-----------------------------------------------------------------

'''
grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 1, 0]]
'''

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]

nrows, ncols = len(grid), len(grid[0])

#-----------------------------------------------------------------
metaMoves = [('^', [-1, 0]), ('<', [0, -1]), ('v', [1, 0]), ('>', [0, 1])]
init, goal = [0, 0], [4, 5]
#-----------------------------------------------------------------
allManhattanHeuristics = map(lambda x: manhattanDistance(x, goal), [(x, y) for x in range(nrows) for y in range(ncols)])
naiveManhanttanHeuristics = zip(*[iter(allManhattanHeuristics)] * ncols)
#naiveManhanttanHeuristics = [[1] * ncols for row in range(nrows)]
gridShower(naiveManhanttanHeuristics)
#-----------------------------------------------------------------
openSet = [{'weight': naiveManhanttanHeuristics[init[0]][init[1]], 'position': init}]

allowedMoves = [move[1] for move in metaMoves]
closedSet = [openSet[0]['position']]


weightGrid = [[-1]*6 for x  in range(5)]

xInit, yInit = extractXandY(closedSet[0])
weightGrid[xInit][yInit] = openSet[0]['weight']

finalSolvability = False

print openSet
while True:
	openSet = expandNodes(openSet)
	print openSet
	if len(openSet) == 0:
		print 'Failure to find a path'	
		break
	if True in [status['position'] == goal for status in openSet]:
		finalSolvability = True
		break


gridShower(weightGrid)

#start backwards propagation
if finalSolvability:
	pathGrid = [[' ']*6 for x  in range(5)]
	pathGrid[goal[0]][goal[1]] = '*'
	backTrackPosition = goal
	while backTrackPosition != init:
		bestPath = findBestNeighborAndMove(weightGrid, backTrackPosition)
		backTrackPosition, backTrackMove = bestPath['bestNeighbor'], bestPath['bestMove'][0]
		pathGrid[backTrackPosition[0]][backTrackPosition[1]] = backTrackMove
	gridShower(pathGrid)

