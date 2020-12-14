'''
Pai Gow Poker
Double hand training

!/usr/bin/python
 -*- coding: utf-8 -*-
'''

from win32api import GetSystemMetrics
from itertools import combinations
from itertools import groupby
from tkinter import *
import random
import copy
import re
import Toolbox

class DH:
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.sevenCards = {}
        self.initClickedCards()
        self.currentHand = []
        self.setHand = []
        self._updateGeo()
        self.shoe = self.newShoe()
        self.cardValues = self.initialCardValue()
        self.cardSuits = self.initialCardSuit()
        self.correctPoint = 0
        self.wrongPoint = 0
        self.toolbox = Toolbox.Toolbox()
        # Deal button
        dealButton = Button(self.root, text='Deal', command=self.displayCards)
        dealButton.pack(side=LEFT)
        # Check Set Hand
        checkButton = Button(self.root, text='Check Set Hand', command=self.checkSet)
        checkButton.pack(side=LEFT)
        # Houseway button
        housewayButton = Button(self.root, text='Houseway', command=self._houseway)
        housewayButton.pack(side=LEFT)
        # Bind the left click to onClickMove
        self.canvas.bind("<Button-1>", self.onClickMove)
        self.welcomeScreen()

    def welcomeScreen(self):
        self._updateGeo()
        self.canvas.create_text(
            self.center[0],
            self.center[1] * 0.5,
            fill="darkblue",
            font="Times 20 italic bold",
            text='\tCasino M8trix\n\t            &\n\tBlackstone Gaming\n\nDouble hand Houseway Training Program'
        )
        self.canvas.create_text(
            self.center[0] * 1.2,
            self.center[1],
            fill="black",
            font="Times 20 italic bold",
            text='- Made by Peter'
        )

    def initClickedCards(self):
        # Initial all 7 cards as behind cards
        self.clickedCards = []
        for i in range(7):
            self.clickedCards.append(False)

    def _updateGeo(self):
        self.root.update()
        self.width = self.root.winfo_width()
        self.height = self.root.winfo_height()
        self.center = [self.width/2, self.height/2]

    def newShoe(self, decks=1, joker=True):
        suits = ['Club', 'Diamond', 'Heart', 'Spade']
        values = []
        for v in range(2, 11):
            values.append(str(v))
        values.append('J')
        values.append('Q')
        values.append('K')
        values.append('A')
        deck = []
        if joker:
            deck.append('Joker')
        for suit in suits:
            for value in values:
                deck.append(
                    suit + '_' + value
                )
        if decks > 1:
            cardDecks = []
            for d in range(decks):
                cardDecks.extend(deck)
            return cardDecks
        else:
            return deck

    def initialCardValue(self):
        values = {}
        for card in self.shoe:
            num = re.findall(r'\d+',card)
            if not num:
                if card == 'Joker':
                    values[card] = 15
                else:
                    if 'J' in card:
                        values[card] = 11
                    if 'Q' in card:
                        values[card] = 12
                    if 'K' in card:
                        values[card] = 13
                    if 'A' in card:
                        values[card] = 14
            else:
                values[card] = int(num[0])
        #print('Card Values: \n', values)
        return values

    def initialCardSuit(self):
        cardSuits = {}
        suits = ['Heart', 'Diamond', 'Club', 'Spade']
        cardSuits['Joker'] = 'All'
        for card in self.shoe:
            for suit in suits:
                if suit in card:
                    cardSuits[card] = suit
        #print('Card suits: \n', cardSuits)
        return cardSuits

    def switchToValues(self, hand):
        values = []
        for card in hand:
            values.append(
                self.cardValues[card]
            )
        return values
    
    def switchToSuits(self, hand):
        suits = []
        for card in hand:
            suits.append(
                self.cardSuits[card]
            )
        return suits

    def pickRanCards(self, number=7):
        return random.sample(self.shoe, number)

    def displayImage(self, image_path, location, cut=2):
        pic = PhotoImage(file=image_path).subsample(cut, cut)
        image = self.canvas.create_image(
            location[0], location[1],
            image = pic,
            anchor = NW,
            tags = image_path
        )
        '''
        canvas.create_text(
            location[0], location[1],
            fill="darkblue",
            font="Times 20 italic bold",
            text=str(location[0]) + ', ' + str(location[1])
        )
        '''
        self.canvas.images.append(pic)
        return image

    def displayText(self, text, location, tag):
        t = self.canvas.create_text(
            location[0], location[1], 
            fill="darkblue",
            font="Times 20 italic bold",
            text=text, 
            tags=tag
        )
        return t

    def displayPoints(self):
        self.canvas.delete('Correct Points')
        self.canvas.delete('Wrong Points')
        correct = 'correct.PNG'
        wrong = 'wrong.PNG'
        pathCorrect = 'imgs/' + correct
        pathWrong = 'imgs/' + wrong
        x = self.center[0]
        y = self.center[1]
        self.displayImage(pathCorrect, [x*0.2, y*0.2], 3)
        self.displayText(str(self.correctPoint), [x*0.4, y*0.3], 'Correct Points')
        self.displayImage(pathWrong, [x*1.6, y*0.2], 3)
        self.displayText(str(self.wrongPoint), [x*1.8, y*0.3], 'Wrong Points')

    def displayCards(self):
        self._updateGeo()
        # Set all cards back to behind
        for i in range(len(self.clickedCards)):
            self.clickedCards[i] = False

        self.canvas.delete('all')
        self.canvas.images = []
        # Display points
        self.displayPoints()
        self.currentHand = self.pickRanCards()
        #print(self.currentHand)
        index = 0
        startX = self.center[1] * 0.1
        startY = self.center[1] * 0.7
        gap = self.center[0] * 0.24
        for card in self.currentHand:
            path = 'imgs/' + card + '.PNG'
            x = startX + (index*gap)
            self.sevenCards[index] = self.displayImage(path, [x, startY])
            index += 1

    def onClickMove(self, event):
        Xs = []
        startX = self.center[1] * 0.1
        gap = self.center[0] * 0.24
        for i in range(8):
            Xs.append(startX+(i*gap))
        Xs[-1] += self.center[1] * 0.15

        if event.y >= (self.center[1] * 0.5) and event.y <= (self.center[1] * 1.7):
            for index in range(len(Xs)-1):
                if event.x >= Xs[index] and event.x <= Xs[index+1]:
                    if self.clickedCards[index]:
                        self.canvas.move(self.sevenCards[index], 0, 100)
                        self.clickedCards[index] = False
                    else:
                        self.canvas.move(self.sevenCards[index], 0, -100)
                        self.clickedCards[index] = True
    
    def _allCombinations(self, hand):
        allFronts = list(combinations(hand, 2))
        allBacks = []
        for i in range(len(allFronts)):
            allFronts[i] = list(allFronts[i])
            allBacks.append(
                list(set(hand)-set(allFronts[i]))
            )
        return {'Fronts': allFronts, 'Backs': allBacks}
        
    def checkStraight(self, hand, playNum):
        # 如果手中牌张数小于需求，直接返回空
        if playNum > len(hand):
            return []
        else:
            # 检查是否有Joker在里面
            hasJoker = False
            if "Joker" in hand:
                hasJoker = True
            # 将牌面转换成数值序列
            values = self.switchToValues(hand)
            # 首先对数值列表进行排序
            sortedValues = sorted(values)
            # 如果只是检查是不是顺子
            if playNum == len(hand):
                a0 = sortedValues[0]
                straight = [a0]
                jumped = False
                for sv in sortedValues[1:]:
                    if sv == (a0+1) and sv != 15:
                        straight.append(sv)
                        a0 = sv
                    else:
                        if hasJoker and (sv == (a0+2)) and not jumped:
                            straight.append(15)
                            straight.append(sv)
                            a0 = sv
                            jumped = True
                if (sortedValues[0]==2) and (14 in sortedValues):
                    straight.insert(0, 14)
                if len(straight) == playNum:
                    # 排序用于检查重复
                    return sorted(hand)
                else:
                    return []
            else:
                straights = []
                cs = combinations(hand, playNum)
                for c in cs:
                    isStraight = self.checkStraight(list(c), playNum)
                    if isStraight:
                        straights.append(isStraight)
                # 消除重复的手
                straights = self.toolbox.deduplication(straights)
                return straights

    def checkFlush(self, hand, playNum):
        len_hand = len(hand)
        # 如果手中牌张数小于需求，直接返回空
        if playNum > len_hand:
            return []
        else:
            # 将牌列表转换成花色列表，顺序不变
            handSuits = self.switchToSuits(hand)
            # 如果只是看着一手是不是同花，而不是看包不包含同花
            if playNum == len_hand:
                suited = True
                if handSuits[0] != 'All':
                    first_CardSuit = handSuits[0]
                else:
                    first_CardSuit = handSuits[1]
                for hs in handSuits:
                    if hs != first_CardSuit and hs != 'All':
                        suited = False
                if suited:
                    # 排序用于检查重复
                    return sorted(hand)
                else:
                    return []
            else:
                cs = combinations(hand, playNum)
                flushes = []
                for c in cs:
                    isFlush = self.checkFlush(list(c), playNum)
                    if isFlush:
                        flushes.append(isFlush)
                # 消除重复的手
                flushes = self.toolbox.deduplication(flushes)
                return flushes

    def checkAnyofAKind(self, hand, playNum):
        # 如果手中牌张数小于需求，直接返回空
        if playNum > len(hand):
            print('长度太长')
            return []
        qualified = []
        len_hand = len(hand)
        hasJoker = False
        # 检查王牌是否存在，如果存在找到地址
        if 'Joker' in hand:
            hasJoker = True
        # 将牌面转换成数值列表
        handValues = self.switchToValues(hand)
        # 交叉对比，相同的纳入合格列表
        appended = []
        for i in range(len_hand)[:len_hand-1]:
            temp = []
            v_i = handValues[i]
            if v_i not in appended:
                if v_i != 15:
                    temp = [hand[i]]
                    appended.append(v_i)
                for j in range(len_hand)[i+1:]:
                    v_j = handValues[j]
                    if v_j == v_i:
                        temp.append(hand[j])
                if hasJoker:
                    temp.append('Joker')
            #print('temp: ', temp)
            if len(temp) >= playNum:
                #print('temp appended')
                qualified.append(temp)
        # 加工合格列表里的数据，然后放到另一个列表返回
        pairs = []
        if qualified:
            for q in qualified:
                combines = combinations(q, playNum)
                for c in combines:
                    #print('c: ', c)
                    pairs.append(list(c))
            # 去重复
            pairs = self.toolbox.deduplication(pairs)
        return pairs

    def classifiedAnyOfKinds(self, data):
        if data:
            if type(data[0]) is list:
                classification = []
                minValue = []
                for k in data:
                    k_value = self.switchToValues(k)
                    minimum = min(k_value)
                    if not classification:
                        classification.append([k])
                        minValue.append(minimum)
                    else:
                        if minimum in minValue:
                            index = minValue.index(minimum)
                            classification[index].append(k)
                        else:
                            classification.append([k])
                            minValue.append(minimum)
                return classification
            else:
                return [data]
        else:
            return []

    def checkFullHouse(self, hand):
        # 如果不足5张牌，返回空
        len_hand = len(hand)
        if len_hand < 5:
            return []
        threeOfKind = self.checkAnyofAKind(hand, 3)
        if threeOfKind:
            fullHouses = []
            for tok in threeOfKind:
                cardsLeft = list(set(hand) - set(tok))
                hasPair = self.checkAnyofAKind(cardsLeft, 2)
                if hasPair:
                    for p in hasPair:
                        fullHouses.append(
                            {'Front': p, 'Back': tok}
                        )
            return fullHouses
        else:
            return []

    def allSetHandCombines(self):
        # 是否包含小王
        hasJoker = False
        if 'Joker' in self.currentHand:
            hasJoker = True
        # 列出所有可能
        allCombines = self._allCombinations(self.currentHand)
        front = allCombines['Fronts']
        back = allCombines['Back']
        # 找出不合格
        fallHands = []
        if len(front) == len(back):
            for i in range(len(front)):
                # 上下的牌
                hair = front[i]
                fiveCards = back[i]
                # 上下牌的值
                hairValues = self.switchToValues(hair)
                backValues = self.switchToValues(fiveCards)
                # 检查上牌是否为对子
                hairPairCheck = self.checkAnyofAKind(hair, 2)
                # 检查下牌是否为顺子
                straightCheck = self.checkStraight(fiveCards, 5)
                # 检查下牌是否为同花
                flushCheck = self.checkFlush(fiveCards, 5)
                # 检查下牌是否包含小王
                jokerCheck = ('Joker' in fiveCards)
                # 检查下牌是否包含对子
                pairCheck = self.checkAnyofAKind(fiveCards, 2)
                # 如果头上是对子
                if hairPairCheck:
                    # 后面没有顺子、同花
                    if (not straightCheck) and (not flushCheck):
                        # 如果没有小王
                        if not jokerCheck:
                            # 如果也没有对子
                            if not pairCheck:
                                fallHands.append(i)
                        else:
                            # 后面有小王(肯定有对子)，深度复制序列，去除小王后，序列中没有对子，并且序列中最大值小于头上最小值
                            noJoker = copy.deepcopy(fiveCards)
                            noJoker.remove('Joker')
                            noJokerValues = self.switchToValues(noJoker)
                            noJokerPairCheck = self.checkAnyofAKind(noJoker, 2)
                            if (not noJokerPairCheck) and (max(noJokerValues) < min(hairValues)):
                                fallHands.append(i)
                # 如果头上不是对子
                else:
                    # 后面没有顺子、同花、对子，并且最大值小于头上最大值
                    if (not straightCheck) and (not flushCheck) and (not pairCheck) and (max(backValues) < max(hairValues)):
                        fallHands.append(i)
        else:
            print('Something wrong: Front length != Back length')
        # 将所有合格的手放入合格序列
        front_noFallHands = []
        back_noFallHands = []
        for i in range(len(front)):
            if i not in fallHands:
                front_noFallHands.append(front[i])
                back_noFallHands.append(back[i])
        # 去除赌博
        gambleHands = []
        nature4 = False
        has4OfKind = self.checkAnyofAKind(self.currentHand, 4)
        if not hasJoker and has4OfKind:
            nature4 = True
            nature4Value = self.switchToValues(has4OfKind[0])[0]
        for i in range(len(front_noFallHands)):
            # 上下的牌
            hair = front_noFallHands[i]
            fiveCards = back_noFallHands[i]
            # 上下牌的值
            hairValues = self.switchToValues(hair)
            backValues = self.switchToValues(fiveCards)
            # 检查上牌是否为对子
            hairPairCheck = self.checkAnyofAKind(hair, 2)
            # 检查下牌是否包含对子
            backPairCheck = self.checkAnyofAKind(fiveCards, 2)
            backPairNum = len(self.classifiedAnyOfKinds(backPairCheck))
            if not nature4:
                # 检查某些 Pair - Pair 应该是 Two Pair behind
                # 如果有小王，则永远Pair-Pair
                if not hasJoker:
                    if hairPairCheck and backPairNum == 1:
                        hairPairValue = min(self.switchToValues(hairPairCheck[0]))
                        backPairValue = min(self.switchToValues(backPairCheck[0]))
                        maxPairValue = max(hairPairValue, backPairValue)
                        maxBack = max(backValues)
                        # 如果最大单牌小于Q，或最大对子大于等于Q，则不存在Two Pair behind
                        if maxBack > 11 and maxPairValue < 12:
                            if maxBack == 12:
                                if maxPairValue < 6:
                                    gambleHands.append(i)
                            elif maxBack == 13:
                                if maxPairValue < 9:
                                    gambleHands.append(i)
                            elif maxBack == 14:
                                gambleHands.append(i)
                            else:
                                print('Max back value = ', maxBack)
                # 检查某些 Two Pair behind 应该是 Pair - Pair
                # 如果有小王，则永远Pair-Pair
                if hasJoker:
                    gambleHands.append(i)
                else:
                    if not hairPairCheck and backPairNum == 2:
                        maxHairValue = max(self.switchToValues(hair))
                        maxBackPairValue = max(
                            max(self.switchToValues(backPairCheck[0]), self.switchToValues(backPairCheck[1]))
                        )
                        if maxHairValue < 12 or maxBackPairValue > 11:
                            gambleHands.append(i)
                        else:
                            if maxHairValue == 12 and maxBackPairValue > 5:
                                gambleHands.append(i)
                            elif maxHairValue == 13 and maxBackPairValue > 8:
                                gambleHands.append(i)
                            else:
                                print('Hair hight card: ', maxHairValue, 'Highest pair: ', maxBackPairValue)
            else:
                # 四条情况
                # 如果是 Pair - Pair
                if 
        # 去掉赌博手
        front_laundried = []
        back_laundried = []
        for i in range(len(front_noFallHands)):
            if i not in gambleHands:
                front_laundried.append(front_noFallHands[i])
                back_laundried.append(back_noFallHands[i])
        # 返回合格序列
        return {'Front': front_laundried, 'Back': back_laundried}
    
    def sortSingleCards(self, hand):
        hand_copy = copy.deepcopy(hand)
        if 'Joker' in hand_copy:
            hand_copy.remove('Joker')
        pairs = self.checkAnyofAKind(hand_copy, 2)
        singleCards = []
        if pairs:
            pairCards = self.toolbox.flatList(pairs)
            singleCards = list(set(hand_copy) - set(pairCards))
        else:
            singleCards = hand_copy
        singleCards_values = self.switchToValues(singleCards)
        sortedValue = sorted(singleCards_values, reverse=True)
        sortedSingleCards = []
        for sv in sortedValue:
            i = singleCards_values.index(sv)
            sortedSingleCards.append(singleCards[i])
        return sortedSingleCards
        
    def _houseway(self, hand):
        self._updateGeo()
        x = self.center[0]
        y = self.center[1] * 0.5
        self.displayPoints()
        self.setHand = self.clickedCards
        for i in range(len(self.clickedCards)):
            if self.clickedCards[i]:
                self.canvas.move(self.sevenCards[i], 0, 100)
                self.clickedCards[i] = False
        # 排列出所有可能
        all_SetHands = self.allSetHandCombines()
        fronts = all_SetHands['Front']
        backs = all_SetHands['Back']
        # 检查 Pair-Complete hand
        pair_Complete = []
        for i in range(len(fronts)):
            front = fronts[i]
            back = backs[i]
        # 检查 FullHouse
        fullHouse = []
        if not pair_Complete:

        # 检查 三对
        threePair = []
        # 检查 Pair-Pair
        pair_Pair = []
        # 检查 非对子 - 完全手
        nonPair_Complete = []
        # 检查 非对子 - 三张
        nonPair_ThreeCard = []
        # 检查 非对子 - 一对
        nonPair_Pair = []
        # 检查 非对子 - 单牌
        nonPair_HighCard = []

    def checkBonus(self, hand):
        bonus = {
            '7CardStraightFlush': False, 
            '5Aces': False, 
            '5OfAKind': False, 
            'Royal': False, 
            'StraightFlush': False, 
            '4OfAKind': False, 
            'Nature4OfAKind': False, 
            'FullHouse': False, 
            'Flush': False, 
            'Straight': False, 
            '3OfAKind': False, 
            '3Pair': False, 
            '2Pair': False, 
            '1Pair': False
        }
        hasJoker = False
        if 'Joker' in hand:
            hasJoker = True
        len_hand = len(hand)
        # check 7 card straight flush
        is7Straight = self.checkStraight(hand, len_hand)
        is7Flush = self.checkStraight(hand, len_hand)
        if is7Straight and is7Flush:
            bonus['7CardStraightFlush'] = True
            bonus['StraightFlush'] = True
        # check 5 Aces and 5 of a kind
        is5ofKind = self.checkAnyofAKind(hand, 5)
        if is5ofKind:
            bonus['5OfAKind'] = True
            bonus['Nature4OfAKind'] = True
        fiveOfKind_Value = self.switchToValues(is5ofKind)
        if min(fiveOfKind_Value) == 14:
            bonus['5Aces'] = True
        # check Royal and Straight flush
        is5Flush = self.checkStraight(hand, 5)
        is5Straight = self.checkStraight(hand, 5)
        straightFlush = []
        if is5Flush:
            if is5Straight:
                for f5 in is5Flush:
                    for s5 in is5Straight:
                        if s5 == f5:
                            straightFlush.append(s5)
        if straightFlush:
            bonus['StraightFlush'] = True
            for sf in straightFlush:
                sf_value = self.switchToValues(sf)
                sf_value.sort()
                royal_NoJoker_Values = [10, 11, 12, 13, 14]
                if not hasJoker:
                    if sf_value == royal_NoJoker_Values:
                        bonus['Royal'] = True
                else:
                    partialRoyals = combinations(royal_NoJoker_Values, 4)
                    for pr in partialRoyals:
                        royal_Joker_Values = pr.append(15)
                        if royal_Joker_Values == sf_value:
                            bonus['Royal'] = True
        # 将小王去除
        hand_copy = copy.deepcopy(hand)
        if hasJoker:
            hand_copy.remove('Joker')
        is4ofKind = self.checkAnyofAKind(hand_copy, 4)
        is3ofKind = self.checkAnyofAKind(hand_copy, 3)
        pairsInHand = self.checkAnyofAKind(hand_copy, 2)
        # check 4 of a kind
        if is4ofKind:
            bonus['Nature4OfAKind'] = True
        else:
            if is3ofKind:
                bonus['4OfAKind'] = True
        # check full house
        isFullHouse = self.checkFullHouse(hand)
        if isFullHouse:
            bonus['FullHouse'] = True
        # check flush
        if is5Flush:
            bonus['Flush'] = True
        # check straight
        if is5Straight:
            bonus['Straight'] = True
        # check 3 of a kind
        if is3ofKind:
            bonus['3OfAKind'] = True
        else:
            if hasJoker:
                if pairsInHand:
                    bonus['3OfAKind'] = True
        # check 3 pairs
        pairNum = self.classifiedAnyOfKinds(pairsInHand)
        if len(pairNum) == 3:
            bonus['3Pair'] = True
        # check 2 pairs
        elif len(pairNum) == 2:
            bonus['2Pair'] = True
        # check 1 pair
        elif len(pairNum) == 1:
            bonus['1Pair'] == True
        else:
            print('Pair number in hand: ', len(pairNum))
        return bonus

    def completeHandLevel(self, hand):
        bonus = self.checkBonus(hand)
        if bonus['5OfAKind']:
            return 7
        if bonus['Royal']:
            return 6
        if bonus['StraightFlush']:
            return 5
        if bonus['4OfAKind']:
            return 4
        if bonus['FullHouse']:
            return 3
        if bonus['Flush']:
            return 2
        if bonus['Straight']:
            return 1
        return 0

    def compareHands(self, handsList):
        fronts = handsList['Front']
        backs = handsList['Back']
        for i in range(len(fronts)):
            hair = fronts[i]
            behind = backs[i]
            
    def checkSet(self, hand):
        hasJoker = False
        if 'Joker' in hand:
            hasJoker = True
        # 所有情况
        # 如果没有小王
        # 没对子： 什么都没有， 把第二、第三大的牌放上面
        # 仅有一对： 把第一、第二大的单牌放上面
        # 有两对： 
            # 如果最大的对子是 A 、K 、 Q, 则把小的对子放上面
            # 如果最大的对子是 J 、10 、9，则： 
                # 如果第一大单牌是 A，就把第一、第二大单牌放上面，两对放下面
                # 否则便把小的对子放上面
                # 如果第一大单牌是 A 或 K，就把第一、第二大单牌放上面，两对放下面
                # 否则便把小的对子放上面
            # 如果最大的对子是 5 、4 、3，则： 
                # 如果第一大单牌是 A 、K 或 Q，就把第一、第二大单牌放上面，两对放下面
                # 否则便把小的对子放上面
        # 三条： 
            # 三条 A，把其中一条 A,和最大单牌一起，放上面，留一对 A 在下面
            # 其他三条，将第一、第二大单牌放上面
        # 两个三条： 将最大的对子放上面
        # 三对： 同上
        # 顺子、同花或者同花顺，没有对子： 将尽可能最大的两张放上面，下面保持完全手
        # 顺子、同花或者同花顺或者一对： 同上
        # 顺子、同花或者同花顺或者两对： 用两对的规则
        # 三带二： 一对放上面，三条放下面
        # 四条（炸弹）： 
            # A 、K 、Q： 分成两对，放一对在上面
            # J 、10 、9： 
                # 如果第一大单牌是 A 或 K： 把第一、第二大单牌放上面
                # 否则分成两对，放一对在上面
            # 8 、7 、6： 
                # 如果第一大单牌是 A 、K 、Q： 把第一、第二大单牌放上面
                # 否则分成两对，放一对在上面
            # 5 以及以下： 
                # 永远把第一、第二大单牌放上面，四条放下面
        # 四条带一对： 一对放上面，四条放下面

        # 如果有小王
        # 没有对子，没有顺子，没有同花： 把第一、第三大单牌放上面，小王和第二大单牌组成对子
        # 没有对子，有顺子或同花： 用小王来组成顺子或同花，把最大的两张单牌放上面
        # 顺子、同花或者一对加小王： 把小的一对放上面
        # 一对加小王： 同上
        # 两对加小王： 
            # 如果最大单牌比最大对子的牌大至少三个等级（如果最大对子是7，则单牌至少是10）：则将小王和最大单牌作为一对放上面，两对放下面
            # 否则将最大对子放上面，将小的对子于小王组成三条放下面 - 即三带二
        # 三对加小王：最大对子放上面，三带二放下面
        # 三条加小王：最大单牌与小王组成对子放上面，三条放下面
        # 四条加一对加小王： 把最大对子放上面，四条或者三带二放下面
        # 三带二加小王： 同上

        # 三条加完全手，不管有没有小王，实行： 最大对子在上面，完全手在下面

                        
