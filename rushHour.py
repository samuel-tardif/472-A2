

def isSolution(state):
    if state[17] == 'A':
        return True
    else:
        return False


def valet(state):
    if state[2] != '.':
        toReplace = state[2]
        state = state.replace(toReplace, '.')
    return state


def areStatesSame(state1, state2):
    if state1[0:35] == state2[0:35]:
        return True
    else:
        return False


def moveCarRight(car, state, dist):
    carPos = state.index(car)
    carLength = getCarLength(car, state)
    for i in range(0, dist):
        state[carPos+i] = '.'
        state[carPos+carLength+i]=car
    state = updateCarFuel(car, state ,dist)
    return state


def moveCarLeft(car, state, dist):
    carPos = state.index(car)
    carLength = getCarLength(car, state)
    for i in range(0, dist):
        state[carPos+carLength - i] = '.'
        state[carPos-i] = car
    state = updateCarFuel(car, state ,dist)
    return state


def moveCarDown(car, state, dist):
    carPos = state.index(car)
    carLength = getCarLength(car, state)
    for i in range(0, dist):
        state[carPos+i*6] = '.'
        state[carPos+carLength*6+i*6] = car
    state = updateCarFuel(car, state ,dist)
    return state


def moveCarUp(car, state, dist):
    carPos = state.index(car)
    carLength = getCarLength(car, state)
    for i in range(0, dist):
        state[carPos+carLength*6-i*6] = '.'
        state[carPos-i*6] = car
    state = updateCarFuel(car, state ,dist)
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
        for i in range(carPos, carPos+5):
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
                if state[i] == '.' & getFuelForCar(car, state)>carRange:
                    carRange += 1
                else:
                    return carRange
            return carRange

def getCarRangeDown(car, state):
    if not isCarVertical(car, state):
        return 0
    else:
        carPos = state.index(car)
        if carPos >= 30:
            return 0
        else:
            carRange = 0
            for i in range(carPos+getCarLength(car, state)*6,0,6):
                if state[i] == '.'& getFuelForCar(car, state)>carRange:
                    carRange += 1
                else:
                    return carRange
            return carRange

def getCarRangeRight(car, state):
    if isCarVertical(car, state):
        return 0
    else:
        carPos = state.index(car)
        if (carPos) % 6 >= 4:
            return 0
        else:
            carRange = 0
            for i in range(carPos+getCarLength(car, state), carPos+(6-carPos%6-getCarLength(car, state))):
                if state[i] == '.'& getFuelForCar(car, state)>carRange:
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
                if state[i] == '.'& getFuelForCar(car, state)>carRange:
                    carRange += 1
                else:
                    return carRange
            return carRange

def listOfCars(state):
    listOfCars = set(state)
    listOfCars.replace('.', '')
    return listOfCars

def getFuelForCar(car, state):
    if len(state)==36:
        return 100
    fuelInfo = state[36:]
    if car in fuelInfo:
        ind = fuelInfo.index("car")
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
    if car in fuelInfo:
        ind = fuelInfo.index("car")
        fuel = int(fuelInfo[ind + 1])
        state[36+ind+1] = str(fuel-dist)
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
