import random
import copy
import numpy as np
import Show1

# setting room's size
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
OPS = ["up", "down", "left", "right", "clean", "pick", "putInBasket", "random", "idle"] # optional actions for the agent to take
ROBOT_POSITION = 2, 1 # initial agent's position in the room. Can be changed.
BASKET_POSITION = [1, 2] # initial basket's position in the room. Can be changed.

# rewards for the various actions
CLEANING_CREDIT = 10.
PICKING_CREDIT = 5.
PUTTING_CREDIT = 20.
MOVE_COST = 1.
GAMMA = 0.9 # discount factor

# the i-j cell in the transition probability matrix indicates the probability to do action j given that the chosen action is i
# the matrix is ordered according to the order in the variable OPS
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
    "initialize the room according the given input."
    for i in range(roomHeight):
        newRow = [0] * roomWidth
        room.append(newRow)
    for i in range(1, roomHeight - 1):
        for j in range(1, roomWidth - 1):
            room[i][j] = 1
    # Obstacles might be added by putting '0' in the requested cell in the variable room.

    room[ROBOT_POSITION[0]][ROBOT_POSITION[1]] = 9  # initializing robot's location
    room[BASKET_POSITION[0]][BASKET_POSITION[1]] = 2  # initializing basket's location

def printRoom(r):
    'prints the current room (given as r) representation (for debugging)'
    for i in range((len(r))):
        print r[i]

def scatteringStains():
    "scattering numOfStains stains randomly"
    i = 1
    while i <= numOfStains:
        num1 = random.randint(1, roomHeight - 2)
        num2 = random.randint(1, roomWidth - 2)
        if room[num1][num2] == 1:
            room[num1][num2] = 8
            i += 1

def scatteringFruits():
    "scattering numOfFruits fruits randomly"
    i = 1
    while i <= numOfFruits:
        num1 = random.randint(1, roomHeight - 2)
        num2 = random.randint(1, roomWidth - 2)
        if room[num1][num2] == 1:
            room[num1][num2] = random.randint(3, 5)
            i += 1

def userScatterring(num, str):
    "this function allows the user to scatter the stains and fruits as he wishes."
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

initRoom()

# determining the number of empty cells to occupy with stains/fruits and scattering them in the room
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
        self.stateRoom = [[ROBOT_POSITION[0], ROBOT_POSITION[1]]]  # list of lists: list of robot coordinates, stains list, fruit list and num of carried fruits
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
        self.hash = repr(self.stateRoom)  # each stateRoom has a unique string to represent it
        self.end = len(self.stateRoom[1]) == 0 and len(self.stateRoom[2]) == 0 and self.stateRoom[3] == 0

    def isEnd(self):
        "checks if self is a state when all stains are cleaned and all fruits are in the basket"
        self.end = len(self.stateRoom[1]) == 0 and len(self.stateRoom[2]) == 0 and self.stateRoom[3] == 0
        return self.end

    def nextState(self, op):
        """givan a state and an operation to apply, computes the actual action taken,
            and returns the next room's state after applying the actual action"""
        global TRAN_PROB_MAT
        actionIndex = OPS.index(op)
        sample = np.random.uniform(0.000000001, 1.)
        sumProb = 0
        for i in range(len(OPS)):
            sumProb += TRAN_PROB_MAT[actionIndex][i]
            if sumProb > sample:
                realActionIndex = i
                break
        actualOp = OPS[realActionIndex]
        if not self.legalOp(actualOp):
            actualOp = "idle"
        newState = State()
        newState.stateRoom = copy.deepcopy(self.stateRoom[:])  # deep copy
        if actualOp == "up":
            newState.stateRoom[0][0] = self.stateRoom[0][0] - 1
        elif actualOp == "down":
            newState.stateRoom[0][0] = self.stateRoom[0][0] + 1
        elif actualOp == "left":
            newState.stateRoom[0][1] = self.stateRoom[0][1] - 1
        elif actualOp == "right":
            newState.stateRoom[0][1] = self.stateRoom[0][1] + 1
        elif actualOp == "clean":  # remove a stain from the current position only if there's a stain there
            if self.stateRoom[0] in self.stateRoom[1]:
                index = self.stateRoom[1].index(self.stateRoom[0])
                newState.stateRoom[1] = newState.stateRoom[1][0:index] + newState.stateRoom[1][index + 1:]
                newState.end = newState.isEnd()
            else:
                return self
        elif actualOp == "pick":  # pick a fruit from the current position only if there's a fruit there
            if self.stateRoom[0] in self.stateRoom[2]:
                index = self.stateRoom[2].index(self.stateRoom[0])
                newState.stateRoom[2] = newState.stateRoom[2][0:index] + newState.stateRoom[2][index + 1:]
                newState.stateRoom[3] += 1
                newState.end = newState.isEnd()
            else:
                return self
        elif actualOp == "putInBasket":  # legalOp prevents putInBasket not in the basket
            newState.stateRoom[3] = 0
            newState.end = newState.isEnd()
        elif actualOp == "idle":
            return self
        elif actualOp == "random":
            legalOps = [op for op in OPS if self.legalOp(op)]
            return self.nextState(np.random.choice(legalOps))
        newState.hash = repr(newState.stateRoom)
        return newState

    def actualNextState(self, op):
        """givan a state and an operation to apply, returns the next room's state if this action will be applied"""
        if not self.legalOp(op):
            op = "idle"
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
            return self.actualNextState(np.random.choice(legalOps))
        newState.hash = repr(newState.stateRoom)
        return newState

    def legalOp(self, op):
        "given an action, returns true iff the action can be done in this (self) state"
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

