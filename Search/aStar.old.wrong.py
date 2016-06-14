import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from operator import add, sub
import itertools
import numpy as np
#-----------------------------------------------------------------
#-----------------------------------------------------------------
def flatMap(func, *iterable):
	return list(itertools.chain.from_iterable(map(func, *iterable)))

def gridShower(grid):
	for row in grid:	print row
	print '\n'

def manhattanDistance(startPosition, targetPosition):
	return np.abs(startPosition[0] - targetPosition[0]) + np.abs(startPosition[1] - targetPosition[1])		

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
	possiblePositions = [map(add, position, move) for move in metaMoves]
	boundaryAndWallFilter = filter(boundaryAndWallChecker, possiblePositions)
	return boundaryAndWallFilter

def expandPositions(status):
	currentPosition = status['position']
	currentWeight = status['weight']
	boundaryAndWallFilter = neighborFinder(currentPosition)
	previouslyVisitedFilter = filter(lambda position: position not in closedSet, boundaryAndWallFilter)
	return [{'weight': currentWeight + 1, 'position': position} for position in previouslyVisitedFilter]
	#return [{'weight': currentWeight + naiveManhanttanHeuristics[position[0]][position[1]], 'position': position} for position in previouslyVisitedFilter]

def processStatus(status):
	visitedSites = expandPositions(status)
	[closedSet.append(site['position']) for site in visitedSites]
	return visitedSites

def findBestNeighborAndMove(weightGrid, position):
	neighbors = map(lambda cell: (weightGrid[cell[0]][cell[1]], cell), neighborFinder(position))
	neighbors = filter(lambda neighbor: weightGrid[neighbor[1][0]][neighbor[1][1]] != -1, neighbors) #-1 means unexpanded node
	neighbors.sort()
	bestNeighbor = neighbors[0][1]
	#bestMove = [move[0] for move in metaMoves if move[1] == map(sub, position, bestNeighbor)]
	#return {'bestNeighbor':bestNeighbor, 'bestMove':bestMove}
	return {'bestNeighbor':bestNeighbor, 'bestMove':map(sub, position, bestNeighbor)}

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

gridShower(grid)

#-----------------------------------------------------------------
metaMoves = {(-1, 0): ['^', (0, 1)], (0, -1): ['<', (-1, 0)] , (1, 0): ['v', (0, -1)], (0, 1): ['>', (1, 0)]}

init, goal = [0, 0], [4, 5]

goalX, goalY = extractXandY(goal)
#-----------------------------------------------------------------
allManhattanHeuristics = map(lambda x: manhattanDistance(x, goal), [(x, y) for x in range(nrows) for y in range(ncols)])
naiveManhanttanHeuristics = zip(*[iter(allManhattanHeuristics)] * ncols)
#naiveManhanttanHeuristics = [[1] * ncols for row in range(nrows)]
#gridShower(naiveManhanttanHeuristics)
#-----------------------------------------------------------------
openSet = [{'weight': naiveManhanttanHeuristics[init[0]][init[1]], 'position': init}]

closedSet = [openSet[0]['position']]

weightGrid = [[-1] * ncols for x  in range(nrows)]

xInit, yInit = extractXandY(closedSet[0])
weightGrid[xInit][yInit] = openSet[0]['weight']

finalSolvability = False

#print openSet
while True:
	openSet = expandNodes(openSet)
	#print openSet
	if len(openSet) == 0:
		print 'Failure to find a path'	
		break
	if True in [status['position'] == goal for status in openSet]:
		finalSolvability = True
		break


gridShower(weightGrid)

#start backwards propagation
if finalSolvability:

	policyMap = [['.'] * ncols for x  in range(nrows)]
	policyMap[goal[0]][goal[1]] = '*'

	policyMapX = [[0 for row in range(ncols)] for col in range(nrows)]
	policyMapY = [[0 for row in range(ncols)] for col in range(nrows)]

	backTrackPosition = goal

	while backTrackPosition != init:
		bestPath = findBestNeighborAndMove(weightGrid, backTrackPosition)
		backTrackPosition, backTrackMove = bestPath['bestNeighbor'], metaMoves.get(tuple(bestPath['bestMove']))

		policyMap[backTrackPosition[0]][backTrackPosition[1]] = backTrackMove[0]
		policyMapX[backTrackPosition[0]][backTrackPosition[1]] = backTrackMove[1][0]
		policyMapY[backTrackPosition[0]][backTrackPosition[1]] = backTrackMove[1][1]

	gridShower(policyMap)


#----------------------------
allValidCells = flatMap(lambda rowIndex: [(rowIndex, colIndex) for (colIndex, cellValue) in enumerate(grid[rowIndex]) if cellValue == 0], range(nrows))
wallCells = flatMap(lambda rowIndex: [(rowIndex, colIndex) for (colIndex, cellValue) in enumerate(grid[rowIndex]) if cellValue == 1], range(nrows))

xGrid = np.linspace(0, ncols-1, ncols)
yGrid = np.linspace(nrows-1, 0, nrows)

plotGridConverter = lambda (x, y): (y, nrows - 1 - x)

convertedGoal = plotGridConverter(goal)
convertedWallCells = map(plotGridConverter, wallCells)

fig = plt.figure()
q = plt.quiver(xGrid, yGrid, policyMapX, policyMapY, pivot='middle', headwidth=4, headlength=6, scale=10.)
#http://www.w3schools.com/colors/colors_names.asp
plt.text(convertedGoal[0], convertedGoal[1], 'goal', size=18, rotation=0., ha="center", va="center", bbox=dict(boxstyle="roundtooth",ec='limegreen',fc='lime',))
[plt.text(wall[0], wall[1], 'wall', size=18, rotation=0., ha="center", va="center", bbox=dict(boxstyle="round",ec='salmon',fc='sandybrown',)) for wall in convertedWallCells]
plt.xlim(-1, ncols); plt.ylim(-1, nrows)
plt.xticks([]); plt.yticks([])
fig.savefig('Search/Illustrations/aStar_%d_%d.png' % (goalX, goalY))
plt.close()

