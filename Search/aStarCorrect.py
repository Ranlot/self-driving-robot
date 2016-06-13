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

def validBoundaryChecker(x, y):
	return (x >= 0 and x < len(grid)) and (y >= 0 and y < len(grid[0]))

def validCell(x, y, closedCells):
	return validBoundaryChecker(x, y) and (x, y) not in closedCells

def validNeighbors(x, y, closedCells):
	potentialNeighbors = [tuple(map(add, [x, y], move)) for move in metaMoves]
	return filter(lambda pos: validCell(pos[0], pos[1], closedCells), potentialNeighbors)

def manhattanHeuristicCost(current, goal):
	return np.abs(current[0] - goal[0]) + np.abs(current[1] - goal[1])	
	#return 0

if __name__ == "__main__":

	gScoreValues, fScoreValues, cameFrom = {}, {}, {}

	#1) set the walls as closed cells (closed = True)
	#closedCells = map(initalWallCloser, grid)

	closedCells = flatMap(closedCellsPerRow, range(len(grid)))

	gScoreValues[init] = 0
	fScoreValues[init] = gScoreValues[init] + manhattanHeuristicCost(init, goal)
	
	openCells = [init]
		
	#closedcells[init[0]][init[1]] = true
	closedCells.append(init)

	#while True:
	for mv in range(25):

		#a) pick the best cell according to fCost
		currentCell = min(fScoreValues, key=lambda neighbor: fScoreValues[neighbor])		
		print currentCell

		print closedCells
		print '\n'

		#b) if this cell is the final cell, we are done
		if currentCell == goal:
			print "finished"
			#closedCells[goal[0]][goal[1]] = True
			closedCells.append(goal)
			print gScoreValues
			break

		#c) otherwise, remove current cell from open list and set it to closed
		openCells.remove(currentCell)
		fScoreValues.pop(currentCell)	
		
		currentX, currentY = currentCell
		#closedCells[currentX][currentY] = True
		closedCells.append(currentCell)
	
		#d) find all the neighbors of current cell
		allNeighbors = validNeighbors(currentX, currentY, closedCells)
		#allNeighbors = validNeighbors(currentX, currentY, closedCells)

		for neighbor in allNeighbors:

			tentativeGscore = gScoreValues[currentCell] + moveCost

			if neighbor not in openCells: #add this neighbor to the open list
				openCells.append(neighbor)
			elif tentativeGscore >= gScoreValues[neighbor]:
				break #move on to next neighbor

			gScoreValues[neighbor] = tentativeGscore
			fScoreValues[neighbor] = tentativeGscore + manhattanHeuristicCost(neighbor, goal)
			cameFrom[neighbor] = currentCell

