# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 16:41:42 2019

@author: Marie
"""

# Ce fichier contient (au moins) cinq erreurs.
# Instructions:
#  - tester jusqu'à atteindre 100% de couverture;
#  - corriger les bugs;
#  - envoyer le diff ou le dépôt git par email.

from hypothesis import given, strategies as st

class BinHeap:
    def __init__(self):
        self.heapList = [0]
        self.currentSize = 0#1->0

    def percUp(self,i):
        while i // 2 > 0:
          if self.heapList[i] < self.heapList[i // 2]:
             tmp = self.heapList[i // 2]
             self.heapList[i // 2] = self.heapList[i]
             self.heapList[i] = tmp
          i = i // 2 #incrementation -1 cran

    def insert(self,k):
      self.heapList.append(k)
      self.currentSize = self.currentSize + 1
      self.percUp(self.currentSize)

    def percDown(self,i):
      while (i * 2) <= self.currentSize: #< -> <=
          mc = self.minChild(i)
          if self.heapList[i] > self.heapList[mc]:
              tmp = self.heapList[i]
              self.heapList[i] = self.heapList[mc]
              self.heapList[mc] = tmp
              i = mc #incrementation +1 cran
          else:
              return 0

    def minChild(self,i):
      if i * 2 + 1 > self.currentSize:
          return i * 2
      else:
          if self.heapList[i*2] < self.heapList[i*2+1]:
              return i * 2
          else:
              return i * 2 + 1

    def delMin(self):
      retval = self.heapList[1]
      self.heapList[1] = self.heapList[self.currentSize]
      self.currentSize = self.currentSize - 1
      self.heapList.pop()
      self.percDown(1)
      return retval #rval->retval

    def buildHeap(self,alist):
      i = len(alist) // 2
      self.currentSize = len(alist)
      self.heapList = [0] + alist[:]
      while (i > 0):
          self.percDown(i)  #percUp -> percDown
          i = i - 1

    

@given(st.lists(st.integers()))      
def test_insert_delMin(l):
    x=BinHeap()
    l1=sorted(l)
    for i in l:
        x.insert(i)
    l2=[]
    for i in l:
        l2.append(x.delMin())
    assert l1==l2
    
@given(st.lists(st.integers()))
def test_buildHeap_delMin(l):
    x=BinHeap()
    x.buildHeap(l)
    l1=sorted(l)
    l2=[]
    for i in l:
        l2.append(x.delMin())
    assert l1==l2
    
    
    