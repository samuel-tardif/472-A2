import rushHour as rh
import time
import copy

def heur1(state):
    if 'A' not in state:
        return 0

    aPos = state.index('A')
    heur = 0
    for i in range(0, 4 - aPos % 6):
        if not state[aPos + 2 + i] == '.':
            heur += 1
    return heur


def heur2(state):
    if 'A' not in state:
        return 0
    aPos = state.index('A')
    heur = 0
    carsPassed = []
    for i in range(0, 4 - aPos % 6):
        if not ((state[aPos + 2 + i] == '.') | (state[aPos + 2 + i] in carsPassed)):
            carsPassed.append(state[aPos + 2 + i])
            heur += 1
    return heur


def heur3(state):
    if 'A' not in state:
        return 0
    lam = 3
    return lam * heur1(state)


def heur4(state):
    if 'A' not in state:
        return 0
    aPos = state.index('A')
    heur = 0
    carsPassed = []
    for i in range(0, 4 - aPos % 6):
        if not ((state[aPos + 2 + i] == '.') | (state[aPos + 2 + i] in carsPassed)):
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




def searchUCS(name, startState):

    #Setting files for writing as we go
    algoName = "UCS"
    solFileName = algoName+"-sol-"+name+".txt"

    searchFileName = algoName+"-search-"+name+".txt"

    #Setting up lists
    openList = [SearchNode(startState,0,"-","none",0)]
    closedList = []

    #Counter to know how many nodes we explore
    counter = 0

    #Start the clock
    st = time.time()

    #Only print sol file for demo problems
    if "demo" in name:
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
        #print("\n\n--------------------------------------------------------------------")
        #print("start of while loop")
        #print("There are " + str(len(openList)) + " elements in openlist")
        current = openList.pop(0)
        #print("There are " + str(len(openList)) + " elements in openlist")

        #print(current.state)

        # Only print sol file for demo problems
        if "demo" in name:
            #Print to search list
            fs = open(searchFileName, "a")
            fs.write("0\t"+str(current.cost)+"\t0\t"+current.state+"\n")
            fs.close()

        if rh.isSolution(current.state):
            #We found it
            solution = returnSolutionPath(current)
            solutionString = solutionAsString(solution)
            print(solutionString)

            # Only print sol file for demo problems
            if "demo" in name:
                #SOLUTION FILE
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
            else:
                #Print results to spreadsheet
                fss = open("randomresults.txt", "a")
                fss.write(name + "\tUCS\tNA\t" + str(len(solution))+ "\t" + str(counter) + "\t" + str(time.time()-st)  + "\n")


            #Do this so we stop looking
            return "Solution found: " + str(solution)
        else:
            #Children of current
            children = []
            activeCars = rh.listOfCars(current.state)
            #print("There are " + str(len(activeCars)) + " elements in list of cars")
            for car in activeCars:
                #Check if we can move right
                #print("Range right: " + str(rh.getCarRangeRight(car, current.state)))
                if rh.getCarRangeRight(car, current.state) > 0:
                    for dist in range(1,rh.getCarRangeRight(car, current.state)+1):
                        children.append(SearchNode(rh.moveCarRight(car, current.state, dist),
                                                   current.cost+dist,
                                                   str(car)+"\tright\t"+str(dist),
                                                   current,
                                                   0))
                # Check if we can move left
                #print("Range left: " + str(rh.getCarRangeLeft(car, current.state)))
                if rh.getCarRangeLeft(car, current.state) > 0:
                    for dist in range(1, rh.getCarRangeLeft(car, current.state)+1):
                        children.append(SearchNode(rh.moveCarLeft(car, current.state, dist),
                                                   current.cost + dist,
                                                   str(car) + "\tleft\t" + str(dist),
                                                   current,
                                                   0))
                # Check if we can move up
                #print("Range up: " + str(rh.getCarRangeUp(car, current.state)))
                if rh.getCarRangeUp(car, current.state) > 0:
                    for dist in range(1, rh.getCarRangeUp(car, current.state)+1):
                        children.append(SearchNode(rh.moveCarUp(car, current.state, dist),
                                                   current.cost + dist,
                                                   str(car) + "\tup\t" + str(dist),
                                                   current,
                                                   0))
                # Check if we can move down
                #print("Range down: " + str(rh.getCarRangeRight(car, current.state)))
                if rh.getCarRangeDown(car, current.state) > 0:
                    for dist in range(1, rh.getCarRangeDown(car, current.state)+1):
                        children.append(SearchNode(rh.moveCarDown(car, current.state, dist),
                                                    current.cost + dist,
                                                    str(car) + "\tdown\t" + str(dist),
                                                    current,
                                                    0))

            #Add current to closed list
            closedList.append(current)

            #Check if children are in closed
            uniqueChildren = copy.deepcopy(children)
            for child in children:
                #print("Checking child: " + child.state + " vs closedList\n")
                for node in closedList:
                    #print("COmparing " + child.state + " and " + node.state)
                    if rh.areStatesSame(child.state, node.state):
                        #print("states are the same")
                        for elem in uniqueChildren:
                            if rh.areStatesSame(elem.state, child.state):
                                #print("Removing child")
                                uniqueChildren.remove(elem)
                        break


            children = copy.deepcopy(uniqueChildren)


            #Check if children are in open
            uniqueChildren = copy.deepcopy(children)
            for child in children:
                #print("Checking child: " + child.state + " vs openList")
                for node in openList:
                    #print("COmparing "+ child.state + " and "+ node.state)
                    if rh.areStatesSame(child.state, node.state):
                        #print("States are the same")
                        for elem in uniqueChildren:
                            if rh.areStatesSame(elem.state, child.state):
                                #print("Removing child")
                                uniqueChildren.remove(elem)
                        break


            children = copy.deepcopy(uniqueChildren)

            #Insert in queue according to cost
            #print("There are " + str(len(openList)) + " nodes in open list")
            #print("Inserting "+str(len(children))+" nodes in open list")
            for child in children:
                if len(openList) == 0:
                    #print("inserted 1")
                    #print("Inserted state:" + child.state)
                    openList.append(child)
                else:
                    inserted = False
                    for i in range(0, len(openList)):
                        if child.cost <= openList[i].cost:
                            #print("inserted 2")
                            #print("Inserted state:" + child.state)
                            openList.insert(i, child)
                            inserted = True
                            break

                    if not inserted:
                        openList.append(child)
                        #print("inserted 3")
                        #print("Inserted state:"+child.state)



            #print("There are " + str(len(closedList)) + " nodes in closed list")
            #print("There are " + str(len(openList)) + " nodes in open list")

    # Only print sol file for demo problems
    if "demo" in name:
        #NO solution was found
        f = open(solFileName, "a")
        f.write("Runtime: " + str(time.time() - st) + "\n")
        f.write("Length of search path: " + str(counter) + "\n")
        f.write("No solution found")
        f.close()

    return "No solution"