def getAllStatesImpl(currentState, allStates, value_func):
    "a recursive function to build the data structure allStates"
    global FINAL_STATE
    for i in OPS:
        if currentState.legalOp(i):
            newState = currentState.actualNextState(i)
            if newState.hash not in allStates.keys():  # maybe it's better to use hash function in order to construct allStates
                allStates[newState.hash] = newState
                value_func[newState.hash] = 0
                if not newState.isEnd():
                    getAllStatesImpl(newState, allStates, value_func)


def getAllStates():
    "building the data structure of all the states"
    currentState = State()
    allStates = dict()
    value_func = dict()
    allStates[currentState.hash] = currentState
    value_func[currentState.hash] = 0
    getAllStatesImpl(currentState, allStates, value_func)
    return allStates, value_func

allStates, value_func = getAllStates()
# for key in value_func.keys():
#     state = allStates[key]
#     if state.end:
#         value_func[key] = 10

def computeReward(state, action):
    """this function computes the reward of doing an action in a specific state (given that the robot succeeded to make it,
        i.e. this is the actual action taken)"""
    if action == "clean" and state.stateRoom[0] in state.stateRoom[1]:
        return CLEANING_CREDIT - MOVE_COST
    elif action == "pick" and state.stateRoom[0] in state.stateRoom[2]:
        return PICKING_CREDIT - MOVE_COST
    elif action == "putInBasket":
        return PUTTING_CREDIT * state.stateRoom[3] - MOVE_COST
    return - MOVE_COST

def getProbSAS(state1, state2, action):
    """"given state1 and action, returns the probability to reach state2
        in case that action is 'random' the function returns -1
        if state1 is a final state, than it leads by any action to itself in probability 1"""
    if action == 'random':
        return -1.0
    actionIndex = OPS.index(action)
    possibleActionsIndices = [numOp for numOp in range(len(OPS)) if TRAN_PROB_MAT[actionIndex][numOp] > 0]
    sum = 0.0
    for numOp in possibleActionsIndices:
        if state1.actualNextState(OPS[numOp]).hash == state2.hash:
            sum += TRAN_PROB_MAT[actionIndex][numOp]
    return sum


def computeExpectedReward(state, action):
    """given a state and an action that the robot tried to do (and not necessarily succeeded),
     returns the expectation of the received reward trying this action"""
    reward = 0
    for op in OPS:
        opProb = TRAN_PROB_MAT[OPS.index(action)][OPS.index(op)]
        reward += opProb * computeReward(state, op)
    return reward


# value iteration functions


# returns an optimal value function with gama variable set to 0.9
def value_iteration(epsilon, gamma):
    _policy = dict()
    while True:
        flag = True
        for key in allStates.keys():
            new_val, new_action_index = calc_value_and_action_for_curr_state(allStates[key], gamma)

            if abs(value_func[key] - new_val) >= epsilon:
                value_func[key] = new_val
                _policy[key] = OPS[new_action_index]
                flag = False
        if flag:
            break

    return _policy


# returns the best possible value and action index of a given state
def calc_value_and_action_for_curr_state(state, gamma):
    max_value = -1000
    best_action_index = None
    possible_states = get_possible_states(state)
    for i in range(len(OPS)):
        if state.legalOp(OPS[i]):
            action_reward = computeExpectedReward(state, OPS[i])
            sigma_param = 0

            for next_state_key in possible_states.keys():
                next_state = allStates[next_state_key]
                sigma_param += getProbSAS(state, next_state, OPS[i])*value_func[next_state_key]

            curr_reward = action_reward + gamma*sigma_param
            max_value = max(max_value, curr_reward)
            if max_value == curr_reward:
                best_action_index = i

    return max_value, best_action_index


# returns possible states test
def get_possible_states(state, defined_action=None):
    possible_states = dict()
    if defined_action is None:
        for op in OPS:
            if state.legalOp(op):
                _next_state = state.actualNextState(op)
                possible_states[_next_state.hash] = _next_state
    else:
        if state.legalOp(defined_action):
            _next_state = state.actualNextState(defined_action)
            possible_states[_next_state.hash] = _next_state
    return possible_states

