import copy
import queue

import requests

search_list = ["BFS", "DFS", "UCS", "GS", "A*", "A*2"]
search = "UCS"
target_url = "https://www.cmpe.boun.edu.tr/~emre/courses/cmpe480/hw1/input1.txt"
txt = requests.get(target_url).text.splitlines()


class Node:
    def __init__(self, parentNode, state, action, pathCost, depth, name):
        self.parentNode = parentNode
        self.state = state
        self.action = action
        self.pathCost = pathCost
        self.depth = depth
        self.name = name


def dfs(state):
    stack = queue.LifoQueue()
    initialNode = Node(None, state, "", 0, 0, "")
    stack.put(initialNode)
    nodesRemoved = 0
    while True:
        if stack.empty():
            return 0
        currentNode = stack.get()
        nodesRemoved += 1
        if isGoal(currentNode):
            return currentNode, nodesRemoved
        newNodes = expandL(currentNode)
        for newNode in newNodes:
            stack.put(newNode)


def bfs(state):
    fQueue = queue.Queue()
    initialNode = Node(None, state, "", 0, 0, "")
    fQueue.put(initialNode)
    nodesRemoved = 0
    while True:
        if fQueue.empty():
            return 0
        currentNode = fQueue.get()
        nodesRemoved += 1
        if isGoal(currentNode):
            return currentNode, nodesRemoved
        newNodes = expandL(currentNode)
        for newNode in newNodes:
            fQueue.put(newNode)


def get_pathCost(node):
    return node.pathCost


def getMin(priorityQueue):
    min = get_pathCost(priorityQueue[0])
    node = priorityQueue[0]
    pq = priorityQueue[1:]
    for element in pq:
        pathCost = get_pathCost(element)
        if pathCost < min:
            min = pathCost
            node = element
        elif pathCost == min:
            node = tieBreak(node, element)
    return node


def getMinH1(priorityQueue):
    min = h1(priorityQueue[0])
    node = priorityQueue[0]
    pq = priorityQueue[1:]
    for element in pq:
        heuristic = h1(element)
        if heuristic < min:
            min = heuristic
            node = element
        elif heuristic == min:
            node = tieBreak(node, element)
    return node


def getMinF1(priorityQueue):
    min = f1(priorityQueue[0])
    node = priorityQueue[0]
    pq = priorityQueue[1:]
    for element in pq:
        heuristic = f1(element)
        if heuristic < min:
            min = heuristic
            node = element
        elif heuristic == min:
            node = tieBreak(node, element)
    return node


def getMinF2(priorityQueue):
    min = f2(priorityQueue[0])
    node = priorityQueue[0]
    pq = priorityQueue[1:]
    for element in pq:
        heuristic = f2(element)
        if heuristic < min:
            min = heuristic
            node = element
        elif heuristic == min:
            node = tieBreak(node, element)
    return node


def tieBreak(node1, node2):
    node1Name = node1.action.split(' ')[0]
    node2Name = node2.action.split(' ')[0]
    if node1Name < node2Name:
        return node1
    elif node2Name < node1Name:
        return node2
    node1Move = node1.action.split(' ')[1]
    node2Move = node2.action.split(' ')[1]
    order = {"left,": 1, "down,": 2, "right,": 3, "up,": 4}
    if order.get(node1Move) <= order.get(node2Move):
        return node1
    return node2


def ucs(state):
    priorityQueue = []
    initialNode = Node(None, state, "", 0, 0, "")
    priorityQueue.append(initialNode)
    nodesRemoved = 0
    while True:
        if not priorityQueue:
            return 0
        currentNode = getMin(priorityQueue)
        # print("action-->", currentNode.action)
        priorityQueue.remove(currentNode)
        nodesRemoved += 1
        if isGoal(currentNode):
            return currentNode, nodesRemoved
        newNodes = expandL(currentNode)
        for newNode in newNodes:
            priorityQueue.append(newNode)


def gs(state):
    priorityQueue = []
    initialNode = Node(None, state, "", 0, 0, "")
    priorityQueue.append(initialNode)
    nodesRemoved = 0
    while True:
        if not priorityQueue:
            return 0
        currentNode = getMinH1(priorityQueue)
        priorityQueue.remove(currentNode)
        nodesRemoved += 1
        if isGoal(currentNode):
            return currentNode, nodesRemoved
        newNodes = expandL(currentNode)
        for newNode in newNodes:
            priorityQueue.append(newNode)


def h1(node):
    rows = 0
    columns = 0
    for i in range(len(node.state)):
        for j in range(len(node.state[i])):
            if node.state[i][j] != ".":
                rows += 1
                break
    for i in range(len(node.state[0])):
        for j in range(len(node.state)):
            if node.state[j][i] != ".":
                columns += 1
                break
    return min(rows, columns) - 1


def h2(node):
    rows = 0
    columns = 0
    for i in range(len(node.state)):
        if node.state[i][0] != '.':
            rows += 2
            continue
        elif node.state[i][-1] != '.':
            rows += 4
            continue
        for j in range(len(node.state[i])):
            if node.state[i][j] != ".":
                rows += 1
                break
    for i in range(len(node.state[0])):
        if node.state[i][0] != '.':
            columns += 3
            continue
        for j in range(len(node.state)):
            if node.state[j][i] != ".":
                columns += 1
                break
    return min(rows, columns)


