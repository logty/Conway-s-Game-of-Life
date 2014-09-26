from numpy import random as numpyRandom
import numpy as np

def getSumNeighbourCells(array,x,y):
    if x<1 or x > len(array[0]) or y < 1 or y > len(array):
        print 'problemo!'
        return 0
    return sum([array[y+j][x+i] for j in range(-1,2) for i in range(-1,2) if not (i==0 and j==0)])

def getCell(array,x,y):
    neighbourSum = getSumNeighbourCells(array,x,y)
    if neighbourSum<2 or neighbourSum>3:
        return 0
    if neighbourSum==3:
        return 1
    if neighbourSum==2:
        return array[y][x]
''' For testing purposes
l = numpyRandom.randint(2,size=(10,10))
print l
print getSumNeighbourCells(l,-1,2)
'''
