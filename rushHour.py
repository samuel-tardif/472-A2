import random

def isSolution(state):
    if 'A' not in state:
        return True
    else:
        return False


def valet(state):
    if state[17] != '.':
        toReplace = state[17]
        state = state.replace(toReplace, '.')
    return state


def areStatesSame(state1, state2):
    if state1[0:36] == state2[0:36]:
        return True
    else:
        return False


def moveCarRight(car, state, dist):
    carPos = state.index(car)
    carLength = getCarLength(car, state)
    for i in range(0, dist):
        state = replacer(state, '.', carPos+i)
        state = replacer(state, car, carPos+carLength+i)
    state = updateCarFuel(car, state, dist)
    state = valet(state)
    return state


def moveCarLeft(car, state, dist):
    carPos = state.index(car)
    carLength = getCarLength(car, state)
    for i in range(0, dist):
        state = replacer(state, '.', carPos + carLength-1 - i)
        state = replacer(state, car, carPos-(1+i))
    state = updateCarFuel(car, state, dist)
    state = valet(state)
    return state


def moveCarDown(car, state, dist):
    carPos = state.index(car)
    carLength = getCarLength(car, state)
    for i in range(0, dist):
        state = replacer(state,'.', carPos+i*6)
        state = replacer(state, car, carPos+carLength*6+i*6)
    state = updateCarFuel(car, state, dist)
    state = valet(state)
    return state


def moveCarUp(car, state, dist):
    carPos = state.index(car)
    #print("car pos : " + str(carPos))
    carLength = getCarLength(car, state)
    for i in range(0, dist):
        #print("adding blank at index :"+ str(carPos+(carLength-1)*6-i*6))
        state = replacer(state, '.', carPos+(carLength-1)*6-i*6)
        #print("adding car at ind :"+str(carPos-(i+1)*6))
        state = replacer(state, car, carPos-(i+1)*6)
    state = updateCarFuel(car, state, dist)
    state = valet(state)
    return state


def isCarVertical(car, state):
    carPos = state.index(car)
    if carPos >= 30:
        return False
    elif state[carPos+6]==car:
        return True
    else:
        return False


def getCarLength(car, state):
    carPos = state.index(car)
    length = 0
    if isCarVertical(car,state):
        for i in range(carPos,35,6):
            if state[i] == car:
                length+=1
    else:
        for i in range(carPos, carPos+5-carPos%6):
            if state[i] == car:
                length+=1
    return length


def getCarRangeUp(car, state):
    if not isCarVertical(car, state):
        return 0
    else:
        carPos = state.index(car)
        if carPos <= 5:
            return 0
        else:
            carRange = 0
            for i in range(carPos-6,0,-6):
                if ((state[i] == '.') & (getFuelForCar(car, state)>carRange)):
                    carRange += 1
                else:
                    return carRange
            return carRange

def getCarRangeDown(car, state):
    if not isCarVertical(car, state):
        #print("car not vertical")
        return 0
    else:
        carPos = state.index(car)
        #print("car pos: "+str(carPos))
        if carPos >= 30:
            return 0
        else:
            carRange = 0
            #print("car length: "+str(getCarLength(car, state)))
            for i in range(carPos+getCarLength(car, state)*6, 36, 6):
                #print("i: "+str(i))
                #print(str(getFuelForCar(car, state)))
                if (state[i] == '.') & (getFuelForCar(car, state)>carRange):
                    #print("Increment range")
                    carRange += 1
                else:
                    return carRange
            return carRange

def getCarRangeRight(car, state):
    if isCarVertical(car, state):
        #print("car vertical")
        return 0
    else:
        carPos = state.index(car)
        length = getCarLength(car, state)
        if (length == 2) & ((carPos) % 6 >= 4):
            #print("car already max right")
            return 0
        elif (length == 3) & ((carPos) % 6 >= 3):
            #print("car already max right")
            return 0
        else:
            carRange = 0
            #print("lower bound"+ str(carPos+length)+ " upper bound: "+str(carPos+(6-carPos%6)))
            for i in range(carPos+length, carPos+(6-carPos%6)):
                #print("i: "+str(i))
                #print(state[i])
                if (state[i] == '.') & (getFuelForCar(car, state) > carRange):
                    #print("Increment range")
                    carRange += 1
                else:
                    return carRange
            return carRange

