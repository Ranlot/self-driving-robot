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
	print '\n'
	for row in grid:	print row
	print '\n'

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

def optimalPolicy(cell):
	cellX, cellY = extractXandY(cell)
	if cellX == goal[0] and cellY == goal[1]:
		policyMap[cellX][cellY] = '*'
		hasFlipped[cellX][cellY] = False #mutate back to False to indicate that this cell now has an optimal policy direction
	if hasFlipped[cellX][cellY]: #this cell has not flipped back; we need to find its optimal policy direction
		neighborValues = [{'goTo':(x,y), 'goToValue':valueGrid[x][y]} for (x, y) in neighborFinder(cell)]
		sortedNeighborValues = sorted(neighborValues, key=lambda x: x['goToValue'], reverse=False)
		bestNeighbor = sortedNeighborValues[0]['goTo']
		bestMove = tuple(map(sub, bestNeighbor, cell))
		policyMap[cellX][cellY] = allowedMovesNew[bestMove][0]

		policyMapX[cellX][cellY] = allowedMovesNew[bestMove][1][0]  #TODO: use only 1 set of allowedMoves
		policyMapY[cellX][cellY] = allowedMovesNew[bestMove][1][1]  #TODO: use only 1 set of allowedMoves

		hasFlipped[cellX][cellY] = False #mutate back to False to indicate that this cell now has an optimal policy direction
#-----------------------------------------------------------------
#-----------------------------------------------------------------
grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
	[0, 0, 0, 0, 1, 0]]

nrows, ncols = len(grid), len(grid[0])

init = [0, 0]
#goal = [nrows-3, ncols-1]
goal = [1, 4]

goalX, goalY = extractXandY(goal)

cost = 1 # the cost associated with moving from a cell to an adjacent one

allowedMoves = [[-1, 0 ], # go up
         	[ 0, -1], # go left
         	[ 1, 0 ], # go down
         	[ 0, 1 ]] # go right

allowedMovesNew = {(-1, 0): ['^', (0, 1)], (0, -1): ['<', (-1, 0)] , (1, 0): ['v', (0, -1)], (0, 1): ['>', (1, 0)]}

gridShower(grid)

valueGrid = [[99 for row in range(ncols)] for col in range(nrows)]
hasFlipped = [[False for row in range(ncols)] for col in range(nrows)]

valueGrid[goalX][goalY] = 0
hasFlipped[goalX][goalY] = True

change = True

fringeCells = [goal]
while change:
	change = False
	newFringeCells = []

	for originatingFringeCell in fringeCells:

		originatingX, originatingY = extractXandY(originatingFringeCell)
		possibleNeighbors = neighborFinder(originatingFringeCell)

		for neighbor in possibleNeighbors:

			neighborX, neighborY = extractXandY(neighbor)

			if not hasFlipped[neighborX][neighborY]:
				valueGrid[neighborX][neighborY] = valueGrid[originatingX][originatingY] + 1
				hasFlipped[neighborX][neighborY] = True
				change = True
		
			newFringeCells.append(neighbor)

	fringeCells = newFringeCells

gridShower(valueGrid)

allValidCells = flatMap(lambda rowIndex: [(rowIndex, colIndex) for (colIndex, cellValue) in enumerate(grid[rowIndex]) if cellValue == 0], range(nrows))
wallCells = flatMap(lambda rowIndex: [(rowIndex, colIndex) for (colIndex, cellValue) in enumerate(grid[rowIndex]) if cellValue == 1], range(nrows))

#re-use the hasFlipped structure.
#If a cell is valid and we got here then its flip status must have been set to True.  
#We can set it back to false to avoid duplication in the

policyMap = [['.' for row in range(ncols)] for col in range(nrows)]
policyMapX = [[0 for row in range(ncols)] for col in range(nrows)]
policyMapY = [[0 for row in range(ncols)] for col in range(nrows)]

#optimalPolicy does not return anything but is used to mutate the policyMap
map(optimalPolicy, allValidCells)

gridShower(policyMap)


xGrid = np.linspace(0, nrows-1, nrows)
yGrid = np.linspace(ncols-1, 0, ncols)
#xGrid, yGrid = np.meshgrid(xGrid, yGrid)


plotGridConverter = lambda (x, y): (y, nrows - 1 - x)

convertedGoal = plotGridConverter(goal)
convertedWallCells = map(plotGridConverter, wallCells)

fig = plt.figure()
q = plt.quiver(xGrid, yGrid, policyMapX, policyMapY, pivot='middle', headwidth=4, headlength=6)
#http://www.w3schools.com/colors/colors_names.asp
plt.text(convertedGoal[0], convertedGoal[1], 'goal', size=18, rotation=0., ha="center", va="center", bbox=dict(boxstyle="roundtooth",ec='limegreen',fc='lime',))
[plt.text(wall[0], wall[1], 'wall', size=18, rotation=0., ha="center", va="center", bbox=dict(boxstyle="round",ec='salmon',fc='sandybrown',)) for wall in convertedWallCells]
plt.xlim(-1, ncols); plt.ylim(-1, nrows)
plt.xticks([]); plt.yticks([])
fig.savefig('Search/Illustrations/dynamicProg_%d_%d.png' % (goalX, goalY))
plt.close()


