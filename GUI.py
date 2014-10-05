from Tkinter import *
from utilities import *
from numpy import *
from settings import *
from gameOfLife import *
from PIL import Image, ImageTk

#For MatPlotLib visualization
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib

class App:
    def __init__(self,master):
        self.master = master #master = the Tk root
        self.updateObject = None
        """update object is the
        reference/pointer to our update function"""
        cols = 3
        #set columns across
        rws = 7
        #set rows down
        
        ##################
        ### Graphics
        ##################
        
        ##############
        ### Column 0
        ##############
        
        ''' Label, Label, Label, Play Button,
            Restart Button, Export Button, Import Button'''
        Label(master, text="Width").grid(row = 0, column = 0)
        Label(master, text="Height").grid(row = 1, column = 0)
        Label(master, text="Timestep").grid(row = 2, column = 0)
        self.playButton = Button(master,
                                 text="Play",
                                 command=self.play).grid(row = 4, column = 0)
        self.restartButton = Button(master,
                                    text="Restart",
                                    command = self.restart).grid(row = 3, column = 0)
        self.exportButton = Button(master,
                                   text="Export").grid(row = 5, column = 0)
        self.importButton = Button(master,
                                   text="Import").grid(row = 6, column = 0)

        ##############
        ### Column 1
        ##############

        ''' Canvas Width, Canvas Height, Timestep, Pause Button,
            Set Dimensions, Input, Input'''
        self.canvasWidth = Entry(master)
        self.canvasWidth.insert(0,str(WIDTH))
        self.canvasWidth.grid(row = 0, column = 1)
        
        self.canvasHeight = Entry(master)
        self.canvasHeight.insert(0,str(HEIGHT))
        self.canvasHeight.grid(row = 1, column = 1)
        
        self.timeStep = Entry(master)
        self.timeStep.insert(0,TIMESTEP)
        self.timeStep.grid(row = 2, column = 1)
        
        self.setDimensions = Button(master, text="Set Dimensions", command=self.updateDimensions).grid(row = 3, column = 1)
        self.pauseButton = Button(master, text="Pause", command=self.pause).grid(row = 4, column = 1)
        
        Entry(master).grid(row = 5, column = 1)
        Entry(master).grid(row = 6, column = 1)


        ##############
        ### Column 3
        ##############

        ''' Canvas, Blank, Blank'''
        
        self.GOLHandler = gameOfLife(WIDTH,HEIGHT)
        self.display()
        
    def update(self):
        self.updateBoard()
        self.updateObject = self.master.after(int(TIMESTEP*1000),self.update)

    def updateDimensions(self):
        self.restart()

    def display(self):
        f = Figure(figsize=(5,5), dpi=DPI)
        a = f.add_subplot(111)
        a.imshow(self.GOLHandler.board,cmap='hot',interpolation='nearest')
        self.canvas = FigureCanvasTkAgg(f,master=self.master)
        self.canvas._tkcanvas.grid(row=0,column=2,rowspan=7)

    def canvasDimGet(self):
        return (int(float(self.canvasWidth.get())),int(float(self.canvasHeight.get())))
    
    def updateBoard(self):
        self.GOLHandler.getNextBoard()
        self.display()
        
    def play(self):
        if self.updateObject==None:
            self.updateObject = self.master.after(100,self.update)
            
    def pause(self):
        if not self.updateObject==None:
            self.master.after_cancel(self.updateObject)
            self.updateObject=None
    
    def restart(self, array=None): #defaults to random board unless board is put in
        x, y = self.canvasDimGet()
        self.GOLHandler.restart(x,y, array)
        self.display()
        

root = Tk()
app = App(root)
root.mainloop()
#root.destroy()
