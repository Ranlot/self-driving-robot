import matplotlib.pyplot as plt

def plotMaker(index, xpos, ypos, frameDir):
	plMeasured = plt.scatter(xpos[:index], ypos[:index], c='black', marker='o', s=120, label='measured')
	plt.legend(loc='lower right', scatterpoints=1, shadow=True)
	plt.title('time = %d' % index); plt.grid()
	plt.xlabel('position in x'); plt.ylabel('position in y')
	plt.xlim([-0.3, 3.3]); plt.ylim([-0.3, 1.9])
	plt.savefig('%s/%d.png' % (frameDir, index))
	plt.close()


def plotPrediction(predictionTime, xpos, ypos, predictionX, predictionY, predictedXvelocity, predictedYvelocity, frameDir):
	plMeasured = plt.scatter(xpos, ypos, c='black', marker='o', s=120, label='measured')
	plPredicted = plt.scatter([predictionX], [predictionY], c='orange', marker='D', s=120, label='measured')
	plt.legend((plMeasured, plPredicted), ('measured', 'KF prediction\nx = %.1f; vx = %.1f\ny = %.1f ; vy = %.1f' % (predictionX, predictedXvelocity, predictionY, predictedYvelocity)), scatterpoints=1, loc='lower right')
	plt.title('time = %d ; Kalman Filter prediction' % predictionTime); plt.grid()
	plt.xlabel('position in x'); plt.ylabel('position in y')
	plt.xlim([-0.3, 3.3]); plt.ylim([-0.3, 1.9])
	plt.savefig('%s/%d.png' % (frameDir, predictionTime))
	plt.close()

