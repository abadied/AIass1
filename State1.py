import random
import copy
import numpy as np
import Show1

heightInput = ""
widthInput = ""
while not heightInput in range(4,20):
    try:
        heightInput = int(raw_input("Enter the height of the room between 4 to 20 (walls included): "))
    except:
        print "You have to insert a number between 4 to 20."
        continue
while not widthInput in range(4,20):
    try:
        widthInput = int(raw_input("Enter the width of the room between 4 to 20 (walls included): "))
    except:
        print "You have to insert a number between 4 to 20."
        continue

room = []
roomHeight = heightInput # walls included
roomWidth = widthInput # walls included
OPS = ["up", "down", "left", "right", "clean", "pick", "putInBasket", "random", "idle"]
ROBOT_POSITION = 2, 1
BASKET_POSITION = [1, 2]

# the i-j cell in the transition probability matrix indicates the probability to do action j given that the chosen action is i
# the matrix is ordered according to the order in OPS
TRAN_PROB_MAT = [[0.8, 0, 0.1, 0.1, 0, 0, 0, 0, 0],
                 [0, 0.8, 0.1, 0.1, 0, 0, 0, 0, 0],
                 [0.1, 0.1, 0.8, 0, 0, 0, 0, 0, 0],
                 [0.1, 0.1, 0, 0.8, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0.8, 0, 0, 0, 0.2],
                 [0, 0, 0, 0, 0, 0.8, 0, 0, 0.2],
                 [0, 0, 0, 0, 0, 0, 0.8, 0, 0.2],
                 [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0, 0.125],
                 [0, 0, 0, 0, 0, 0, 0, 0, 1]]

def initRoom():
    for i in range(roomHeight):
        newRow = [0] * roomWidth
        room.append(newRow)
    for i in range(1, roomHeight - 1):
        for j in range(1, roomWidth - 1):
            room[i][j] = 1
    walls = []
    # for i in range(1, roomWidth/2 - 2):                           # An option for walls in the room (minimal size 6*9
    #     walls.append([roomHeight / 2, i])                         #
    # for i in range(1, roomHeight/2 + 1):
    #     walls.append([i, roomWidth / 2])
    # for i in range(2):
    #     walls.append([roomHeight / 2, i + roomWidth/2 + 1])
    # for i in range(roomHeight / 2 + 3, roomHeight):
    #     walls.append([i, roomWidth / 2 + 2])
    # for [i, j] in walls:
    #     room[i][j] = 0
    room[ROBOT_POSITION[0]][ROBOT_POSITION[1]] = 9  # initial robot's location
    room[BASKET_POSITION[0]][BASKET_POSITION[1]] = 2  # initial basket's location

def printRoom(r):
    'prints the current room representation (for debugging)'
    for i in range((len(r))):
        print r[i]

def scatteringStains():
    i = 1
    while i <= numOfStains:
        num1 = random.randint(1, roomHeight - 2)
        num2 = random.randint(1, roomWidth - 2)
        if room[num1][num2] == 1:
            room[num1][num2] = 8
            i += 1

def userScatterring(num, str):
    scatteringCounter = 0
    while scatteringCounter < num:
        try:
            if str == "stain":
                inpStr = "Choose x-coordinate for the next stain: "
            else:
                inpStr = "Choose x-coordinate for the next fruit: "
            xCo = int(raw_input(inpStr))

            if not xCo in range(1, roomWidth - 1):
                print "x has to be a number between 1 to ", roomWidth - 1
                continue

            if str == "stain":
                inpStr = "Choose y-coordinate: "
            else:
                inpStr = "Choose y-coordinate: "
            yCo = int(raw_input(inpStr))

            if not yCo in range(1, roomHeight - 1):
                print "y has to be a number between 1 to ", roomHeight - 1
                continue

            if room[yCo][xCo] == 1:
                if str == "stain":
                    room[yCo][xCo] = 8
                else:
                    room[yCo][xCo] = random.randint(3, 5)
                scatteringCounter += 1
                printRoom(room)
            else:
                print "The cell (", xCo, ",", yCo, ") does not contain '1'. Choose another cell."

        except:
            print "Insert a number between 1 to ", roomHeight - 1, " for x and between 1 to ", roomWidth - 1, " for y."

def scatteringFruits():
    i = 1
    while i <= numOfFruits:
        num1 = random.randint(1, roomHeight - 2)
        num2 = random.randint(1, roomWidth - 2)
        if room[num1][num2] == 1:
            room[num1][num2] = random.randint(3, 5)
            i += 1

initRoom()

numOfStainsAndFruitsIsOK = False
numOfZeroes = 0
for i in range(roomHeight):
    for j in range(roomWidth):
        if room[i][j] == 0:
            numOfZeroes += 1

numOfStains = -1
numOfFruits = -1
while not numOfStainsAndFruitsIsOK:
    while not numOfStains in range(0,numOfZeroes):
        try:
            numOfStains = int(raw_input("How many stains would you like to scatter? "))
            if numOfStains > numOfZeroes:
                print "You can scatter only ", numOfZeroes, " stains."
        except:
            print "Wrong Input, please try again."
            continue
    while not numOfFruits in range(0,numOfZeroes):
        try:
            numOfFruits = int(raw_input("How many fruit would you like to scatter? "))
            if numOfFruits > numOfZeroes:
                print "You can scatter only ", numOfZeroes, " fruits."
        except:
            print "Wrong Input, please try again."
            continue
    if numOfStains + numOfFruits < numOfZeroes:
        numOfStainsAndFruitsIsOK = True
    else:
        numOfStains = 0
        numOfFruits = 0
        print "You can scatter only ", numOfZeroes, " stains and fruits totally. Lets try again."

