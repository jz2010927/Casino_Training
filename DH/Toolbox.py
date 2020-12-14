'''
Pai Gow Poker
Double hand training
Tool box

!/usr/bin/python
 -*- coding: utf-8 -*-
'''
import itertools
from copy import deepcopy

class Toolbox:

    def __init__(self):
        pass
        
    def itemIndexesInList(self, l1, item):
        indexes = []
        for i in range(len(l1)):
            if l1[i] == item:
                indexes.append(l1[i])
        return indexes
    
    # 去重复
    def deduplication(self, l):
        deduplicated = []
        for i in l:
            if i not in deduplicated:
                deduplicated.append(i)
        return deduplicated

    # 深度去重复
    def inDepthDeduplication(self, l):
        deduplicated = []
        for i in range(len(l)):
            if l[i] not in deduplicated:
                if type(l[i]) is list:
                    item = self.inDepthDeduplication(l[i])
                else:
                    item = l[i]
                deduplicated.append(item)
        return deduplicated
    
    # 扁平化列表
    def flatList(self, nestedList):
        nestedList = deepcopy(nestedList)
        while nestedList:
            sublist = nestedList.pop(0)

            if isinstance(sublist, list):
                nestedList = sublist + nestedList
            else:
                yield sublist

if __name__=='__main__':
    t = Toolbox()
    a = [1,463,3,2,57,43,213,8,1,1,4,78,3,3,3,2,2,7,7,'gds']
    a1 = t.deduplication(a)
    print('a1: ', a1)
    b = [[1,1,1,2,2],2,3,2,2,3,4,[4,4,2,[3,2,[3,4,5,3,2,[22,3,6,3,5]],2],3,2,2],46,23,[22,33,22,33]]
    b1 = t.inDepthDeduplication(b)
    b2 = t.deduplication(b)
    print('b1: ', b1)
    print('b2: ', b2)
    b3 = t.flatList(b)
    print('b3: ', list(b3))