def getCarRangeLeft(car, state):
    if isCarVertical(car, state):
        return 0
    else:
        carPos = state.index(car)
        if (carPos) % 6 == 0:
            return 0
        else:
            carRange = 0
            for i in range(carPos+getCarLength(car, state), carPos-carPos%6, -1):
                if (str(state[i]) == ".") & (getFuelForCar(car, state)>carRange):
                    carRange += 1
                else:
                    return carRange
            return carRange

def listOfCars(state):
    setOfCars = set(state[0:36])
    listOfCars = (list(setOfCars))
    listOfCars.remove('.')
    return listOfCars

def getFuelForCar(car, state):
    if len(state)==36:
        return 100
    fuelInfo = state[36:]
    if car in fuelInfo:
        ind = fuelInfo.index(car)
        return int(fuelInfo[ind+1])
    else:
        return 100

def checkIfProblemValid(state):
    carPos = state.index('A')
    if getFuelForCar('A') < (4-carPos%6):
        return False
    else:
        return True


def updateCarFuel(car, state, dist):
    if len(state) == 36:
        return state
    fuelInfo = state[36:]
    #print("length: "+str(len(state)))
    #print("fuel info : "+fuelInfo)
    if car in fuelInfo:
        ind = fuelInfo.index(car)
        fuel = int(fuelInfo[ind + 1])
        state = replacer(state, str(fuel-dist), 36+ind+1)
    return state


def printState(state):
    print("\t|\t1\t2\t3\t4\t5\t6\n")
    print("___________________________________________________________")
    print("1\t|\t"+state[0]+"\t"+state[1]+"\t"+state[2]+"\t"+state[3]+"\t"+state[4]+"\t"+state[5]+"\n")
    print("1\t|\t" + state[6] + "\t" + state[7] + "\t" + state[8] + "\t" + state[9] + "\t" + state[10] + "\t" + state[
        11] + "\n")
    print("1\t|\t" + state[12] + "\t" + state[12] + "\t" + state[14] + "\t" + state[15] + "\t" + state[16] + "\t" + state[
        17] + "\n")
    print("1\t|\t" + state[18] + "\t" + state[19] + "\t" + state[20] + "\t" + state[21] + "\t" + state[22] + "\t" + state[
        23] + "\n")
    print("1\t|\t" + state[24] + "\t" + state[25] + "\t" + state[26] + "\t" + state[27] + "\t" + state[28] + "\t" + state[
        29] + "\n")
    print("1\t|\t" + state[30] + "\t" + state[31] + "\t" + state[32] + "\t" + state[33] + "\t" + state[34] + "\t" + state[
        35] + "\n")


def generateRandomProblem():
    state = ["."]*36
    #add spacing for fuel
    state.append("  ")
    #Place ambulance
    starting_spot = random.choice([0,1,2])
    state[12+starting_spot]='A'
    state[13+starting_spot]='A'

    #Decide what cars will be placed
    possible_cars = ['B','C','D','E','F','G','H','I','J','K']
    for car in possible_cars:
        if coinFlip():
            #Place cars to be placed
            count = 0
            isCarPlaced = False
            while not isCarPlaced & count < 10:

                count+=1

                isCarVertical = coinFlip()
                size = random.choice([2,3])

                #Choose spot
                row = random.randint(0,5)
                column = random.randint(0,5)

                #Check if fits
                is_placeable = True
                if state[row*6+column] == '.':
                    if isCarVertical:
                        if (row+size)*6+column < 36:
                            for i in range(1,size-1):
                                if state[(row+i)*6+column] != '.':
                                    is_placeable = False
                        else:
                            is_placeable = False
                    else:
                        if column%6+size > 6 :
                            for i in range(1,size-1):
                                if state[(row)*6+column+i] != '.':
                                    is_placeable = False
                        else:
                            is_placeable = False
                else:
                    is_placeable = False

                #If it can be placed, do so
                    #Places
                    for i in range(0,size):
                        if isCarVertical:
                            state[(row+i)*6+column]=car
                        else:
                            state[row * 6 + column + i] = car
                    #Gas info
                    if coinFlip():
                        state.append(car)
                        state.append(str(random.randint(0, 5)))

#GENERAL UTIL FUNCTIONS
def coinFlip():
    result = random.choice([True, False])
    return result

def replacer(s, newstring, index):
    if index < 0:  # add it to the beginning
        return newstring + s
    if index > len(s):  # add it to the end
        return s + newstring

    if index == len(s)-1:  # add it to the end
        return s[:index] + newstring
    # insert the new string between "slices" of the original
    return s[:index] + newstring + s[index + 1:]
