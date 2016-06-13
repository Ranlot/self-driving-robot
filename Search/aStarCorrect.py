from operator import add, sub, itemgetter
import itertools
import numpy as np

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]

heuristic = [[9, 8, 7, 6, 5, 4],
            [8, 7, 6, 5, 4, 3],
            [7, 6, 5, 4, 3, 2],
            [6, 5, 4, 3, 2, 1],
            [5, 4, 3, 2, 1, 0]]

init = (0, 0)
goal = (len(grid)-1, len(grid[0])-1)
moveCost = 1

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
		
	#while True:
	for mv in range(25):

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

			if neighbor not in openCells: #add this neighbor to the open list
				openCells.append(neighbor)
			elif tentativeGscore >= gScoreValues[neighbor]:
				break #move on to next neighbor

			gScoreValues[neighbor] = tentativeGscore
			fScoreValues[neighbor] = tentativeGscore + manhattanHeuristicCost(neighbor, goal)
			cameFrom[neighbor] = currentCell