whoScatters = ""
while not whoScatters in ["y", "n"]:
    try:
        whoScatters = raw_input("Would you like to decide the locations of the stains and fruits? (y/n) ")
    except:
        print 'The answer has to be "y" for yes or "n" for no.'
        continue
if whoScatters == "n":
    scatteringStains()
    scatteringFruits()
else:
    print "\nThe room situation is currently this:\n"
    printRoom(room)
    print "\nLets choose the location for the stains and the fruits.\n" \
          "You can choose any cell which contains '1'."
    userScatterring(numOfStains, "stain")
    userScatterring(numOfFruits, "fruit")

class State:
    "This class represents a specific state of the game - contains all parameters to fully characterize specific situation"

    def __init__(self):
        self.stateRoom = [[ROBOT_POSITION[0], ROBOT_POSITION[1]]]  # list of lists: lists for the robot coordinates, stains and fruits location
        stains = []
        fruits = []
        carriedFruits = 0  # num of fruits the robot is holding
        for i in range(len(room)):
            for j in range(len(room[0])):
                if room[i][j] == 8:
                    stains.append([i, j])
                if room[i][j] in [3, 4, 5]:
                    fruits.append([i, j])
        self.stateRoom.append(stains)
        self.stateRoom.append(fruits)
        self.stateRoom.append(carriedFruits)
        self.hash = repr(self.stateRoom)  # each stateRoom has a string that is it's name (and it's unique)
        self.end = len(self.stateRoom[1]) == 0 and len(self.stateRoom[2]) == 0 and self.stateRoom[3] == 0

    def isEnd(self):
        self.end = len(self.stateRoom[1]) == 0 and len(self.stateRoom[2]) == 0 and self.stateRoom[3] == 0
        return self.end

    def nextState(self, op):
        "givan a state and a legal operation, returns the next room's state"

        # should probably add here a transition matrix: given a chose action, what's the actions that might be done and their probabilities
        # note that this matrix will be a global variable
        newState = State()
        newState.stateRoom = copy.deepcopy(self.stateRoom[:])  # deep copy
        if op == "up":
            newState.stateRoom[0][0] = self.stateRoom[0][0] - 1
        elif op == "down":
            newState.stateRoom[0][0] = self.stateRoom[0][0] + 1
        elif op == "left":
            newState.stateRoom[0][1] = self.stateRoom[0][1] - 1
        elif op == "right":
            newState.stateRoom[0][1] = self.stateRoom[0][1] + 1
        elif op == "clean":  # remove a stain from the current position only if there's a stain there
            if self.stateRoom[0] in self.stateRoom[1]:
                index = self.stateRoom[1].index(self.stateRoom[0])
                newState.stateRoom[1] = newState.stateRoom[1][0:index] + newState.stateRoom[1][index + 1:]
                newState.end = newState.isEnd()
            else:
                return self
        elif op == "pick":  # pick a fruit from the current position only if there's a fruit there
            if self.stateRoom[0] in self.stateRoom[2]:
                index = self.stateRoom[2].index(self.stateRoom[0])
                newState.stateRoom[2] = newState.stateRoom[2][0:index] + newState.stateRoom[2][index + 1:]
                newState.stateRoom[3] += 1
                newState.end = newState.isEnd()
            else:
                return self
        elif op == "putInBasket":  # legalOp prevents putInBasket not in the basket
            newState.stateRoom[3] = 0
            newState.end = newState.isEnd()
        elif op == "idle":
            return self
        elif op == "random":
            legalOps = [op for op in OPS if self.legalOp(op)]
            return self.nextState(np.random.choice(legalOps))
        newState.hash = repr(newState.stateRoom)
        return newState

    def legalOp(self, op):
        if op == "idle":
            return True
        if self.isEnd():
            return False
        row_positionOfRobot = self.stateRoom[0][0]
        col_positionOfRobot = self.stateRoom[0][1]
        occupied = [0, 7, 10]  # these numbers represent wall, basket, cabinet and man appropriately
        if op == "up" and room[row_positionOfRobot - 1][col_positionOfRobot] not in occupied:
            return True
        elif op == "down" and room[row_positionOfRobot + 1][col_positionOfRobot] not in occupied:
            return True
        elif op == "left" and room[row_positionOfRobot][col_positionOfRobot - 1] not in occupied:
            return True
        elif op == "right" and room[row_positionOfRobot][col_positionOfRobot + 1] not in occupied:
            return True
        elif op in ["clean", "pick"]:
            return True
        elif op == "putInBasket" and self.stateRoom[0] == BASKET_POSITION:
            return True
        return False

    def printState(self):
        "just for debug"
        print("robot: ", self.stateRoom[0], ", stains: ", self.stateRoom[1], ", fruits: ", self.stateRoom[2])

def getAllStatesImpl(currentState, allStates):
    global FINAL_STATE
    for i in OPS:
        if currentState.legalOp(i):
            newState = currentState.nextState(i)
            if newState.hash not in allStates.keys():  # maybe it's better to use hash function in order to construct allStates
                allStates[newState.hash] = newState
                if not newState.isEnd():
                    getAllStatesImpl(newState, allStates)
                else:
                    FINAL_STATE = newState.hash

def getAllStates():
    currentState = State()
    allStates = dict()
    allStates[currentState.hash] = currentState
    getAllStatesImpl(currentState, allStates)
    return allStates
allStates = getAllStates()
print
# initial policy
policy = dict()
for key in allStates.keys():
    num = -1
    while num == -1:
        num = random.randint(0, len(OPS) - 1)
        if OPS[num] in ["random","pick","putInBasket","idle","clean"]:
            num = -1
    policy[key] = OPS[num]
    if allStates[key].isEnd():
        policy[key] = "idle"

initialState = State()

Show1.showRoom(room, policy, allStates, initialState, OPS, TRAN_PROB_MAT)