This project is largely inspired by the online course:
- Artificial Intelligence for Robotics: http://www.udacity.com/course/cs373

### 1) Localization

#### 1.a) Histogram Filter

Let's assume that we are in possession a map of the "world" as depicted on the left panel.  Our objective is to localize ourselves on this map.  

We can do this by assigning a probability to be in each cell as shown in the right panel.  In the absence of any information, our first guess is that we are equally likely to be anywhere in the world.  From then on, we can pinpoint our location more precisely by moving from cell to cell and using a sensor to measure the color of the cells as we go along.

Let's say for example that we are following the steps as in the animation (right, down, down, right).  In addition, we measure that we are in a green cell during all of our path.  Clearly, this will lead to a probability peak in the (row=3, col=4).  Note that the probability of being in this cell is only about 35% since we are accounting for the possibility of unsuccessful moves as well as sensor errors (same parameters as those discussed in the online lecture).  This makes this cell about 3 times more likely to be our location after all these moves and measurements compared to the second best possibility.

<p align="center">
<img src="HistogramFilter/Animation/worldMap.png" width="430"/>
<img src="HistogramFilter/Animation/animatedLocalizer.gif" width="430"/>
</p>

#### 2.b) Kalman Filter
