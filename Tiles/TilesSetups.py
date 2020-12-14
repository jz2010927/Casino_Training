'''
Tiles Exception List
'''
def newShoe(decks=1):
    tiles = [
            'Joker_3', 'Joker_6', 'H12', 'H12', 'H2', 'H2',
            'H8', 'H8', 'H4', 'H4', 'H10', 'H10',
            'H6', 'H6', 'L4', 'L4', 'H11', 'H11',
            'L10', 'L10', 'H7', 'H7', 'L6', 'L6',
            'M9_1', 'M9_2', 'M8_1', 'M8_2', 'M7_1', 'M7_2',
            'M5_1', 'M5_2'
        ]

    if decks > 1:
        deck = []
        for i in range(decks):
            deck.extend(tiles)
        return deck
    else:
        return tiles

def initialTilesValue():
    tilesValues = {
        'Joker_3': [3, 6], 'Joker_6': [3, 6],
        'H12': 2, 'H2': 2, 'H8': 8, 'H4': 4,
        'H10': 0, 'H6': 6, 'L4': 4, 'H11': 1,
        'L10': 0, 'H7': 7, 'L6': 6, 
        'M9_1': 9, 'M9_2': 9, 
        'M8_1': 8, 'M8_2': 8, 
        'M7_1': 7, 'M7_2': 7, 
        'M5_1': 5, 'M5_2': 5
    }
    return tilesValues

def initialTilesSingleRankings():
    tilesValues = initialTilesValue()
    singleTileRankings = {}
    index = 1
    for key in tilesValues.keys():
        # Joker ranks 15th
        if 'Joker' in key:
            singleTileRankings[key] = 15
        # Mixed 9 ranks 12th
        elif 'M9' in key:
            singleTileRankings[key] = 12
        # Mixed 8 ranks 13th
        elif 'M8' in key:
            singleTileRankings[key] = 13
        # Mixed 7 ranks 14th
        elif 'M7' in key:
            singleTileRankings[key] = 14
        # Mixed 5 ranks 16th
        elif 'M5' in key:
            singleTileRankings[key] = 16
        # Other tile ranks same as pair ranking
        else:
            singleTileRankings[key] = index
            index += 1
    return singleTileRankings

def initialTilesPairRankings():
    pairRanking = [
        ['Joker_3', 'Joker_6'], ['H12', 'H12'], ['H2', 'H2'],
        ['H8', 'H8'], ['H4', 'H4'], ['H10', 'H10'],
        ['H6', 'H6'], ['L4', 'L4'], ['H11', 'H11'],
        ['L10', 'L10'], ['H7', 'H7'], ['L6', 'L6'],
        ['M9_1', 'M9_2'], ['M8_1', 'M8_2'], ['M7_1', 'M7_2'],
        ['M5_1', 'M5_2']
    ]
    pairRanking.reverse()
    for pair in pairRanking:
        pair.sort()
    return pairRanking

def pairNames():
    Name = [
        'Gee Jeong', 'Double Teen', 'Double Day', 
        'Double High 8', 'Double High 4', 'Double High 10', 
        'Double High 6', 'Double Low 4', 'Double 11',
        'Double Low 10', 'Double High 7', 'Double Low 6', 
        'Mixed 9s', 'Mixed 8s', 'Mixed 7s', 'Mixed 5s', 
        'Wong', 'Gong', 'H9'
    ]
    Name.reverse()
    return Name

