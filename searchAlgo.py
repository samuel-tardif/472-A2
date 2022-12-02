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


class SearchNode:
    def __init__(self, state, cost, move, prev, heur):
        self.state = state
        self.cost = cost
        self.move = move
        self.prev = prev
        self.heur = heur

# AYYYYY

def searchUCS(name, startState):

    #Setting files for writing as we go
    algoName = "UCS"
    solFileName = algoName+"-sol-"+name+".txt"

    searchFileName = algoName+"-search-"+name+".txt"

    #Setting up lists
    openList = [SearchNode(startState,0,"","none",0)]
    closedList = []

    #Counter to know how many nodes we explore
    counter = 0

    while openList != []:

        counter += 1

        current = open.pop(0)

        if rh.isSolution(current.state):
            #We found it
            solution = returnSolutionPath(current)
            print(solution)
            #TO DO SOLUTION FILE
            #
            #
            #
            #
            #
            #
            #
            #
            #
            #


            #Do this so we stop looking
            return "Solution found: "+solution
        else:
            #Children of current
            children = []
            activeCars = rh.listOfCars(current.state)
            for car in activeCars:
                #Check if we can move right
                if rh.getCarRangeRight(car, current.state) > 0:
                    for dist in range(1,rh.getCarRangeRight(car, current.state)):
                        children.append(SearchNode(rh.moveCarRight(car,current.state,dist),
                                                   current.cost+dist,
                                                   str(car)+"\tright\t"+str(dist),
                                                   current,
                                                   0))
                # Check if we can move left
                if rh.getCarRangeLeft(car, current.state) > 0:
                    for dist in range(1, rh.getCarRangeLeft(car, current.state)):
                        children.append(SearchNode(rh.moveCarLeft(car, current.state, dist),
                                                   current.cost + dist,
                                                   str(car) + "\tleft\t" + str(dist),
                                                   current,
                                                   0))
                # Check if we can move up
                if rh.getCarRangeUp(car, current.state) > 0:
                    for dist in range(1, rh.getCarRangeUp(car, current.state)):
                        children.append(SearchNode(rh.moveCarUp(car, current.state, dist),
                                                   current.cost + dist,
                                                   str(car) + "\tup\t" + str(dist),
                                                   current,
                                                   0))
                # Check if we can move down
                if rh.getCarRangeDown(car, current.state) > 0:
                    for dist in range(1, rh.getCarRangeDown(car, current.state)):
                        children.append(SearchNode(rh.moveCarDown(car, current.state, dist),
                                                    current.cost + dist,
                                                    str(car) + "\tdown\t" + str(dist),
                                                    current,
                                                    0))

            #Add current to closed list
            closedList.append(current)

            #Check if children are in closed
            for child in children:
                for node in closedList:
                    if rh.areStatesSame(child.state, node.state):
                        children.remove(child)


            #Check if children are in open
            for child in children:
                for node in openList:
                    if rh.areStatesSame(child.state, node.state):
                        children.remove(child)

            #Insert in queue according to cost
            for child in children:
                if len(openList) == 0:
                    openList.append(child)
                else:
                    for i in range(0, len(openList)):
                        if child.cost <= openList[i].cost:
                            openList.insert(i, child)


    #NO solution was found
    #TO DO - Print solution file with no sol
    #
    #
    #
    #
    #
    #
    #

    print("no solution")
    return "No solution"

def searchGBFS(name, startState):
    # Setting files for writing as we go
    algoName = "GBFS"

    for heur in heurList:

        solFileName = algoName + "-sol-"+ str(heur) + name + ".txt"

        searchFileName = algoName + "-search-" + str(heur) + name + ".txt"

        # Setting up lists
        openList = [SearchNode(startState, 0, "", "none", heur(startState))]
        closedList = []

        # Counter to know how many nodes we explore
        counter = 0
        solutionFound = False

        while openList != []:

            counter += 1

            current = open.pop(0)

            if rh.isSolution(current.state):
                # We found it
                solution = returnSolutionPath(current)
                print(solution)
                # TO DO SOLUTION FILE
                #
                #
                #
                #
                #
                #
                #
                #
                #
                #

                # Do this so we stop looking
                openList = []
                solutionFound = True

            else:
                # Children of current
                children = []
                activeCars = rh.listOfCars(current.state)
                for car in activeCars:
                    # Check if we can move right
                    if rh.getCarRangeRight(car, current.state) > 0:
                        for dist in range(1, rh.getCarRangeRight(car, current.state)):
                            newState = rh.moveCarRight(car, current.state, dist)
                            children.append(SearchNode(newState ,
                                                       current.cost + dist,
                                                       str(car) + "\tright\t" + str(dist),
                                                       current,
                                                       heur(newState)))
                    # Check if we can move left
                    if rh.getCarRangeLeft(car, current.state) > 0:
                        for dist in range(1, rh.getCarRangeLeft(car, current.state)):
                            newState = rh.moveCarLeft(car, current.state, dist)
                            children.append(SearchNode(newState,
                                                       current.cost + dist,
                                                       str(car) + "\tleft\t" + str(dist),
                                                       current,
                                                       heur(newState)))
                    # Check if we can move up
                    if rh.getCarRangeUp(car, current.state) > 0:
                        for dist in range(1, rh.getCarRangeUp(car, current.state)):
                            newState = rh.moveCarUp(car, current.state, dist)
                            children.append(SearchNode(newState,
                                                       current.cost + dist,
                                                       str(car) + "\tup\t" + str(dist),
                                                       current,
                                                       heur(newState)))
                    # Check if we can move down
                    if rh.getCarRangeDown(car, current.state) > 0:
                        for dist in range(1, rh.getCarRangeDown(car, current.state)):
                            newState = rh.moveCarDown(car, current.state, dist)
                            children.append(SearchNode(newState,
                                                       current.cost + dist,
                                                       str(car) + "\tdown\t" + str(dist),
                                                       current,
                                                       heur(newState)))

                # Add current to closed list
                closedList.append(current)

                # Check if children are in closed
                for child in children:
                    for node in closedList:
                        if rh.areStatesSame(child.state, node.state):
                            children.remove(child)

                # Check if children are in open
                for child in children:
                    for node in openList:
                        if rh.areStatesSame(child.state, node.state):
                            children.remove(child)

                # Insert in queue according to heur
                for child in children:
                    if len(openList) == 0:
                        openList.append(child)
                    else:
                        for i in range(0, len(openList)):
                            if child.heur <= openList[i].heur:
                                openList.insert(i, child)

        if not solutionFound:
            # NO solution was found
            # TO DO - Print solution file with no sol
            #
            #
            #
            #
            #
            #
            #

            print("no solution")


def searchA(name, startState):
    return


def returnSolutionPath(solutionNode):
    return
