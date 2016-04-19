import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

import itertools
import seaborn as sns
import numpy as np
import glob
import imageio
import os

from helperFunctions import *
#------------------------------------------------
frameDir, animationDir = 'HistogramFilter/Frames', 'HistogramFilter/Animation'
if not os.path.exists(frameDir):	os.makedirs(frameDir)
if not os.path.exists(animationDir):	os.makedirs(animationDir)
#------------------------------------------------
worldMap = [['red', 'green', 'green', 'red', 'red'], ['red', 'red', 'green', 'red', 'red'], ['red', 'red', 'green', 'green', 'red'], ['red', 'red', 'red', 'red', 'red']]
#------------------------------------------------
sizeHorizontal, sizeVertical = len(worldMap[0]), len(worldMap)
assert [len(row) for row in worldMap] == [sizeHorizontal] * sizeVertical
#------------------------------------------------
fig = plt.figure()
ax = fig.add_subplot(111, aspect=1.1)
worldMapForPlot = [map(lambda cell: 0 if cell == 'red' else 1, row) for row in worldMap]
plt.title('World Map')
ax = sns.heatmap(np.array(worldMapForPlot), cmap=ListedColormap(['red', 'green']), annot=False, cbar=True, linecolor='k', linewidths=1, xticklabels=['']*sizeHorizontal, yticklabels=['']*sizeVertical)
fig.savefig('HistogramFilter/Animation/worldMap.png')
plt.close()
#------------------------------------------------
probSensorIsRight = 0.7
probMoveIsSuccessful = 0.8
#------------------------------------------------
flatInitProb = 1 / (float(sizeHorizontal * sizeVertical))
flatRow = [flatInitProb for cell in range(sizeHorizontal)]
flatLandscape = list(itertools.repeat(flatRow, sizeVertical))
#------------------------------------------------
locationPrinter(worldMap, flatLandscape, '0-initial', frameDir, True)
#------------------------------------------------
step = generalStep(probMoveIsSuccessful, probSensorIsRight, worldMap, frameDir)
#------------------------------------------------
l0 = step('stay', 'green', flatLandscape, '1-stay-green')
l1 = step('right', 'green', l0, '2-right-green')
l2 = step('down', 'green', l1, '3-down-green')
l3 = step('down', 'green', l2, '4-down-green')
l4 = step('right', 'green', l3, '5-right-green')
#------------------------------------------------
allFrames = map(lambda img: imageio.imread(img), sorted(glob.glob('%s/*.png' % frameDir), key = lambda frame: int(frame.split('/')[2].split('-')[0])))
imageio.mimwrite('%s/animatedLocalizer.gif' % animationDir, allFrames, duration=[1.5]*len(allFrames))
#------------------------------------------------