# policy iteration functions


#  returns an optimal policy with gamma var set to 0.9
def policy_iteration(gamma):
    local_policy = get_random_policy()
    local_value_function = None
    while True:
        change = False
        local_value_function = get_value_function(local_policy, gamma,local_value_function)
        for state_key in allStates.keys():
            state = allStates[state_key]
            possible_states = get_possible_states(state)
            max_change = 0
            max_op = None
            for op in OPS:
                if op != local_policy[state_key] and state.legalOp(op):
                    action_reward = computeExpectedReward(state, op)
                    sigma_param = 0
                    for next_state_key in possible_states.keys():
                        next_state = allStates[next_state_key]
                        sigma_param += getProbSAS(state, next_state, op) * local_value_function[next_state_key]
                    curr_reward = action_reward + gamma * sigma_param
                    curr_change = curr_reward - local_value_function[state_key]
                    if curr_change > max_change:
                        max_change = curr_change
                        max_op = op

            if max_change > 0:
                print(state_key, max_op)
                local_policy[state_key] = max_op
                change = True
        if not change:
            break
    return local_policy


def get_value_function(_policy, gamma, _value_func=None):
    if _value_func is None:
        _value_func = dict()
        for key in allStates.keys():
            # TODO: check how to improve initial value function
             curr_state = allStates[key]
             if len(curr_state.stateRoom[2]) == 0 and len(curr_state.stateRoom[1]) == 0 and (curr_state.stateRoom[3] == 0):
                 _value_func[key] = 10
             elif len(curr_state.stateRoom[1])==0:
                 _value_func[key] = 0
             elif len(curr_state.stateRoom[2])==0:
                 _value_func[key] = 0
             else:
                _value_func[key] = 0
    for i in range (0,1):
    #while True:
        changed = False
        for state_key in allStates.keys():
            curr_state = allStates[state_key]
            action = _policy[state_key]
            sigma_param = 0
            action_reward = computeExpectedReward(curr_state, action)
            possible_states = get_possible_states(curr_state)
            for next_state_key in possible_states.keys():
                next_state = allStates[next_state_key]
                sigma_param += getProbSAS(curr_state, next_state, action) * _value_func[next_state_key]
            curr_reward = action_reward + gamma * sigma_param
            if _value_func[state_key] != curr_reward:
                _value_func[state_key] = curr_reward
                changed = True
        if not changed:
            break
    return _value_func

# general function for both algorithms


# create the initial policy
def get_policy():
    algo_type = raw_input('For Value Iteration press \'v\', For Policy Iteration press \'p\': ')
    if algo_type == 'v':
        return value_iteration(0.01, 0.9)
    elif algo_type == 'p':
        return policy_iteration(0.9)
    else:
        raise ValueError('unknown planner')

def getAction(x,y,i,j):
    if(x>i):
        return "up"
    elif (x<j):
        return "down"
    elif (y>j):
        return "left"
    else:
        return "right"

def get_random_policy():
    policy = dict()
    for key in allStates.keys():
        curr_state = allStates[key]
        if(curr_state.stateRoom[0] in curr_state.stateRoom[1]):
            policy[key] = "pick"
        elif (curr_state.stateRoom[0] in curr_state.stateRoom[2]):
            policy[key] = "clean"
        elif (curr_state.legalOp("putInBasket") and (curr_state.stateRoom[3]) > 0):
            policy[key] = "putInBasket"
        elif(len (curr_state.stateRoom[1]) == 0 and len (curr_state.stateRoom[2]) == 0 and (curr_state.stateRoom[3]==0)):
            policy[key] = "idle"
        elif (len(curr_state.stateRoom[1])>0):
            policy[key] = getAction(curr_state.stateRoom[0][0],curr_state.stateRoom[0][1],curr_state.stateRoom[1][0][0],curr_state.stateRoom[1][0][1])
        elif (len(curr_state.stateRoom[2])>0):
            policy[key] = getAction(curr_state.stateRoom[0][0],curr_state.stateRoom[0][1],curr_state.stateRoom[2][0][0],curr_state.stateRoom[2][0][1])
        else:
            policy[key] = getAction(curr_state.stateRoom[0][0],curr_state.stateRoom[0][1],BASKET_POSITION[0],BASKET_POSITION[1])



     #   for op in OPS:
     #       curr_state = allStates[key]
     #       if curr_state.legalOp(op):
     #           if curr_state.end:
     #               policy[key] = 'idle'
     #           else:
     #               policy[key] = op
     #           break
    return policy


# initial policy
policy = get_policy()

initialState = State()

Show1.showRoom(room, policy, allStates, initialState, OPS, TRAN_PROB_MAT)