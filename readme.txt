A short explanation of State1 and Show1 files and how to use them.

We suggest to run the program once or twice before reading this file.
Except for very simple functions, each function is documented in it's beginning.

State1:
The file starts with the "building" of the room- the room is simply a 2-d int array (which in python is implemented as list of lists), such that the i,j-th cell represents what is the i,j-th square of the room (in the graphical display). The number 'num' in the cell, will be the object COLOR_DICT[num] (the variable COLOR_DICT is defined in the head of Show1). The initialization includes the robot's and basket's positions, but those can be changed in order to check that your program works regardless of initial position of those objects. In addition, the action rewards are initialized, and may be changed to see how it affects the robot's behavior.

The variable TRAN_PROB_MAT defines the distribution of what action will be done, given the action that was tried to be done. Notice the var OPS holds all possible actions for the robot to make. For all i,j, TRAN_PROB_MAT[i][j] = Prob (action taken = OPS[j] | action tried = OPS[i]). For example, you can see that when the robot tries to move up, it will succeed with prob of 0.8, will divert right or left with prob of 0.1 each, but it will definitely not go down.

The function initRoom initializes an empty room, surrounded in walls. Note that the room sizes include the outer walls. You may add obstacles (put '0' in the appropriate cell).

The scattering functions scatter the stains and the fruits in the room. You can do it manually, or let the program scatter them randomly.

Class State represents a specific state. A state is defined by the robot's, stains, and fruits positions and the number of fruits the robot holds. The variable allStates holds the state space.

In the end of State1 file, a random policy is initialized. As it is now, you can see that some of the actions cannot be chosen: this is done to make sure that a movement action will be chosen and you'll be able to see the change in the GUI. You might want to make some changes (such as initializing a policy that will always go up), to understand how it works.