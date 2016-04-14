import itertools
import glob
import imageio
from LocationMatrix import LocationMatrix
#------------------------------------------------
worldMap = [['R', 'G', 'G', 'R', 'R'], ['R', 'R', 'G', 'R', 'R'], ['R', 'R', 'G', 'G', 'R'], ['R', 'R', 'R', 'R', 'R']]
#------------------------------------------------
sizeHorizontal, sizeVertical = len(worldMap[0]), len(worldMap)
assert [len(row) for row in worldMap] == [sizeHorizontal] * sizeVertical
#------------------------------------------------
probSensorIsRight = 0.7
probMoveIsSuccessful = 0.8
#------------------------------------------------
flatInitProb = 1 / (float(sizeHorizontal * sizeVertical))
flatRow = [flatInitProb for cell in range(sizeHorizontal)]
flatLandscape = list(itertools.repeat(flatRow, sizeVertical))
#------------------------------------------------
#locationPrinter(worldMap, flatLandscape, '0-INITIAL', True)

l0 = LocationMatrix(flatLandscape).localize('G', probSensorIsRight)

l1 = l0.executeMove('right', probMoveIsSuccessful).localize('G', probSensorIsRight)
l2 = l1.executeMove('down', probMoveIsSuccessful).localize('G', probSensorIsRight)
l3 = l2.executeMove('down', probMoveIsSuccessful).localize('G', probSensorIsRight)
l4 = l3.executeMove('right', probMoveIsSuccessful).localize('G', probSensorIsRight)

print l4.locationProbs

#------------------------------------------------
#step = generalStep(probMoveIsSuccessful, probSensorIsRight, worldMap)
#------------------------------------------------
#l0 = step('stay', 'G', flatLandscape, '1-STAY')
#l1 = step('right', 'G', l0, '2-RIGHT')
#l2 = step('down', 'G', l1, '3-DOWN')
#l3 = step('down', 'G', l2, '4-DOWN')
#l4 = step('right', 'G', l3, '5-RIGHT')
#------------------------------------------------
#allFrames = map(lambda img: imageio.imread(img), sorted(glob.glob('Frames/*.png'), key = lambda frame: int(frame.split('/')[1].split('-')[0])))
#imageio.mimwrite('Animation/animatedLocalizer.gif', allFrames, duration=[1.5]*len(allFrames))
#------------------------------------------------
