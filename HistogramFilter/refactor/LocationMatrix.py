import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

import seaborn as sns
import operator
from helperFunctions import measurementProcessor
import numpy as np

class LocationMatrix:

	worldMap = [['R', 'G', 'G', 'R', 'R'], ['R', 'R', 'G', 'R', 'R'], ['R', 'R', 'G', 'G', 'R'], ['R', 'R', 'R', 'R', 'R']]
	sizeHorizontal, sizeVertical = len(worldMap[0]), len(worldMap)	

	def __init__(self, locationProbs):
		self.locationProbs = locationProbs

	def overlayWorldMap(self):
		return map(lambda row: zip(self.worldMap[row], self.locationProbs[row]), range(self.sizeVertical))

	def executeMove(self, move, probMoveIsSuccessful):
		if move == 'stay':
			return LocationMatrix(self.locationProbs)
		if move == 'left' or move == 'right':
			return LocationMatrix(map(lambda locationRow: self.__horizontalMove(locationRow, move, probMoveIsSuccessful), self.locationProbs))
		elif move == 'up' or move == 'down':
			transposeLocationMatrix, transposeMove = self.__locationFlipper(self.locationProbs), 'right' if move == 'down' else 'left'
			transposedResult = self.__locationNormalizer(map(lambda locationRow: self.__horizontalMove(locationRow, transposeMove, probMoveIsSuccessful), transposeLocationMatrix))
			return LocationMatrix(self.__locationFlipper(transposedResult))
		else:
			raise ValueError('move not supported')

	def __locationFlipper(self, locationProbs):
		return map(list, zip(*locationProbs))

	def __locationNormalizer(self, locationProbs):
		normalizingConstant, sizeVertical_t = sum(map(sum, locationProbs)), len(locationProbs)
		if normalizingConstant == 0.0:	raise ValueError('worldMap probably inconsistent with measurements & moves')
		return [map(lambda cell: cell / normalizingConstant, locationProbs[row]) for row in range(sizeVertical_t)]	

	def __shift(self, locationRow, n, move):
        	if move == 'right':     pivot = len(locationRow) - n
        	else:                   pivot = n
        	return locationRow[pivot::] + locationRow[:pivot:]

	def __horizontalMove(self, locationRow, move, probMoveIsSuccessful):
        	failedMove = map(lambda cell: (1 - probMoveIsSuccessful) * cell, locationRow)
        	successfulMove = map(lambda cell: probMoveIsSuccessful * cell, self.__shift(locationRow, 1, move))
        	return map(operator.add, failedMove, successfulMove)

	def localize(self, measurement, probSensorIsRight):
		coLoc = self.overlayWorldMap()
		newLocation = map(measurementProcessor(measurement, probSensorIsRight), coLoc)
		return LocationMatrix(self.__locationNormalizer(newLocation))

	def printer(self, savingDirectory, message, debug=False):
		fig = plt.figure()
		ax = fig.add_subplot(111)
		plt.title('%s' % message)
		ax = sns.heatmap(np.array(self.locationProbs), annot=True, cmap="YlGnBu", linecolor='k', linewidths=1, xticklabels=['']*self.sizeHorizontal, yticklabels=['']*self.sizeVertical)
		fig.savefig('%s/%s.png' % (savingDirectory, message))
		plt.close()
		if debug:	locationPrint = self.overlayWorldMap()
		else:		locationPrint = self.locationProbs
		for cell in locationPrint:	print cell
		print '\n'

