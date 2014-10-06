from numpy import random as numpyRandom
import numpy as np
import copy
import utilities as util
import time
from settings import *

#Array format 
'''array([[ 0.14022471,  0.96360618],  
       [ 0.37601032,  0.25528411],  
       [ 0.49313049,  0.94909878]]) '''

class gameOfLife:
    def __init__(self,width,height,array=None): #auto generates array, 2-dimensional
        self.restart(width,height,array)
        

    def getNextBoard(self):
        sumBoard = [[0]*WIDTH]*HEIGHT
        
        print time.clock()
        oldBoard = copy.deepcopy(self.board) #make an old copy for reference
        for j in range(1,self.height-1): #ignores edge cells
            for i in range(1,self.width-1):
                self.board[j][i]=util.getCell(oldBoard,i,j)
        print time.clock()

    def restart(self,  width,height,array=None):
        if array==None:
            self.height = height
            self.width = width
            self.board = numpyRandom.randint(2,size=(height,width)).astype(bool) #filled with 0,1
        else:
            self.board = array
            self.height = len(array) #tells us the height of the first column
            self.width = len(array[0]) #tells us the width of the first row
        