def sortedExceptionList():
    # All exceptions
    exceptionList = [
        # 1
        ['H12', 'H2', 'H11', 'H10'],
        ['H12', 'H2', 'H11', 'L10'],
        # 2
        ['H12', 'H2', 'H4', 'M5_1'],
        ['H12', 'H2', 'H4', 'M5_2'],
        ['H12', 'H2', 'L4', 'M5_1'],
        ['H12', 'H2', 'H4', 'M5_2'],
        # 3
        ['H10', 'L10', 'M8_1', 'M9_1'],
        ['H10', 'L10', 'M8_1', 'M9_2'],
        ['H10', 'L10', 'M8_2', 'M9_1'],
        ['H10', 'L10', 'M8_2', 'M9_2'],
        # 4
        ['H10', 'L10', 'H11', 'M9_1'],
        ['H10', 'L10', 'H11', 'M9_2'],
        # 5
        ['H8', 'H11', 'H10', 'M8_1'],
        ['H8', 'H11', 'H10', 'M8_2'],
        ['H8', 'H11', 'L10', 'M8_1'],
        ['H8', 'H11', 'L10', 'M8_2'],
        # 6
        ['H8', 'H10', 'H11', 'H7'],
        ['H8', 'H10', 'H11', 'M7_1'],
        ['H8', 'H10', 'H11', 'M7_2'],
        # 7
        ['H4', 'L4', 'M5_1', 'Joker_3'],
        ['H4', 'L4', 'M5_2', 'Joker_3'],
        ['H4', 'L4', 'M5_1', 'Joker_6'],
        ['H4', 'L4', 'M5_2', 'Joker_6'],
        # 8
        ['H8', 'M8_1', 'H7', 'M9_1'],
        ['H8', 'M8_1', 'H7', 'M9_2'],
        ['H8', 'M8_1', 'M7_1', 'M9_1'],
        ['H8', 'M8_1', 'M7_1', 'M9_2'],
        ['H8', 'M8_1', 'M7_2', 'M9_1'],
        ['H8', 'M8_1', 'M7_2', 'M9_2'],
        ['H8', 'M8_2', 'H7', 'M9_1'],
        ['H8', 'M8_2', 'H7', 'M9_2'],
        ['H8', 'M8_2', 'M7_1', 'M9_1'],
        ['H8', 'M8_2', 'M7_1', 'M9_2'],
        ['H8', 'M8_2', 'M7_2', 'M9_1'],
        ['H8', 'M8_2', 'M7_2', 'M9_2'],
        # 9
        ['H6', 'L6', 'H11', 'Joker_3'],
        ['H6', 'L6', 'H11', 'Joker_6'],
        # 10
        ['H12', 'H4', 'H8', 'M9_1'],
        ['H12', 'H4', 'H8', 'M9_2'],
        ['H12', 'H4', 'M8_1', 'M9_1'],
        ['H12', 'H4', 'M8_1', 'M9_2'],
        ['H12', 'H4', 'M8_2', 'M9_1'],
        ['H12', 'H4', 'M8_2', 'M9_2'],
        ['H12', 'L4', 'H8', 'M9_1'],
        ['H12', 'L4', 'H8', 'M9_2'],
        ['H12', 'L4', 'M8_1', 'M9_1'],
        ['H12', 'L4', 'M8_1', 'M9_2'],
        ['H12', 'L4', 'M8_2', 'M9_1'],
        ['H12', 'L4', 'M8_2', 'M9_2'],
        ['H2', 'H4', 'H8', 'M9_1'],
        ['H2', 'H4', 'H8', 'M9_2'],
        ['H2', 'H4', 'M8_1', 'M9_1'],
        ['H2', 'H4', 'M8_1', 'M9_2'],
        ['H2', 'H4', 'M8_2', 'M9_1'],
        ['H2', 'H4', 'M8_2', 'M9_2'],
        ['H2', 'L4', 'H8', 'M9_1'],
        ['H2', 'L4', 'H8', 'M9_2'],
        ['H2', 'L4', 'M8_1', 'M9_1'],
        ['H2', 'L4', 'M8_1', 'M9_2'],
        ['H2', 'L4', 'M8_2', 'M9_1'],
        ['H2', 'L4', 'M8_2', 'M9_2'],
        # 11
        ['H12', 'M5_1', 'Joker_3', 'H6'],
        ['H12', 'M5_1', 'Joker_3', 'L6'],
        ['H12', 'M5_1', 'Joker_6', 'H6'],
        ['H12', 'M5_1', 'Joker_6', 'L6'],
        ['H12', 'M5_2', 'Joker_3', 'H6'],
        ['H12', 'M5_2', 'Joker_3', 'L6'],
        ['H12', 'M5_2', 'Joker_6', 'H6'],
        ['H12', 'M5_2', 'Joker_6', 'L6'],
        ['H2', 'M5_1', 'Joker_3', 'H6'],
        ['H2', 'M5_1', 'Joker_3', 'L6'],
        ['H2', 'M5_1', 'Joker_6', 'H6'],
        ['H2', 'M5_1', 'Joker_6', 'L6'],
        ['H2', 'M5_2', 'Joker_3', 'H6'],
        ['H2', 'M5_2', 'Joker_3', 'L6'],
        ['H2', 'M5_2', 'Joker_6', 'H6'],
        ['H2', 'M5_2', 'Joker_6', 'L6'],
        # 12
        ['H4', 'L4', 'M9_1', 'M5_1'],
        ['H4', 'L4', 'M9_1', 'M5_2'],
        ['H4', 'L4', 'M9_2', 'M5_1'],
        ['H4', 'L4', 'M9_2', 'M5_2']
    ]
    for hand in exceptionList:
        hand.sort()
    return exceptionList

