import rushHour as rh


def heur1(state):
    aPos = state.index('A')
    heur = 0
    for i in range(0, 4 - aPos % 6):
        if not state[aPos + 2 + i] == '.':
            heur += 1
    return heur


def heur2(state):
    aPos = state.index('A')
    heur = 0
    carsPassed = []
    for i in range(0, 4 - aPos % 6):
        if not (state[aPos + 2 + i] == '.' | state[aPos + 2 + i] in carsPassed):
            carsPassed.append(state[aPos + 2 + i])
            heur += 1
    return heur


def heur3(state):
    lam = 3
    return lam * heur1(state)


def heur4(state):
    aPos = state.index('A')
    heur = 0
    carsPassed = []
    for i in range(0, 4 - aPos % 6):
        if not (state[aPos + 2 + i] == '.' | state[aPos + 2 + i] in carsPassed):
            carsPassed.append(state[aPos + 2 + i])
            heur += 1

            # Special condition
            carPassed = state[aPos + 2 + i]
            if rh.isCarVertical(carPassed, state):
                if rh.getCarRangeDown(carPassed, state) == 0 & rh.getCarRangeUp(carPassed, state) == 0:
                    heur += 1
            else:
                if rh.getCarRangeRight(carPassed, state) == 0 & rh.getCarRangeLeft(carPassed, state) == 0:
                    heur += 1
    return heur


heurList = [heur1, heur2, heur3, heur4]


def getSolution(finalSearchNode):
    return


class SearchNode:
    def __init__(self, state, cost, move, prev, heur):
        self.state = state
        self.cost = cost
        self.move = move
        self.prev = prev
        self.heur = heur

# AYYYYY

def searchUCS(state):
    return

def searchGBFS(state):
    return

def searchA(state):
    return
