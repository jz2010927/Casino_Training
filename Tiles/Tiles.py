'''
Pai Gow Tiles
4 tiles generator

!/usr/bin/python
 -*- coding: utf-8 -*-
'''

from win32api import GetSystemMetrics
from tkinter import *
import random
import copy
import TilesSetups
import TilesToolbox

class Tiles:
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.shoe = TilesSetups.newShoe()
        self.exceptionList = TilesSetups.sortedExceptionList()
        self.exceptionHousewayList = TilesSetups.exceptionHouseWayList()
        self.tilesValue = TilesSetups.initialTilesValue()
        self.singleTileRanking = TilesSetups.initialTilesSingleRankings()
        self.pairRanking = TilesSetups.initialTilesPairRankings()
        self.pairNames = TilesSetups.pairNames()
        self.regularHandsExceptions = []
        self._updateGeo()
        # Deal button
        dealButton = Button(self.root, text='Deal', command=self.deal)
        dealButton.pack(side=LEFT)
        # Exception button
        exceptionButton = Button(self.root, text='Exception Practice', command=self.dealException)
        exceptionButton.pack(side=LEFT)
        # House Way button
        houseWayButton = Button(self.root, text='House Way', command=self.displayHouseway)
        houseWayButton.pack(side=LEFT)

        self.currentHand = []
        self.currentHouseway = []
        self.welcomeScreen()

    def welcomeScreen(self):
        self._updateGeo()
        canvas.create_text(
            self.center[0],
            self.center[1] - 300,
            fill="darkblue",
            font="Times 20 italic bold",
            text='\tCasino M8trix\n\t            &\n\tBlackstone Gaming\n\nTiles Houseway Training Program'
        )
        canvas.create_text(
            self.center[0] + 300,
            self.center[1] + 100,
            fill="black",
            font="Times 20 italic bold",
            text='- Made by Peter'
        )

    def getValue(self, hand):
        print('Debug getValue: ')
        print(hand)
        value = []
        for tile in hand:
            value.append(self.tilesValue[tile])
        print('Debug getValue, Value: ', value)
        return value

    def getTilesCombineValue(self, hand):
        print('Debug getTilesCombineValue: ')
        print(hand)
        if hand in self.pairRanking:
            return self.pairRanking.index(hand) + 13

        if ('Joker_3' in hand) or ('Joker_6' in hand):
            if 'Joker' in hand[0]:
                return TilesToolbox.jokerMaxPoint([3, 6], self.tilesValue[hand[1]])
            else:
                return TilesToolbox.jokerMaxPoint([3, 6], self.tilesValue[hand[0]])

        handValues = sorted(self.getValue(hand))
        if handValues in ([2, 7], [2, 8], [2, 9]):
            if handValues == [2, 7]:
                # H9
                return 10
            elif handValues == [2, 8]:
                # GANG
                return 11
            else:
                # WANG
                return 12
        else:
            return TilesToolbox.getMod(handValues[0]+handValues[1])

    def checkFrontBackPoints(self, hand, front, back):
        qualified = False
        points = self._getHandValues(hand)
        if min(points) >= front and max(points) >= back:
            qualified = True
        return qualified

    def combinations(self, hand):
        print('Debug combination: ')
        print(hand)
        possiblities = []
        for i in range(3):
            possiblities.append([])
            possiblities[i].append(hand[0])
        index = 0
        for tile in hand[1:]:
            copyHand = copy.deepcopy(hand)
            copyHand.remove(hand[0])
            possiblities[index].append(tile)
            copyHand.remove(tile)
            possiblities[index].extend(copyHand)
            frontPoint = self.getTilesCombineValue(possiblities[index][:2])
            backPoint = self.getTilesCombineValue(possiblities[index][2:])
            if frontPoint > backPoint:
                possiblities[index].reverse()
            index += 1

        return possiblities
    
    def eliminateWeaks(self, combines):
        weakHands = []
        combinesCopy = copy.deepcopy(combines)
        for i in range(len(combinesCopy)):
            combinesCopy[i] = self.checkKickerRules(combinesCopy[i])

        for hand0 in combinesCopy[:1]:
            for hand1 in combinesCopy[1:]:
                handValues0 = self._getHandValues(hand0)
                handValues1 = self._getHandValues(hand1)
                kicker0_front = self._kickerInHand(hand0[:1])
                kicker0_back = self._kickerInHand(hand0[1:])
                kicker1_front = self._kickerInHand(hand1[:1])
                kicker1_back = self._kickerInHand(hand1[1:])
                rank0_front = list(kicker0_front.values())[0]
                rank0_back = list(kicker0_back.values())[0]
                rank1_front = list(kicker1_front.values())[0]
                rank1_back = list(kicker0_back.values())[0]
                if (handValues1[0] > handValues0[0]) and (handValues1[1] > handValues0[1]):
                    if hand0 not in weakHands:
                        weakHands.append(hand0)
                if (handValues1[0] < handValues0[0]) and (handValues1[1] < handValues0[1]):
                    if hand1 not in weakHands:
                        weakHands.append(hand1)
                if (handValues1[0] > handValues0[0]) and (handValues1[1] == handValues0[1]):
                    if rank1_front < rank0_front:
                        if hand0 not in weakHands:
                            weakHands.append(hand0)
                if (handValues1[0] < handValues0[0]) and (handValues1[1] == handValues0[1]):
                    if rank1_front > rank0_front:
                        if hand1 not in weakHands:
                            weakHands.append(hand1)
                if (handValues1[0] == handValues0[0]) and (handValues1[1] > handValues0[1]):
                    if rank1_back < rank0_back:
                        if hand0 not in weakHands:
                            weakHands.append(hand0)
                if (handValues1[0] == handValues0[0]) and (handValues1[1] < handValues0[1]):
                    if rank1_back > rank0_back:
                        if hand1 not in weakHands:
                            weakHands.append(hand1)
                if (handValues1[0] == handValues0[0]) and (handValues1[1] == handValues0[1]):
                    if (rank1_front < rank0_front) and (rank1_back < rank0_back):
                        if hand0 not in weakHands:
                            weakHands.append(hand0)
                    if (rank1_front > rank0_front) and (rank1_back > rank0_back):
                        if hand1 not in weakHands:
                            weakHands.append(hand1)
        print('Combines Copy: ')
        print(combinesCopy)
        print('Weak Hands List: ')
        print(weakHands)
        if weakHands:
            for hand in weakHands:
                print('Remove weak hand from combinesCopy: ')
                print(hand)
                combinesCopy.remove(hand)
        
        return combinesCopy

    def _balanceOrSook(self, possiblities):
        points = []
        balance = False
        sook = True
        result = []
        for hand in possiblities:
            points.append(
                self._getHandValues(hand)
            )
        # Find the max front point combination and max back point combination
        maxFrontPoints = points[0]
        maxBackPoints = points[0]
        maxFrontCombination = possiblities[0]
        maxBackCombination = possiblities[0]
        for i in range(len(points)):
            hand = possiblities[i]
            p = points[i]
            print('Index: ', i)
            print('Debug hand, p - hand: ', hand)
            print('Debug hand, p - p: ', p)
            if min(p) >= min(maxFrontPoints):
                if min(p) == min(maxFrontPoints):
                    kicker1 = self._kickerInHand(maxFrontCombination[:2])
                    kicker2 = self._kickerInHand(hand[:2])
                    rank1 = list(kicker1.values())[0]
                    rank2 = list(kicker2.values())[0]
                    print('Kicker1.values()', type(kicker1.values()), ' : ', kicker1.values())
                    print('Kicker2.values()', type(kicker2.values()), ' : ', kicker2.values())
                    if rank2 < rank1:
                        maxFrontPoints = p
                        maxFrontCombination = hand
                else:
                    maxFrontPoints = p
                    maxFrontCombination = hand
            if max(p) > max(maxBackPoints):
                maxBackPoints = p
                maxBackCombination = hand

        if self._checkPointsAndKicker(maxFrontCombination[:2]):
            balance = True
            sook = False
        if maxFrontPoints[0] == maxFrontPoints[1]:
            balance = balance or self._checkPointsAndKicker(maxFrontCombination[2:])
            sook = not balance

        if sook:
            if maxBackPoints[1] < 7:
                balance = True
                sook = False
            else:
                qualifiedCombinations = []
                for i in range(len(points)):
                    h = possiblities[i]
                    p = points[i]
                    if p[0] == 3 and p[1] >= 9:
                        qualifiedCombinations.append(h)
                    if p[0] < 3 and p[1] >= 7:
                        qualifiedCombinations.append(h)
                # if len(qualifiedCombinations) != 0
                if qualifiedCombinations:
                    qualifiedMaxBack = qualifiedCombinations[0]
                    for c in qualifiedCombinations:
                        backPoint1 = self.getTilesCombineValue(qualifiedMaxBack[2:])
                        backPoint2 = self.getTilesCombineValue(c[2:])
                        if backPoint2 >= backPoint1:
                            if backPoint2 == backPoint1:
                                kicker1 = self._kickerInHand(qualifiedMaxBack[2:])
                                kicker2 = self._kickerInHand(c[2:])
                                rank1 = list(kicker1.values())[0]
                                rank2 = list(kicker2.values())[0]
                                if rank2 < rank1:
                                    qualifiedMaxBack = c
                            else:
                                qualifiedMaxBack = c
                    result = qualifiedMaxBack
                else:
                    balance = True
                    sook = False

        if balance:
            minGap = max(points[0]) - min(points[0])
            maxTotal = min(points[0]) + max(points[0])
            result = possiblities[0]
            for i in range(len(points)):
                hand = possiblities[i]
                p = points[i]
                gap = max(p) - min(p)
                total = min(p) + max(p)
                if gap <= minGap:
                    if gap < minGap:
                        minGap = gap
                        result = hand
                    else:
                        if total > maxTotal:
                            maxTotal = total
                            result = hand
                        elif total == maxTotal:
                            kicker1 = self._kickerInHand(result[:2])
                            kicker2 = self._kickerInHand(hand[:2])
                            rank1 = list(kicker1.values())[0]
                            rank2 = list(kicker2.values())[0]
                            if rank2 < rank1:
                                result = hand
                        else:
                            pass
        result = self.checkKickerRules(result)
        return result
    
    def checkKickerRules(self, hand):
        if ('H12' not in hand[:2]) and ('L10' not in hand[:2]):
            return hand
        h = copy.deepcopy(hand)
        front = h[:2]
        back = h[2:]
        shouldBefront = ''
        shouldBeBack = ''
        for tile in [['H12', 'H2'], ['L10', 'H10']]:
            shouldBeBack = tile[0]
            shouldBefront = tile[1]
            if (shouldBeBack in front) and (shouldBefront in back):
                iFront, iBack = h.index(shouldBeBack), h.index(shouldBefront)
                h[iFront], h[iBack] = h[iBack], h[iFront]
        return h

    def _kickerInHand(self, hand):
        kicker = hand[0]
        kickerRank = self.singleTileRanking[kicker]
        for tile in hand:
            if self.singleTileRanking[tile] < kickerRank:
                kicker = tile
                kickerRank = self.singleTileRanking[kicker]
        return {kicker: kickerRank}

    def _checkPointsAndKicker(self, combination, p=3, kickerRank=6):
        rank1 = self.singleTileRanking[combination[0]]
        rank2 = self.singleTileRanking[combination[1]]
        point = self.getTilesCombineValue(combination)
        if point > p:
            return True
        elif point == p:
            if rank1 <= kickerRank:
                return True
            if rank2 <= kickerRank:
                return True
        else:
            return False

    def _getHandValues(self, hand):
        return [
            self.getTilesCombineValue([hand[0], hand[1]]), 
            self.getTilesCombineValue([hand[2], hand[3]])
        ]
        
    def _generateHand(self, number=4):
        return random.sample(self.shoe, number)

    def _houseway(self, hand):
        print('Debug _houseway: ')
        print(hand)
        houseway = []
        isException = False
        # if it's an exception, then use exception houseway
        for index in range(len(self.exceptionList)):
            if sorted(hand) == self.exceptionList[index]:
                houseway = self.exceptionHousewayList[index]
                isException = True
        self.regularHandsExceptions.append(isException)
        # if it's not exception, go by steps
        if not isException:
            # step 1: pair
            setHand = []
            pairNum = 0
            for pair in self.pairRanking:
                if TilesToolbox.checkSubSet(hand, pair):
                    setHand.append(pair)
                    pairNum += 1
            # if it's pair pair
            if pairNum == 2:
                pairRank_1 = self.pairRanking.index(sorted(setHand[0]))
                pairRank_2 = self.pairRanking.index(sorted(setHand[1]))
                if pairRank_1 > pairRank_2:
                    houseway.extend(setHand[1])
                    houseway.extend(setHand[0])
                else:
                    houseway.extend(setHand[0])
                    houseway.extend(setHand[1])
            elif pairNum == 1:
                notPair = sorted(list(set(hand)-set(setHand[0])))
                notPairValue = ([
                    self.tilesValue[notPair[0]], 
                    self.tilesValue[notPair[1]]
                ])
                if self.tilesValue[setHand[0][0]] in (4, 5, 6, 0, 1):
                    houseway.extend(notPair)
                    houseway.extend(setHand[0])
                else:
                    if setHand[0] == ['Joker_3', 'Joker_6']:
                        if sorted(notPairValue) in ([4, 6], [5, 6]):
                            houseway.append('Joker_3')
                            if notPairValue[0] < notPairValue[1]:
                                houseway.append(notPair[0])
                                houseway.append('Joker_6')
                                houseway.append(notPair[1])
                            else:
                                houseway.append(notPair[1])
                                houseway.append('Joker_6')
                                houseway.append(notPair[0])
                        elif sorted(notPairValue) == [6, 6]:
                            houseway.append('Joker_3')
                            if self.singleTileRanking[notPair[0]] >= self.singleTileRanking[notPair[1]]:
                                houseway.append(notPair[0])
                                houseway.append('Joker_6')
                                houseway.append(notPair[1])
                            else:
                                houseway.append(notPair[1])
                                houseway.append('Joker_6')
                                houseway.append(notPair[0])
                        else:
                            houseway.extend(notPair)
                            houseway.extend(setHand[0])
                    elif (setHand[0] == ['H12', 'H12']) or (setHand[0] == ['H2', 'H2']):
                        if sorted(notPair) in(sorted(['H11', 'M9_1']), sorted(['H11', 'M9_2'])):
                            houseway.extend(setHand[0])
                            if notPairValue[0] == 1:
                                houseway.insert(1, notPair[0])
                                houseway.insert(3, notPair[1])
                            else:
                                houseway.insert(1, notPair[1])
                                houseway.insert(3, notPair[0])
                        else:
                            testCombines = []
                            testCombines.extend(setHand[0])
                            testCombines.extend(notPair)
                            allCombinations = self.combinations(testCombines)
                            qulifiedHands = []
                            for h in allCombinations:
                                if self.checkFrontBackPoints(h, 6, 8):
                                    qulifiedHands.append(h)
                            if len(qulifiedHands) > 0:
                                houseway = self._balanceOrSook(qulifiedHands)
                            else:
                                houseway.extend(notPair)
                                houseway.extend(setHand[0])
                    elif setHand[0] in (
                        ['H7', 'H7'], ['H8', 'H8'], 
                        ['M7_1', 'M7_2'], ['M8_1', 'M8_2']
                    ):
                        testCombines = []
                        testCombines.extend(setHand[0])
                        testCombines.extend(notPair)
                        allCombinations = self.combinations(testCombines)
                        qulifiedHands = []
                        for h in allCombinations:
                            if self.checkFrontBackPoints(h, 7, 7):
                                qulifiedHands.append(h)
                        if len(qulifiedHands) > 0:
                            houseway = self._balanceOrSook(qulifiedHands)
                        else:
                            houseway.extend(notPair)
                            houseway.extend(setHand[0])
                    elif setHand[0] == ['M9_1', 'M9_2']:
                        testCombines = []
                        testCombines.extend(setHand[0])
                        testCombines.extend(notPair)
                        allCombinations = self.combinations(testCombines)
                        qulifiedHands = []
                        for h in allCombinations:
                            if self.checkFrontBackPoints(h, 9, 9):
                                qulifiedHands.append(h)
                        if len(qulifiedHands) > 0:
                            houseway = self._balanceOrSook(qulifiedHands)
                        else:
                            houseway.extend(notPair)
                            houseway.extend(setHand[0])
                    else:
                        houseway.extend(notPair)
                        houseway.extend(setHand[0])
            elif pairNum == 0:
                print('Debug _houseway before pass to combination: ')
                print('about pass: ', hand)
                allCombinations = self.eliminateWeaks(self.combinations(hand))
                # Check H9, Gang or Wang
                qualifiedhandValues = []
                qualifiedhands = []
                for c in allCombinations:
                    value = self._getHandValues(c)
                    if max(value) > 9:
                        qualifiedhandValues.append(value)
                        qualifiedhands.append(c)
                if len(qualifiedhandValues) > 0:
                    maxFront = qualifiedhandValues[0]
                    houseway = qualifiedhands[0]
                    for i in range(len(qualifiedhandValues)):
                        h = qualifiedhands[i]
                        v = qualifiedhandValues[i]
                        if min(v) >= min(maxFront):
                            if min(v) == min(maxFront):
                                kicker1 = self._kickerInHand(houseway[:2])
                                kicker2 = self._kickerInHand(h[:2])
                                rank1 = list(kicker1.values())[0]
                                rank2 = list(kicker2.values())[0]
                                if rank2 < rank1:
                                    maxFront = v
                                    houseway = h
                            else:
                                maxFront = v
                                houseway = h
                else:
                    # No pair, no H9, Gang or Wang
                    print('No pair, no H9, Gang or Wang')
                    houseway = self._balanceOrSook(allCombinations)
            else:
                print('Error')
                print('Pair number == ', pairNum)
        return houseway
                
    def _updateGeo(self):
        self.root.update()
        self.width = self.root.winfo_width()
        self.height = self.root.winfo_height()
        self.center = [self.width/2, self.height/2]

    def displayText(self, x, y, text, fill="darkblue", font="Times 20 italic bold"):
        self.canvas.create_text(
            x,
            y,
            fill=fill,
            font=font,
            text=text
        )

    def valueToName(self, hand):
        name = []
        for value in hand:
            if value < 10:
                name.append(str(value))
            else:
                name.append(self.pairNames[value-10])
        return name

    def _display(self, hands, startX, name):
        if name == 'Houseways':
            housewayDisplayed = False
            print('Houseway: ')
            print(self.currentHouseway)
        else:
            print('Hand: ')
            print(self.currentHand)
        self._updateGeo()
        # Tell which is dealer's hand
        self.displayText(self.center[0]*1.1, self.center[1]*1.6,'Dealer Hand')
        # Display tiles
        for i in range(len(hands)):
            index = 0
            hand = hands[i]
            for tile in hand:
                if name == 'Houseways' and index > 1:
                    path = r'TilesPics/' + tile + '_rotated.PNG'
                    x = self.center[0] + startX - 255
                    if index == 2:
                        y = self.center[1]*i*2 - 250*i + 15
                    else:
                        y = self.center[1]*i*2 - 250*i + 85
                else:
                    path = r'TilesPics/' + tile + '.PNG'
                    x = self.center[0] - 400 + (index*70) + startX
                    y = self.center[1]*i*2 - 250*i 
                pic = PhotoImage(file=path).subsample(2, 2)
                if name != 'Houseways' or not housewayDisplayed:
                    # Tell what is the hand
                    self.canvas.create_text(
                        self.center[0] - 250 + startX,
                        self.center[1],
                        fill="darkblue",
                        font="Times 20 italic bold",
                        text=name
                    )
                    # Display Images
                    self.canvas.create_image(
                        x, y,
                        image = pic,
                        anchor = NW,
                        tags = path
                    )
                    self.canvas.images.append(pic)
                index += 1

    def displayExceptionMark(self):
        for i in range(len(self.regularHandsExceptions)):
            if self.regularHandsExceptions[i]:
                text = 'Exception'
                x = self.center[0] + 800
                y = self.center[1]*i*2 + 50 - 200*i
                self.displayText(x, y, text)

    def displayResult(self):
        handValue = []
        kickerRankings = []
        for hand in self.currentHouseway:
            handValue.append(self._getHandValues(hand))
            kickerRankings.append(
                [
                    self.singleTileRanking[hand[0]], 
                    self.singleTileRanking[hand[1]], 
                    self.singleTileRanking[hand[2]], 
                    self.singleTileRanking[hand[3]]
                ]
            )
        topValue = handValue[0]
        bottomValue = handValue[1]
        topKickerRanking = kickerRankings[0]
        bottomKickerRanking = kickerRankings[1]
        topPoint = 0
        bottomPoint = 0
        # Compare front(low)
        if topValue[0] > bottomValue[0]:
            topPoint += 1
        if topValue[0] < bottomValue[0]:
            bottomPoint += 1
        if topValue[0] == bottomValue[0]:
            if topValue[0] == 0:
                # Point 0 no kicker, when copy, banker wins
                bottomPoint += 1
            else:
                if min(topKickerRanking[:1]) < min(bottomKickerRanking[:1]):
                    topPoint += 1
                if min(topKickerRanking[:1]) > min(bottomKickerRanking[:1]):
                    bottomPoint += 1
                if min(topKickerRanking[:1]) == min(bottomKickerRanking[:1]):
                    if max(topKickerRanking[:1]) < max(bottomKickerRanking[:1]):
                        topPoint += 1
                    if max(topKickerRanking[:1]) > max(bottomKickerRanking[:1]):
                        bottomPoint += 1
                    # When copy, dealer hand wins
                    if max(topKickerRanking[:1]) == max(bottomKickerRanking[:1]):
                        bottomPoint += 1
            
        # Compare back(high)
        if topValue[1] > bottomValue[1]:
            topPoint += 1
        if topValue[1] < bottomValue[1]:
            bottomPoint += 1
        if topValue[1] == bottomValue[1]:
            if topValue[1] == 0:
                # Point 0 no kicker, when copy, banker wins
                bottomPoint += 1
            else:
                if min(topKickerRanking[1:]) < min(bottomKickerRanking[1:]):
                    topPoint += 1
                if min(topKickerRanking[1:]) > min(bottomKickerRanking[1:]):
                    bottomPoint += 1
                if min(topKickerRanking[1:]) == min(bottomKickerRanking[1:]):
                    if max(topKickerRanking[1:]) < max(bottomKickerRanking[1:]):
                        topPoint += 1
                    if max(topKickerRanking[1:]) > max(bottomKickerRanking[1:]):
                        bottomPoint += 1
                    # When copy, dealer hand wins
                    if max(topKickerRanking[1:]) == max(bottomKickerRanking[1:]):
                        bottomPoint += 1

        x = self.center[0] * 1.1
        y = self.center[1]
        if topPoint > bottomPoint:
            self.displayText(x, y*0.2, 'Winner --->')
            print('Top winner displayed')
        if topPoint < bottomPoint:
            self.displayText(x, y*1.7, 'Winner --->')
            print('Bottom winner displayed')
        if topPoint == bottomPoint:
            self.displayText(x, y, 'PUSH')
            print('Push displayed')

        valueStr = []
        for values in handValue:
            valueStr.append(
                self.valueToName(values)
            )
        index  = -1
        for v in valueStr:
            x = self.center[0] + 450
            y = self.center[1] + (2*index*90)
            if index == 1:
                y -= 75
            text = 'Low: ' + v[0] + '\t  High: ' + v[1]
            self.displayText(x, y, text)
            index += 2

    def displayHouseway(self):
        self.currentHouseway = []
        for hand in self.currentHand:
            self.currentHouseway.append(self._houseway(hand))
        self._display(self.currentHouseway, 700, "Houseways")
        self.displayResult()
        self.displayExceptionMark()
    
    def deal(self):
        self.currentHand = []
        self.regularHandsExceptions = []
        self.currentHand.append(self._generateHand())
        self.currentHand.append(self._generateHand())
        self.canvas.delete('all')
        self.canvas.images = []
        self._display(self.currentHand, 0, "Regular hands")
    
    def dealException(self):
        self.currentHand = random.sample(self.exceptionList, 2)
        self.regularHandsExceptions = []
        self.canvas.delete('all')
        self.canvas.images = []
        self._display(self.currentHand, 0, "Exception hands")

if __name__=='__main__':
    screenResolution = str(GetSystemMetrics(0)) + 'x' + str(GetSystemMetrics(1))
    root = Tk()
    root.geometry(screenResolution)
    root.title("Pai gow tiles")
    # Create canvas object
    canvas = Canvas(root, bg='white')
    canvas.pack(side=BOTTOM, fill=BOTH, expand=YES)
    t = Tiles(root, canvas)
    hand = t._generateHand()
    # print('Hand: ')
    # print(hand)
    # print('Combinations: ')
    # print(t.combinations(hand))
    # print('Points: ')
    # for c in t.combinations(hand):
    #     print(t._getHandValues(c))
    root.mainloop()