if __name__=='__main__':
    
    screenResolution = str(GetSystemMetrics(0)) + 'x' + str(GetSystemMetrics(1))
    root = Tk()
    root.geometry(screenResolution)
    root.title("Double hand")
    # Create canvas object
    canvas = Canvas(root, bg='white')
    canvas.pack(side=BOTTOM, fill=BOTH, expand=YES)
    t = DH(root, canvas)

    testHand_W_Joker = t.pickRanCards(7)
    if 'Joker' not in testHand_W_Joker:
        testHand_W_Joker.append('Joker')
        del testHand_W_Joker[0]
    testHand2 = t.pickRanCards(7)
    ss0 = ['Club_', 'Heart_', 'Diamond_', 'Spade_']
    straight1 = ['Club_A', 'Heart_5', 'Heart_2', 'Joker', 'Club_3']
    straight2 = ['Joker', 'Diamond_A', 'Club_K', 'Heart_10', 'Spade_Q']
    straight3 = ['Joker', 'Club_A', 'Heart_2', 'Diamond_3', 'Spade_4', 'Club_K', 'Heart_Q', 'Diamond_J', 'Spade_10']
    flush1 = ['Club_A', 'Club_2', 'Club_3', 'Club_4', 'Club_5']
    flush2 = ['Joker', 'Heart_A', 'Heart_K', 'Heart_2', 'Heart_3', ]
    flush3 = ['Diamond_A', 'Diamond_5', 'Diamond_6', 'Diamond_7', 'Joker', 'Diamond_J', 'Club_A', 'Club_2', 'Club_3', 'Club_4', ]
    straightFlush_7cards = ['Spade_7', 'Spade_9', 'Spade_J', 'Joker', 'Spade_8', 'Spade_K', 'Spade_10']
    fiveOfKind = ['Club_2', 'Heart_2', 'Diamond_2', 'Spade_2','Club_3', 'Heart_5', 'Joker']
    fourOfKind1 = ['Club_2', 'Heart_2', 'Diamond_2', 'Spade_4','Club_3', 'Heart_5', 'Joker']
    fourOfKind2 = ['Club_2', 'Heart_2', 'Diamond_2', 'Spade_2','Club_3', 'Heart_5', 'Heart_A']
    threeOfKind1 = ['Club_2', 'Heart_2', 'Diamond_2', 'Spade_3','Club_3', 'Heart_4', 'Joker']
    threeOfKind2 = ['Club_A', 'Heart_A', 'Diamond_A', 'Spade_2', 'Club_3', 'Heart_3', 'Diamond_3']
    pairs1 = ['Club_A', 'Heart_A', 'Diamond_2', 'Spade_2', 'Club_3', 'Heart_3', 'Joker']
    pairs2 = ['Club_A', 'Heart_4', 'Diamond_2', 'Spade_5', 'Club_3', 'Heart_A', 'Joker']
    pairs3 = ['Club_A', 'Club_2', 'Club_3', 'Club_4', 'Joker']
    print('Test Hand: ', testHand_W_Joker)
    allCombines = combinations(testHand_W_Joker, 2)
    print('!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-')
    print('All Combinations: ')
    for c in allCombines:
        print(sorted(list(set(testHand_W_Joker)-set(c))))
        print(sorted(list(c)), '\n')
    print('!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-')
    print('Pairs: ')
    checkPairs = t.checkAnyofAKind(testHand_W_Joker, 2)
    for p in checkPairs:
        print(p)

    clsfd_2 = t.classifiedAnyOfKinds(checkPairs)
    print('After classification: \t\t Length = ', len(clsfd_2))
    for c in clsfd_2:
        print(c)
    print('!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-')
    print('3 of a kind: ')
    check3ofKind = t.checkAnyofAKind(testHand_W_Joker, 3)
    for t3 in check3ofKind:
        print(t3)
    
    clsfd_3 = t.classifiedAnyOfKinds(check3ofKind)
    print('After classification: \t\t Length = ', len(clsfd_3))
    for c in clsfd_3:
        print(c)
    print('!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-')
    print('4 of a kind: ')
    check4ofKind = t.checkAnyofAKind(testHand_W_Joker, 4)
    for t4 in check4ofKind:
        print(t4)

    clsfd_4 = t.classifiedAnyOfKinds(check4ofKind)
    print('After classification: \t\t Length = ', len(clsfd_4))
    for c in clsfd_4:
        print(c)
    print('!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-')
    print('5 of a kind: ')
    check5ofKind = t.checkAnyofAKind(fiveOfKind, 5)
    for t5 in check5ofKind:
        print(t5)
    print('!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-')
    print('Straight: ')
    checkStraight = t.checkStraight(straightFlush_7cards, 7)
    for s in checkStraight:
        print(s)
    print('!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-')
    print('Flush: ')
    checkFlush = t.checkFlush(straightFlush_7cards, 7)
    for f in checkFlush:
        print(f)
    print('!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-')
    print('Sorted Single Cards: ')
    sortedSingleCards = t.sortSingleCards(testHand_W_Joker)
    print(sortedSingleCards)
    #root.mainloop()