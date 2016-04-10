import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

import itertools
import seaborn as sns
import numpy as np
import glob
import imageio

from helperFunctions import *
#------------------------------------------------
worldMap = [['R', 'G', 'G', 'R', 'R'], ['R', 'R', 'G', 'R', 'R'], ['R', 'R', 'G', 'G', 'R'], ['R', 'R', 'R', 'R', 'R']]
#------------------------------------------------
sizeHorizontal, sizeVertical = len(worldMap[0]), len(worldMap)
assert [len(row) for row in worldMap] == [sizeHorizontal] * sizeVertical
#------------------------------------------------
fig = plt.figure()
ax = fig.add_subplot(111, aspect=1.1)
worldMapForPlot = [map(lambda cell: 0 if cell == 'R' else 1, row) for row in worldMap]
plt.title('World Map')
ax = sns.heatmap(np.array(worldMapForPlot), cmap=ListedColormap(['red', 'green']), annot=False, cbar=True, linecolor='k', linewidths=1, xticklabels=['']*sizeHorizontal, yticklabels=['']*sizeVertical)
fig.savefig('Animation/worldMap.png')
plt.close()
#------------------------------------------------
probSensorIsRight = 0.7
probMoveIsSuccessful = 0.8
#------------------------------------------------
flatInitProb = 1 / (float(sizeHorizontal * sizeVertical))
flatRow = [flatInitProb for cell in range(sizeHorizontal)]
flatLandscape = list(itertools.repeat(flatRow, sizeVertical))
#------------------------------------------------
locationPrinter(worldMap, flatLandscape, '0-INITIAL', True)
#------------------------------------------------
step = generalStep(probMoveIsSuccessful, probSensorIsRight, worldMap)
#------------------------------------------------
l0 = step('stay', 'G', flatLandscape, '1-STAY')
l1 = step('right', 'G', l0, '2-RIGHT')
l2 = step('down', 'G', l1, '3-DOWN')
l3 = step('down', 'G', l2, '4-DOWN')
l4 = step('right', 'G', l3, '5-RIGHT')
#------------------------------------------------
allFrames = map(lambda img: imageio.imread(img), sorted(glob.glob('Frames/*.png'), key = lambda frame: int(frame.split('/')[1].split('-')[0])))
imageio.mimwrite('Animation/animatedLocalizer.gif', allFrames, duration=[1.5]*len(allFrames))
#------------------------------------------------