def exceptionHouseWayList():
    exceptionHouseWay = [
        ['H12', 'H10', 'H2', 'H11'], 
        ['H12', 'L10', 'H2', 'H11'], 
        ['H12', 'H4', 'H2', 'M5_1'], 
        ['H12', 'H4', 'H2', 'M5_2'], 
        ['H12', 'L4', 'H2', 'M5_1'], 
        ['H12', 'H4', 'H2', 'M5_2'], 
        ['L10', 'M8_1', 'H10', 'M9_1'], 
        ['L10', 'M8_1', 'H10', 'M9_2'], 
        ['L10', 'M8_2', 'H10', 'M9_1'], 
        ['L10', 'M8_2', 'H10', 'M9_2'], 
        ['L10', 'H11', 'H10', 'M9_1'], 
        ['L10', 'H11', 'H10', 'M9_2'], 
        ['H10', 'M8_1', 'H11', 'H8'], 
        ['H10', 'M8_2', 'H11', 'H8'], 
        ['L10', 'M8_1', 'H11', 'H8'], 
        ['L10', 'M8_2', 'H11', 'H8'], 
        ['H10', 'H7', 'H11', 'H8'], 
        ['H10', 'M7_1', 'H11', 'H8'], 
        ['H10', 'M7_2', 'H11', 'H8'], 
        ['H4', 'Joker_3', 'L4', 'M5_1'], 
        ['H4', 'Joker_3', 'L4', 'M5_2'], 
        ['H4', 'Joker_6', 'L4', 'M5_1'], 
        ['H4', 'Joker_6', 'L4', 'M5_2'], 
        ['H7', 'H8', 'M8_1', 'M9_1'], 
        ['H7', 'H8', 'M8_1', 'M9_2'], 
        ['M7_1', 'H8', 'M8_1', 'M9_1'], 
        ['M7_1', 'H8', 'M8_1', 'M9_2'], 
        ['M7_2', 'H8', 'M8_1', 'M9_1'], 
        ['M7_2', 'H8', 'M8_1', 'M9_2'], 
        ['H7', 'H8', 'M8_2', 'M9_1'], 
        ['H7', 'H8', 'M8_2', 'M9_2'], 
        ['M7_1', 'H8', 'M8_2', 'M9_1'], 
        ['M7_1', 'H8', 'M8_2', 'M9_2'], 
        ['M7_2', 'H8', 'M8_2', 'M9_1'], 
        ['M7_2', 'H8', 'M8_2', 'M9_2'], 
        ['L6', 'H11', 'H6', 'Joker_3'], 
        ['L6', 'H11', 'H6', 'Joker_6'], 
        ['H4', 'M9_1', 'H12', 'H8'], 
        ['H4', 'M9_2', 'H12', 'H8'], 
        ['H4', 'M9_1', 'H12', 'M8_1'], 
        ['H4', 'M9_2', 'H12', 'M8_1'], 
        ['H4', 'M9_1', 'H12', 'M8_2'], 
        ['H4', 'M9_2', 'H12', 'M8_2'], 
        ['L4', 'M9_1', 'H12', 'H8'], 
        ['L4', 'M9_2', 'H12', 'H8'], 
        ['L4', 'M9_1', 'H12', 'M8_1'], 
        ['L4', 'M9_2', 'H12', 'M8_1'], 
        ['L4', 'M9_1', 'H12', 'M8_2'], 
        ['L4', 'M9_2', 'H12', 'M8_2'], 
        ['H4', 'M9_1', 'H2', 'H8'], 
        ['H4', 'M9_2', 'H2', 'H8'], 
        ['H4', 'M9_1', 'H2', 'M8_1'], 
        ['H4', 'M9_2', 'H2', 'M8_1'], 
        ['H4', 'M9_1', 'H2', 'M8_2'], 
        ['H4', 'M9_2', 'H2', 'M8_2'], 
        ['L4', 'M9_1', 'H2', 'H8'], 
        ['L4', 'M9_2', 'H2', 'H8'], 
        ['L4', 'M9_1', 'H2', 'M8_1'], 
        ['L4', 'M9_2', 'H2', 'M8_1'], 
        ['L4', 'M9_1', 'H2', 'M8_2'], 
        ['L4', 'M9_2', 'H2', 'M8_2'], 
        ['H12', 'M5_1', 'H6', 'Joker_3'], 
        ['H12', 'M5_1', 'L6', 'Joker_3'], 
        ['H12', 'M5_1', 'H6', 'Joker_6'], 
        ['H12', 'M5_1', 'L6', 'Joker_6'], 
        ['H12', 'M5_2', 'H6', 'Joker_3'], 
        ['H12', 'M5_2', 'L6', 'Joker_3'], 
        ['H12', 'M5_2', 'H6', 'Joker_6'], 
        ['H12', 'M5_2', 'L6', 'Joker_6'], 
        ['H2', 'M5_1', 'H6', 'Joker_3'], 
        ['H2', 'M5_1', 'L6', 'Joker_3'], 
        ['H2', 'M5_1', 'H6', 'Joker_6'], 
        ['H2', 'M5_1', 'L6', 'Joker_6'], 
        ['H2', 'M5_2', 'H6', 'Joker_3'], 
        ['H2', 'M5_2', 'L6', 'Joker_3'], 
        ['H2', 'M5_2', 'H6', 'Joker_6'], 
        ['H2', 'M5_2', 'L6', 'Joker_6'], 
        ['H4', 'M9_1', 'L4', 'M5_1'], 
        ['H4', 'M9_1', 'L4', 'M5_2'], 
        ['H4', 'M9_2', 'L4', 'M5_1'], 
        ['H4', 'M9_2', 'L4', 'M5_2']
    ]
    return exceptionHouseWay

if __name__=='__main__':
    exceptionList = sortedExceptionList()
    exceptionHWList = exceptionHouseWayList()
    error = 0
    correctHWList = []

    if len(exceptionList) != len(exceptionHWList):
        print('Different length')
    else:
        print('Same length\n')
        for o,h in zip(exceptionList, exceptionHWList):
            if o == sorted(h):
                correctHWList.append(h)
            else:
                error += 1
                print('Different item!')
                print(o, '\n\n', h, '\n\n')
                for searchH in exceptionHWList:
                    if sorted(searchH) == o:
                        correctHWList.append(searchH)

    print('List length = ', len(exceptionList))
    print('Error = ', error)
    print('Correct Houseway List: \n')
    print(correctHWList)