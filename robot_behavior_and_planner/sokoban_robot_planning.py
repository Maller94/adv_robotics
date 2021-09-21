import sys
import collections
import numpy as np
import heapq
import time

def transferToGameState(layout):
    """Transfer the layout of initial puzzle"""
    layout = [x.replace('\n', '') for x in layout]
    layout = [','.join(layout[i]) for i in range(len(layout))]
    layout = [x.split(',') for x in layout]
    maxColsNum = max([len(x) for x in layout])
    for irow in range(len(layout)):
        for icol in range(len(layout[irow])):
            if layout[irow][icol] == ' ':
                layout[irow][icol] = 0   # free space
            elif layout[irow][icol] == 'X':
                layout[irow][icol] = 1  # wall
            elif layout[irow][icol] == '@':
                layout[irow][icol] = 2  # robot
            elif layout[irow][icol] == '$':
                layout[irow][icol] = 3  # diamond
            elif layout[irow][icol] == '.':
                layout[irow][icol] = 4  # goal
            elif layout[irow][icol] == '*':
                layout[irow][icol] = 5  # diamond on goal
        colsNum = len(layout[irow])
        if colsNum < maxColsNum:
            layout[irow].extend([1 for _ in range(maxColsNum-colsNum)])
    return np.array(layout)


def PosOfPlayer(gameState):
    """Return the position of agent"""
    return tuple(np.argwhere(gameState == 2)[0])  # e.g. (2, 2)


def PosOfBoxes(gameState):
    """Return the positions of boxes"""
    return tuple(tuple(x) for x in np.argwhere((gameState == 3) | (gameState == 5)))  # e.g. ((2, 3), (3, 4), (4, 4), (6, 1), (6, 4), (6, 5))


def PosOfWalls(gameState):
    """Return the positions of walls"""
    return tuple(tuple(x) for x in np.argwhere(gameState == 1))  # e.g. like those above


def PosOfGoals(gameState):
    """Return the positions of goals"""
    return tuple(tuple(x) for x in np.argwhere((gameState == 4) | (gameState == 5)))  # e.g. like those above


def isEndState(posBox):
    """Check if all boxes are on the goals (i.e. pass the game)"""
    return sorted(posBox) == sorted(posGoals)


def isLegalAction(action, posPlayer):
    """Check if the given action is legal"""
    xPlayer, yPlayer = posPlayer
    if action[-1].isupper():  # the move was a push
        x1, y1 = xPlayer + 1 * action[0], yPlayer + 1 * action[1]
    else:
        x1, y1 = xPlayer + action[0], yPlayer + action[1]
    return (x1, y1) not in posWalls


def legalActions(posPlayer, posBox):
    """Return all legal actions for the agent in the current game state"""
    allActions = [[-2, 0, 'u', 'U'], [2, 0, 'd', 'D'],
                  [0, -2, 'l', 'L'], [0, 2, 'r', 'R']]
    xPlayer, yPlayer = posPlayer
    legalActions = []
    for action in allActions:
        x1, y1 = xPlayer + action[0], yPlayer + action[1]
        if (x1, y1) in posBox:  # the move was a push
            action.pop(2)  # drop the little letter
        else:
            action.pop(3)  # drop the upper letter
        if isLegalAction(action, posPlayer):
            legalActions.append(action)
        else:
            continue
    # e.g. ((0, -1, 'l'), (0, 1, 'R'))
    return tuple(tuple(x) for x in legalActions)


def updateState(posPlayer, posBox, action):
    """Return updated game state after an action is taken"""
    xPlayer, yPlayer = posPlayer  # the previous position of player
    newPosPlayer = [xPlayer + action[0], yPlayer +
                    action[1]]  # the current position of player
    posBox = [list(x) for x in posBox]
    if action[-1].isupper():  # if pushing, update the position of box
        posBox.remove(newPosPlayer)
        posBox.append([xPlayer + 2 * action[0], yPlayer + 2 * action[1]])
    posBox = tuple(tuple(x) for x in posBox)
    newPosPlayer = tuple(newPosPlayer)
    return newPosPlayer, posBox


def breadthFirstSearch():
    beginBox = PosOfBoxes(integerMap)
    beginPlayer = PosOfPlayer(integerMap)

    # e.g. ((2, 2), ((2, 3), (3, 4), (4, 4), (6, 1), (6, 4), (6, 5)))
    startState = (beginPlayer, beginBox)
    frontier = collections.deque([[startState]])  # store states
    actions = collections.deque([[0]])  # store actions
    exploredSet = set()
    moves = []
    while frontier:
        node = frontier.popleft()
        node_action = actions.popleft()
        if isEndState(node[-1][-1]):
            #print(','.join(node_action[1:]).replace(',', ''))
            moves.append(','.join(node_action[1:]).replace(',', ''))
            break
        if node[-1] not in exploredSet:
            exploredSet.add(node[-1])
            for action in legalActions(node[-1][0], node[-1][1]):
                newPosPlayer, newPosBox = updateState(
                    node[-1][0], node[-1][1], action)
                frontier.append(node + [(newPosPlayer, newPosBox)])
                actions.append(node_action + [action[-1]])
    moves = "".join(moves)
    moves_list = [char for char in moves]
    moves_list.append('done')
    return moves_list


# global variables
with open('mandatory_sokobanmaze.txt', "r") as f:
    layout = f.readlines()
integerMap = transferToGameState(layout)
posWalls = PosOfWalls(integerMap)
posGoals = PosOfGoals(integerMap)

def states_converted_to_robot():
    states = breadthFirstSearch()
    newStates = []
    tempArr1 = []
    tempArr2 = []
    for index,elem in enumerate(states):
        if elem.isupper() == True and tempArr1 == []:
            tempArr1.append(elem)
        elif elem.isupper() == True and elem in tempArr1:
            tempArr1.append(elem)
        elif elem.isupper() == True and elem not in tempArr1:
            tempArr2.append(elem)

        if elem.islower() == True:
            if tempArr1 != []:
                tempArr1.append(tempArr1[0])
                newStates.append(tempArr1)
                if tempArr1[0] == 'R':
                    tempArr1.append('l')
                elif tempArr1[0] == 'L':
                    tempArr1.append('r')
                elif tempArr1[0] == 'U':
                    tempArr1.append('d')
                elif tempArr1[0] == 'D':
                    tempArr1.append('u')
            if tempArr2 != []:
                tempArr2.append(tempArr2[0])
                newStates.append(tempArr2)
                if tempArr2[0] == 'R':
                    tempArr2.append('l')
                elif tempArr2[0] == 'L':
                    tempArr2.append('r')
                elif tempArr2[0] == 'U':
                    tempArr2.append('d')
                elif tempArr2[0] == 'D':
                    tempArr2.append('u')
            newStates.append([elem])
            tempArr1 = []
            tempArr2 = []
    finalStates = []
    for el in newStates:
        finalStates += el

    return finalStates

def run():
    print(states_converted_to_robot())
    with open('plan.txt','w') as w:
        w.write(str(states_converted_to_robot()))
run()
