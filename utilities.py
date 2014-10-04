from numpy import random as numpyRandom
import numpy as np
from settings import *
import time
from PIL import Image, ImageTk

def getSumNeighbourCells(array,x,y):
    if x<1 or x > len(array[0]) or y < 1 or y > len(array):
        print 'problemo!'
        return 0
    return sum([array[y+j][x+i] for j in range(-1,2) for i in range(-1,2) if not (i==0 and j==0)])

def getCell(array,x,y):
    neighbourSum = getSumNeighbourCells(array,x,y)
    if neighbourSum<2 or neighbourSum>3:
        return False
    if neighbourSum==3:
        return True
    if neighbourSum==2:
        return array[y][x]

def pixel(image, pos, color):
    r,g,b = color
    x,y = pos
    image.put("#%02x%02x%02x" % (r,g,b), (y, x))

def setPixels(image, array):
    
    print 'setPixels:' + str(time.clock())
    for j in range(len(array)):
        for i in range(len(array[0])):
            pixel(image,(i,j),np.multiply(DEF_COLOR,array[j][i]))
    '''
    for j in range(len(array)):
        for i in range(len(array[0])):
            pixel(image,(i,j),np.multiply(DEF_COLOR,array[j][i]))
    image = ImageTk.PhotoImage(Image.fromarray(np.multiply(array, DEF_COLOR)))'''
    print time.clock()
