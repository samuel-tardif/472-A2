import rushHour as rh
import time

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

    #Start the clock
    st = time.time()

    #Print header
    f = open(solFileName, "a")
    f.write("Initial configuration of the board: "+startState)
    f.write("\n\n")
    f.write(startState[0:6]+"\n")
    f.write(startState[6:12] + "\n")
    f.write(startState[12:18] + "\n")
    f.write(startState[18:24] + "\n")
    f.write(startState[24:30] + "\n")
    f.write(startState[30:36] + "\n")
    f.write("\n")
    f.write("Fuel available to each car: \t")
    for car in rh.listOfCars(startState):
        f.write(car+": " + str(rh.getFuelForCar(car, startState)) + ", ")

    f.write("\n\n")
    f.close()

    while openList != []:

        counter += 1
        print("start of while loop")
        print("There are " + str(len(openList)) + " elements in openlist")
        current = openList.pop(0)
        print("There are " + str(len(openList)) + " elements in openlist")

        print(current.state)

        if rh.isSolution(current.state):
            #We found it
            solution = returnSolutionPath(current)
            solutionString = solutionAsString(solution)
            print(solutionString)
            #TO DO SOLUTION FILE
            f = open(solFileName, "a")
            f.write("Runtime: "+ str(time.time()-st)+"\n")
            f.write("Length of search path: "+str(counter)+"\n")
            f.write("Length of solution path: " + str(len(solution))+"\n")
            f.write("Solution path: "+solutionString+"\n\n")
            for node in solution:
                f.write(node.move + "\t" + str(rh.getFuelForCar(node.move[0],node.state)) + "\t" + node.state + "\n")

            #Final state
            f.write("\n\n")
            f.write(current.state[0:6] + "\n")
            f.write(current.state[6:12] + "\n")
            f.write(current.state[12:18] + "\n")
            f.write(current.state[18:24] + "\n")
            f.write(current.state[24:30] + "\n")
            f.write(current.state[30:36] + "\n")
            f.write("\n")
            f.close()

            #TO DO ADD TO RESULT FILE
            #
            #
            #
            #
            #
            #

            #Do this so we stop looking
            return "Solution found: " + solution
        else:
            #Children of current
            children = []
            activeCars = rh.listOfCars(current.state)
            print("There are " + str(len(activeCars)) + " elements in list of cars")
            for car in activeCars:
                #Check if we can move right
                if rh.getCarRangeRight(car, current.state) > 0:
                    for dist in range(1,rh.getCarRangeRight(car, current.state)+1):
                        children.append(SearchNode(rh.moveCarRight(car, current.state, dist),
                                                   current.cost+dist,
                                                   str(car)+"\tright\t"+str(dist),
                                                   current,
                                                   0))
                # Check if we can move left
                if rh.getCarRangeLeft(car, current.state) > 0:
                    for dist in range(1, rh.getCarRangeLeft(car, current.state)+1):
                        children.append(SearchNode(rh.moveCarLeft(car, current.state, dist),
                                                   current.cost + dist,
                                                   str(car) + "\tleft\t" + str(dist),
                                                   current,
                                                   0))
                # Check if we can move up
                if rh.getCarRangeUp(car, current.state) > 0:
                    for dist in range(1, rh.getCarRangeUp(car, current.state)+1):
                        children.append(SearchNode(rh.moveCarUp(car, current.state, dist),
                                                   current.cost + dist,
                                                   str(car) + "\tup\t" + str(dist),
                                                   current,
                                                   0))
                # Check if we can move down
                if rh.getCarRangeDown(car, current.state) > 0:
                    for dist in range(1, rh.getCarRangeDown(car, current.state)+1):
                        children.append(SearchNode(rh.moveCarDown(car, current.state, dist),
                                                    current.cost + dist,
                                                    str(car) + "\tdown\t" + str(dist),
                                                    current,
                                                    0))

            #Add current to closed list
            closedList.append(current)

            print("There are " + str(len(children)) + " nodes in children list")
            for child in children:
                print(child.state)
            #Check if children are in closed
            for child in children:
                for node in closedList:
                    if rh.areStatesSame(child.state, node.state):
                        children.remove(child)
                        break


            #Check if children are in open
            for child in children:
                for node in openList:
                    if rh.areStatesSame(child.state, node.state):
                        children.remove(child)
                        break

            #Insert in queue according to cost
            print("There are " + str(len(openList)) + " nodes in open list")
            print("Inserting "+str(len(children))+" nodes in open list")
            for child in children:
                if len(openList) == 0:
                    print("inserted 1")
                    print("Inserted state:" + child.state)
                    openList.append(child)
                else:
                    inserted = False
                    for i in range(0, len(openList)):
                        if child.cost <= openList[i].cost:
                            print("inserted 2")
                            print("Inserted state:" + child.state)
                            openList.insert(i, child)
                            inserted = True
                            break

                    if not inserted:
                        openList.append(child)
                        print("inserted3")
                        print("Inserted state:"+child.state)



            print("There are " + str(len(closedList)) + " nodes in closed list")
            print("There are " + str(len(openList)) + " nodes in open list")


    #NO solution was found
    #TO DO - Print solution file with no sol
    f = open(solFileName, "a")
    f.write("Runtime: " + str(time.time() - st) + "\n")
    f.write("Length of search path: " + str(counter) + "\n")
    f.write("No solution found")
    f.close()


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

            current = openList.pop(0)

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
    # Setting files for writing as we go
    algoName = "A*"

    for heur in heurList:

        solFileName = algoName + "-sol-" + str(heur) + name + ".txt"

        searchFileName = algoName + "-search-" + str(heur) + name + ".txt"

        # Setting up lists
        openList = [SearchNode(startState, 0, "", "none", heur(startState))]
        closedList = []

        # Counter to know how many nodes we explore
        counter = 0
        solutionFound = False

        while openList != []:

            counter += 1

            current = openList.pop(0)

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
                            children.append(SearchNode(newState,
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

                # Insert in queue according to f = cost + heur
                for child in children:
                    if len(openList) == 0:
                        openList.append(child)
                    else:
                        for i in range(0, len(openList)):
                            if child.heur+child.cost <= openList[i].heur+openList.heur:
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


def returnSolutionPath(solutionNode):
    solutionPath = [solutionNode]
    current = solutionNode
    while current.prev != "none":
        current = current.prev
        solutionPath.append(0, current)
    return solutionPath

def solutionAsString(solutionPath):
    solutionString = ""
    for node in solutionPath:
        solutionString.append(node.move+", ")
    return solutionString

