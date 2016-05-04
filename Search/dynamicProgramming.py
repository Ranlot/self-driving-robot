from operator import add, sub
import itertools
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
goal = [nrows-1, ncols-1]

goalX, goalY = extractXandY(goal)

cost = 1 # the cost associated with moving from a cell to an adjacent one

allowedMoves = [[-1, 0 ], # go up
         	[ 0, -1], # go left
         	[ 1, 0 ], # go down
         	[ 0, 1 ]] # go right

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

