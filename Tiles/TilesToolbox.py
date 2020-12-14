'''
Toolbox for tiles.py
'''

def getMod(number):
    return number % 10

def jokerMaxPoint(jokerValueList, nonJokerValue):
    allPoints = []
    for value in jokerValueList:
        allPoints.append(getMod(value+nonJokerValue))
    return max(allPoints)

def checkSubSet(list1, subList):
    for item in subList:
        if subList.count(item) > list1.count(item):
            return False
    return True