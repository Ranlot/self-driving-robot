def measurementProcessor(measurement, probSensorIsRight):
	def processRow(colocationRow):
		return map(lambda cell: probSensorIsRight * cell[1] if cell[0] == measurement else (1 - probSensorIsRight) * cell[1], colocationRow)
	return processRow