def searchGBFS(name, startState):
    # Setting files for writing as we go
    algoName = "GBFS"
    print("search GBFS")

    for heur in heurList:

        print("calculating sols with h " + str(heurList.index(heur)+1) + name)

        solFileName = algoName + "-sol-h"+ str(heurList.index(heur)+1) + "-" + name + ".txt"

        searchFileName = algoName + "-search-h" + str(heurList.index(heur)+1) + "-" + name + ".txt"

        # Setting up lists
        openList = [SearchNode(startState, 0, "-", "none", heur(startState))]
        closedList = []

        # Counter to know how many nodes we explore
        counter = 0

        solutionFound= False

        # Start the clock
        st = time.time()

        # Only print sol file for demo problems
        if "demo" in name:
            # Print header
            f = open(solFileName, "a")
            f.write("Initial configuration of the board: " + startState)
            f.write("\n\n")
            f.write(startState[0:6] + "\n")
            f.write(startState[6:12] + "\n")
            f.write(startState[12:18] + "\n")
            f.write(startState[18:24] + "\n")
            f.write(startState[24:30] + "\n")
            f.write(startState[30:36] + "\n")
            f.write("\n")
            f.write("Fuel available to each car: \t")
            for car in rh.listOfCars(startState):
                f.write(car + ": " + str(rh.getFuelForCar(car, startState)) + ", ")

            f.write("\n\n")
            f.close()

        while openList != []:

            counter += 1
            #print("\n\n--------------------------------------------------------------------")
            # print("start of while loop")
            # print("There are " + str(len(openList)) + " elements in openlist")
            current = openList.pop(0)
            # print("There are " + str(len(openList)) + " elements in openlist")

            # print(current.state)

            # Only print sol file for demo problems
            if "demo" in name:
                # Print to search list
                fs = open(searchFileName, "a")
                fs.write("0\t" + str(current.cost) + "\t" + str(heur(current.state)) + "\t" + current.state + "\n")
                fs.close()


            if rh.isSolution(current.state):
                # We found it
                solution = returnSolutionPath(current)
                solutionString = solutionAsString(solution)
                print(solutionString)

                # Only print sol file for demo problems
                if "demo" in name:
                    # TO DO SOLUTION FILE
                    f = open(solFileName, "a")
                    f.write("Runtime: " + str(time.time() - st) + "\n")
                    f.write("Length of search path: " + str(counter) + "\n")
                    f.write("Length of solution path: " + str(len(solution)) + "\n")
                    f.write("Solution path: " + solutionString + "\n\n")
                    for node in solution:
                        f.write(
                            node.move + "\t" + str(rh.getFuelForCar(node.move[0], node.state)) + "\t" + node.state + "\n")

                    # Final state
                    f.write("\n\n")
                    f.write(current.state[0:6] + "\n")
                    f.write(current.state[6:12] + "\n")
                    f.write(current.state[12:18] + "\n")
                    f.write(current.state[18:24] + "\n")
                    f.write(current.state[24:30] + "\n")
                    f.write(current.state[30:36] + "\n")
                    f.write("\n")
                    f.close()

                else:
                    # Print results to spreadsheet
                    fss = open("randomresults.txt", "a")
                    fss.write(
                        name + "\tGBFS\th" +str(heurList.index(heur)+1) + "\t" + str(len(solution))
                        + "\t" + str(counter) + "\t" + str(time.time() - st) + "\n")

                # Do this so we stop looking
                solutionFound = True
                break
            else:
                # Children of current
                children = []
                activeCars = rh.listOfCars(current.state)
                # print("There are " + str(len(activeCars)) + " elements in list of cars")
                for car in activeCars:
                    # Check if we can move right
                    # print("Range right: " + str(rh.getCarRangeRight(car, current.state)))
                    if rh.getCarRangeRight(car, current.state) > 0:
                        for dist in range(1, rh.getCarRangeRight(car, current.state) + 1):
                            children.append(SearchNode(rh.moveCarRight(car, current.state, dist),
                                                       current.cost + dist,
                                                       str(car) + "\tright\t" + str(dist),
                                                       current,
                                                       heur(rh.moveCarRight(car, current.state, dist))))
                    # Check if we can move left
                    # print("Range left: " + str(rh.getCarRangeLeft(car, current.state)))
                    if rh.getCarRangeLeft(car, current.state) > 0:
                        for dist in range(1, rh.getCarRangeLeft(car, current.state) + 1):
                            children.append(SearchNode(rh.moveCarLeft(car, current.state, dist),
                                                       current.cost + dist,
                                                       str(car) + "\tleft\t" + str(dist),
                                                       current,
                                                       heur(rh.moveCarLeft(car, current.state, dist))))
                    # Check if we can move up
                    # print("Range up: " + str(rh.getCarRangeUp(car, current.state)))
                    if rh.getCarRangeUp(car, current.state) > 0:
                        for dist in range(1, rh.getCarRangeUp(car, current.state) + 1):
                            children.append(SearchNode(rh.moveCarUp(car, current.state, dist),
                                                       current.cost + dist,
                                                       str(car) + "\tup\t" + str(dist),
                                                       current,
                                                       heur(rh.moveCarUp(car, current.state, dist))))
                    # Check if we can move down
                    # print("Range down: " + str(rh.getCarRangeRight(car, current.state)))
                    if rh.getCarRangeDown(car, current.state) > 0:
                        for dist in range(1, rh.getCarRangeDown(car, current.state) + 1):
                            children.append(SearchNode(rh.moveCarDown(car, current.state, dist),
                                                       current.cost + dist,
                                                       str(car) + "\tdown\t" + str(dist),
                                                       current,
                                                       heur(rh.moveCarDown(car, current.state, dist))))

                # Add current to closed list
                closedList.append(current)

                # Check if children are in closed
                uniqueChildren = copy.deepcopy(children)
                for child in children:
                    # print("Checking child: " + child.state + " vs closedList\n")
                    for node in closedList:
                        # print("COmparing " + child.state + " and " + node.state)
                        if rh.areStatesSame(child.state, node.state):
                            # print("states are the same")
                            for elem in uniqueChildren:
                                if rh.areStatesSame(elem.state, child.state):
                                    # print("Removing child")
                                    uniqueChildren.remove(elem)
                            break

                children = copy.deepcopy(uniqueChildren)

                # Check if children are in open
                uniqueChildren = copy.deepcopy(children)
                for child in children:
                    # print("Checking child: " + child.state + " vs openList")
                    for node in openList:
                        # print("COmparing "+ child.state + " and "+ node.state)
                        if rh.areStatesSame(child.state, node.state):
                            # print("States are the same")
                            for elem in uniqueChildren:
                                if rh.areStatesSame(elem.state, child.state):
                                    # print("Removing child")
                                    uniqueChildren.remove(elem)
                            break

                children = copy.deepcopy(uniqueChildren)

                # Insert in queue according to heur

                for child in children:
                    inserted = False
                    if len(openList) == 0:
                        openList.append(child)
                    else:
                        for i in range(0, len(openList)):
                            if child.heur <= openList[i].heur:
                                openList.insert(i, child)
                                inserted = True
                                break

                        if not inserted:
                            openList.append(child)

        if not solutionFound:
            # Only print sol file for demo problems
            if "demo" in name:
                # NO solution was found
                f = open(solFileName, "a")
                f.write("Runtime: " + str(time.time() - st) + "\n")
                f.write("Length of search path: " + str(counter) + "\n")
                f.write("No solution found")
                f.close()

            print("no solution")


