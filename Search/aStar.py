import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from operator import add, sub, itemgetter
import itertools
import numpy as np

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]

init = (0, 0)
goal = (4, 5)
moveCost = 1

nrows, ncols = len(grid), len(grid[0])

metaMoves = {(-1, 0): ['^', (0, 1)], (0, -1): ['<', (-1, 0)] , (1, 0): ['v', (0, -1)], (0, 1): ['>', (1, 0)]}

def flatMap(func, *iterable):
	return list(itertools.chain.from_iterable(map(func, *iterable)))

def closedCellsPerRow(row):
	return [(row, pos) for pos, val in enumerate(grid[row]) if val == 1]

def validBoundaryChecker(currentCell):
	x, y = currentCell
	return (x >= 0 and x < len(grid)) and (y >= 0 and y < len(grid[0]))

def validCell(currentCell, closedCells):
	return validBoundaryChecker(currentCell) and currentCell not in closedCells

def validNeighbors(currentCell, closedCells):
	potentialNeighbors = [tuple(map(add, [currentCell[0], currentCell[1]], move)) for move in metaMoves]
	return filter(lambda potentialNeighbor: validCell(potentialNeighbor, closedCells), potentialNeighbors)

def manhattanHeuristicCost(current, goal):
	return np.abs(current[0] - goal[0]) + np.abs(current[1] - goal[1])	

if __name__ == "__main__":

	gScoreValues, fScoreValues, cameFrom = {}, {}, {}

	closedCells = flatMap(closedCellsPerRow, range(len(grid)))

	gScoreValues[init] = 0
	fScoreValues[init] = gScoreValues[init] + manhattanHeuristicCost(init, goal)
	
	openCells = [init]
		
	while True:

		if len(openCells) == 0:
			print 'path does not exist'
			break

		#a) pick the best cell according to fCost
		currentCell = min(fScoreValues, key=lambda cell: fScoreValues[cell])		

		if currentCell == goal:
			print "finished"
			closedCells.append(goal)
			break

		#b) otherwise, remove current cell from open list and set it to closed
		openCells.remove(currentCell)
		fScoreValues.pop(currentCell)	
		
		#c) find all the neighbors of current cell
		allNeighbors = validNeighbors(currentCell, closedCells)

		#d) add the current cell to the list of closed cells
		closedCells.append(currentCell)

		for neighbor in allNeighbors:

			tentativeGscore = gScoreValues[currentCell] + moveCost

			if neighbor not in openCells: 
				openCells.append(neighbor)	#add this neighbor to the open list
			elif tentativeGscore >= gScoreValues[neighbor]:
				continue			#move on to next neighbor

			#we get here if the neighbor is new or the cost is better
			gScoreValues[neighbor] = tentativeGscore
			fScoreValues[neighbor] = tentativeGscore + manhattanHeuristicCost(neighbor, goal)
			cameFrom[neighbor] = currentCell

	#-----------------------------------------
	#best path reconstruction & plotting
	#-----------------------------------------

	policyMapX = [[0 for row in range(ncols)] for col in range(nrows)]
	policyMapY = [[0 for row in range(ncols)] for col in range(nrows)]

	backCell, backTrace = goal, [goal]
	while backCell in cameFrom.keys():
		arrivingCell = cameFrom[backCell]
		reconstructedMove = metaMoves[tuple(map(sub, backCell, arrivingCell))]
		policyMapX[arrivingCell[0]][arrivingCell[1]] = reconstructedMove[1][0]
		policyMapY[arrivingCell[0]][arrivingCell[1]] = reconstructedMove[1][1]
		backCell = arrivingCell

	xGrid = np.linspace(0, ncols-1, ncols)
	yGrid = np.linspace(nrows-1, 0, nrows)

	plotGridConverter = lambda (x, y): (y, nrows - 1 - x)
	convertedGoal = plotGridConverter(goal)
	wallCells = flatMap(lambda rowIndex: [(rowIndex, colIndex) for (colIndex, cellValue) in enumerate(grid[rowIndex]) if cellValue == 1], range(nrows))
	convertedWallCells = map(plotGridConverter, wallCells)

	fig = plt.figure()
	q = plt.quiver(xGrid, yGrid, policyMapX, policyMapY, pivot='middle', headwidth=4, headlength=6, scale=10.)
	plt.text(convertedGoal[0], convertedGoal[1], 'goal', size=18, rotation=0., ha="center", va="center", bbox=dict(boxstyle="roundtooth",ec='limegreen',fc='lime',))
	[plt.text(wall[0], wall[1], 'wall', size=18, rotation=0., ha="center", va="center", bbox=dict(boxstyle="round",ec='salmon',fc='sandybrown',)) for wall in convertedWallCells]
	plt.xlim(-1, ncols); plt.ylim(-1, nrows)
	plt.xticks([]); plt.yticks([]); fig.savefig('Search/Illustrations/aStar_%d_%d.png' % (goal[0], goal[1])); plt.close()

