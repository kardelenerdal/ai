import itertools

walls = "x xx  xx x"
sensors = ["on", "on", "off", "on"]

# your code starts
robot_pos = 0
robot_pos_prob = 0.0

sensor_length = len(sensors)
grid_length = len(walls)

evenRight = 0.8
evenStay = 0.2
oddRight = 0.6
oddStay = 0.4
sensorOnWallOn = 0.7
sensorOnWallOff = 0.2
sensorOffWallOn = 0.3
sensorOffWallOff = 0.8


def isWall(index):
    return walls[index - 1] is "x"


# 9 ('stay', 'stay', 'right', 'stay')
def calculateProbability(startIndex, actions):
    probability = 1.0
    index = startIndex
    actionIndex = 0
    for sensor in sensors:
        # sense
        if sensor is "on":
            if isWall(index):
                probability *= sensorOnWallOn
            else:
                probability *= sensorOnWallOff
        else:
            if isWall(index):
                probability *= sensorOffWallOn
            else:
                probability *= sensorOffWallOff
        # action
        if index is grid_length:
            continue
        if index % 2 is 0:
            if actions[actionIndex] is "stay":
                probability *= evenStay
            else:
                probability *= evenRight
                index += 1
        else:
            if actions[actionIndex] is "stay":
                probability *= oddStay
            else:
                probability *= oddRight
                index += 1
        actionIndex += 1
    return probability


def possibleActions(startIndex, endIndex):
    nofStays = sensor_length - (endIndex - startIndex)
    nofRights = sensor_length - nofStays
    actions = (["stay"] * nofStays) + (["right"] * nofRights)
    return set(itertools.permutations(actions))


start_end_actions = []
for end in range(1, grid_length + 1):
    for diff in range(sensor_length + 1):
        start = end - diff
        if start > 0:
            start_end_actions.append(((start, end), possibleActions(start, end)))

possibilities = [0] * grid_length

for (startIndex, endIndex), actions in start_end_actions:
    for actionSeq in actions:
        possibilities[endIndex - 1] += calculateProbability(startIndex, actionSeq)

robot_pos_prob = max(possibilities)
robot_pos = possibilities.index(robot_pos_prob) + 1

# your code ends

print('The most likely current position of the robot is', robot_pos, 'with probability',
      robot_pos_prob / sum(possibilities))