def searchA(name, startState):
    # Setting files for writing as we go
    algoName = "A"

    print("search A")
    for heur in heurList:

        print("calculating sols with h " + str(heurList.index(heur) + 1) + name)

        solFileName = algoName + "-sol-h" + str(heurList.index(heur) + 1) + name + ".txt"

        searchFileName = algoName + "-search-" + str(heurList.index(heur)+1) + "-" + name + ".txt"

        # Setting up lists
        openList = [SearchNode(startState, 0, "-", "none", heur(startState))]
        closedList = []

        # Counter to know how many nodes we explore
        counter = 0

        solutionFound = False

        # Start the clock
        st = time.time()

        # Only print sol file for demo problems
        if "demo" in name:
            # Print header
            f = open(solFileName, "a")
            f.write("Initial configuration of the board: " + startState)
            f.write("\n\n")
            f.write(startState[0:6] + "\n")
            f.write(startState[6:12] + "\n")
            f.write(startState[12:18] + "\n")
            f.write(startState[18:24] + "\n")
            f.write(startState[24:30] + "\n")
            f.write(startState[30:36] + "\n")
            f.write("\n")
            f.write("Fuel available to each car: \t")
            for car in rh.listOfCars(startState):
                f.write(car + ": " + str(rh.getFuelForCar(car, startState)) + ", ")

            f.write("\n\n")
            f.close()

        while openList != []:

            counter += 1
            #print("\n\n--------------------------------------------------------------------")
            # print("start of while loop")
            # print("There are " + str(len(openList)) + " elements in openlist")
            current = openList.pop(0)
            # print("There are " + str(len(openList)) + " elements in openlist")

            # print(current.state)

            # Only print sol file for demo problems
            if "demo" in name:
                # Print to search list
                fs = open(searchFileName, "a")
                fs.write(str(heur(current.state)) + str(current.cost) +"\t" + str(current.cost) + "\t" + str(heur(current.state)) + "\t" + current.state + "\n")
                fs.close()

            if rh.isSolution(current.state):
                # We found it
                solution = returnSolutionPath(current)
                solutionString = solutionAsString(solution)
                print(solutionString)

                # Only print sol file for demo problems
                if "demo" in name:
                    # TO DO SOLUTION FILE
                    f = open(solFileName, "a")
                    f.write("Runtime: " + str(time.time() - st) + "\n")
                    f.write("Length of search path: " + str(counter) + "\n")
                    f.write("Length of solution path: " + str(len(solution)) + "\n")
                    f.write("Solution path: " + solutionString + "\n\n")
                    for node in solution:
                        f.write(
                            node.move + "\t" + str(rh.getFuelForCar(node.move[0], node.state)) + "\t" + node.state + "\n")

                    # Final state
                    f.write("\n\n")
                    f.write(current.state[0:6] + "\n")
                    f.write(current.state[6:12] + "\n")
                    f.write(current.state[12:18] + "\n")
                    f.write(current.state[18:24] + "\n")
                    f.write(current.state[24:30] + "\n")
                    f.write(current.state[30:36] + "\n")
                    f.write("\n")
                    f.close()
                else:
                    # Print results to spreadsheet
                    fss = open("randomresults.txt", "a")
                    fss.write(
                        name + "\tA*\th" +str(heurList.index(heur)+1) + "\t" + str(len(solution))
                        + "\t" + str(counter) + "\t" + str(time.time() - st) + "\n")

                # Do this so we stop looking
                solutionFound = True
                break
            else:
                # Children of current
                children = []
                activeCars = rh.listOfCars(current.state)
                # print("There are " + str(len(activeCars)) + " elements in list of cars")
                for car in activeCars:
                    # Check if we can move right
                    # print("Range right: " + str(rh.getCarRangeRight(car, current.state)))
                    if rh.getCarRangeRight(car, current.state) > 0:
                        for dist in range(1, rh.getCarRangeRight(car, current.state) + 1):
                            newState = rh.moveCarRight(car, current.state, dist)
                            children.append(SearchNode(newState,
                                                       current.cost + dist,
                                                       str(car) + "\tright\t" + str(dist),
                                                       current,
                                                       heur(newState)))
                    # Check if we can move left
                    # print("Range left: " + str(rh.getCarRangeLeft(car, current.state)))
                    if rh.getCarRangeLeft(car, current.state) > 0:
                        for dist in range(1, rh.getCarRangeLeft(car, current.state) + 1):
                            newState = rh.moveCarLeft(car, current.state, dist)
                            children.append(SearchNode(newState,
                                                       current.cost + dist,
                                                       str(car) + "\tleft\t" + str(dist),
                                                       current,
                                                       heur(newState)))
                    # Check if we can move up
                    # print("Range up: " + str(rh.getCarRangeUp(car, current.state)))
                    if rh.getCarRangeUp(car, current.state) > 0:
                        for dist in range(1, rh.getCarRangeUp(car, current.state) + 1):
                            newState = rh.moveCarUp(car, current.state, dist)
                            children.append(SearchNode(newState,
                                                       current.cost + dist,
                                                       str(car) + "\tup\t" + str(dist),
                                                       current,
                                                       heur(newState)))
                    # Check if we can move down
                    # print("Range down: " + str(rh.getCarRangeRight(car, current.state)))
                    if rh.getCarRangeDown(car, current.state) > 0:
                        for dist in range(1, rh.getCarRangeDown(car, current.state) + 1):
                            newState = rh.moveCarDown(car, current.state, dist)
                            children.append(SearchNode(newState,
                                                       current.cost + dist,
                                                       str(car) + "\tdown\t" + str(dist),
                                                       current,
                                                       heur(newState)))

                # Add current to closed list
                closedList.append(current)

                # Check if children are in closed
                uniqueChildren = copy.deepcopy(children)
                for child in children:
                    # print("Checking child: " + child.state + " vs closedList\n")
                    for node in closedList:
                        # print("COmparing " + child.state + " and " + node.state)
                        if rh.areStatesSame(child.state, node.state):
                            # print("states are the same")
                            for elem in uniqueChildren:
                                if rh.areStatesSame(elem.state, child.state):
                                    # print("Removing child")
                                    uniqueChildren.remove(elem)
                            break

                children = copy.deepcopy(uniqueChildren)

                # Check if children are in open
                uniqueChildren = copy.deepcopy(children)
                for child in children:
                    # print("Checking child: " + child.state + " vs openList")
                    for node in openList:
                        # print("COmparing "+ child.state + " and "+ node.state)
                        if rh.areStatesSame(child.state, node.state):
                            # print("States are the same")
                            for elem in uniqueChildren:
                                if rh.areStatesSame(elem.state, child.state):
                                    # print("Removing child")
                                    uniqueChildren.remove(elem)
                            break

                children = copy.deepcopy(uniqueChildren)

                # Insert in queue according to f = cost + heur
                for child in children:
                    inserted = False
                    if len(openList) == 0:
                        openList.append(child)
                    else:
                        for i in range(0, len(openList)):
                            if child.heur+child.cost <= openList[i].heur + openList[i].cost:
                                openList.insert(i, child)
                                inserted = True
                                break

                        if not inserted:
                            openList.append(child)

        if not solutionFound:

            # Only print sol file for demo problems
            if "demo" in name:
                # NO solution was found
                f = open(solFileName, "a")
                f.write("Runtime: " + str(time.time() - st) + "\n")
                f.write("Length of search path: " + str(counter) + "\n")
                f.write("No solution found")
                f.close()

            print("no solution")


def returnSolutionPath(solutionNode):
    solutionPath = [solutionNode]
    current = solutionNode
    while current.prev != "none":
        current = current.prev
        if current.prev == "none":
            break
        solutionPath.insert(0, current)
    return solutionPath

def solutionAsString(solutionPath):
    solutionString = ""
    for node in solutionPath:
        solutionString = solutionString+node.move+", "
    return solutionString