def f1(node):
    return node.pathCost + h1(node)


def f2(node):
    return node.pathCost + h2(node)


def aStar(state):
    priorityQueue = []
    initialNode = Node(None, state, "", 0, 0, "")
    priorityQueue.append(initialNode)
    nodesRemoved = 0
    while True:
        if not priorityQueue:
            return 0
        currentNode = getMinF1(priorityQueue)
        priorityQueue.remove(currentNode)
        nodesRemoved += 1
        if isGoal(currentNode):
            return currentNode, nodesRemoved
        newNodes = expandL(currentNode)
        for newNode in newNodes:
            priorityQueue.append(newNode)


def aStar2(state):
    priorityQueue = []
    initialNode = Node(None, state, "", 0, 0, "")
    priorityQueue.append(initialNode)
    nodesRemoved = 0
    while True:
        if not priorityQueue:
            return 0
        currentNode = getMinF2(priorityQueue)
        priorityQueue.remove(currentNode)
        nodesRemoved += 1
        if isGoal(currentNode):
            return currentNode, nodesRemoved
        newNodes = expandL(currentNode)
        for newNode in newNodes:
            priorityQueue.append(newNode)


def expandL(node):
    successors = []
    letters = queue.PriorityQueue()
    for i in range(len(node.state)):
        for j in range(len(node.state[i])):
            if node.state[i][j] != ".":
                letters.put((node.state[i][j], i, j))

    while not letters.empty():
        name, i, j = letters.get()

        # left
        moveAmount = 0
        copyi = i
        copyj = j
        newState = copy.deepcopy(node.state)
        while copyj - 1 >= 0 and node.state[copyi][copyj - 1] != ".":
            moveAmount += 1
            newState[copyi][copyj - 1] = "."
            copyj -= 1
        if moveAmount != 0 and copyj - 1 >= 0:
            newState[copyi][copyj - 1] = newState[i][j]
            action = node.state[i][j] + " left, "
            newState[i][j] = "."
            newNode = Node(node, newState, action, node.pathCost + 4, node.depth + 1, node.name)
            successors.append(newNode)
        # down
        moveAmount = 0
        copyi = i
        copyj = j
        newState = copy.deepcopy(node.state)
        while copyi + 1 < len(node.state) and node.state[copyi + 1][copyj] != ".":
            moveAmount += 1
            newState[copyi + 1][copyj] = "."
            copyi += 1
        if moveAmount != 0 and copyi + 1 < len(node.state):
            newState[copyi + 1][copyj] = newState[i][j]
            action = node.state[i][j] + " down, "
            newState[i][j] = "."
            newNode = Node(node, newState, action, node.pathCost + 3, node.depth + 1, node.name)
            successors.append(newNode)

        # right
        moveAmount = 0
        copyi = i
        copyj = j
        newState = copy.deepcopy(node.state)
        while copyj + 1 < len(node.state[0]) and node.state[copyi][copyj + 1] != ".":
            moveAmount += 1
            newState[copyi][copyj + 1] = "."
            copyj += 1
        if moveAmount != 0 and copyj + 1 < len(node.state[0]):
            newState[copyi][copyj + 1] = newState[i][j]
            action = node.state[i][j] + " right, "
            newState[i][j] = "."
            newNode = Node(node, newState, action, node.pathCost + 2, node.depth + 1, node.name)
            successors.append(newNode)

        # up
        moveAmount = 0
        copyi = i
        copyj = j
        newState = copy.deepcopy(node.state)
        while copyi - 1 >= 0 and node.state[copyi - 1][copyj] != ".":
            moveAmount += 1
            newState[copyi - 1][copyj] = "."
            copyi -= 1
        if moveAmount != 0 and copyi - 1 >= 0:
            newState[copyi - 1][copyj] = newState[i][j]
            #action = node.state[i][j] + " up, " + str(moveAmount) + " times. "
            action = node.state[i][j] + " up, "
            newState[i][j] = "."
            newNode = Node(node, newState, action, node.pathCost + 1, node.depth + 1, node.name)
            successors.append(newNode)

    # for row in node.state:
    #    print(row)
    # for x in successors:
    #    print(x.action)
    # print("--------")
    return successors


def isGoal(node):
    nofPegs = 0
    for row in (node.state):
        for element in row:
            if element != ".":
                nofPegs += 1
                if nofPegs > 1:
                    return False

    if nofPegs == 1:
        return True
    return False


def main():
    state = []
    for row in txt:
        state.append([char for char in row])

    if search == "BFS":
        solution, nodesRemoved = bfs(state)
    elif search == "DFS":
        solution, nodesRemoved = dfs(state)
    elif search == "UCS":
        solution, nodesRemoved = ucs(state)
    elif search == "GS":
        solution, nodesRemoved = gs(state)
    elif search == "A*":
        solution, nodesRemoved = aStar(state)
    else:
        solution, nodesRemoved = aStar2(state)

    path = ""
    pathCost = solution.pathCost
    while solution.parentNode is not None:
        path = solution.action + path
        solution = solution.parentNode

    print("Number of removed nodes: " + str(nodesRemoved))
    print("Path cost: " + str(pathCost))
    print("Solution: " + path)


main()
