from Tkinter import *
from utilities import *
from numpy import *
from settings import *
from gameOfLife import *
from PIL import Image, ImageTk

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
                                    command = self.updateBoard).grid(row = 3, column = 0)
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
        
        self.canvas = Canvas(master,
                             width=WIDTH,
                             height=HEIGHT,
                             relief = "sunken",
                             bd = 4)
        self.canvas.grid(row=0,column=2, rowspan = 7)

        self.canvasImage = PhotoImage(width=WIDTH, height = HEIGHT)#Image.new("RGB",(WIDTH,HEIGHT),color='blue')#
        self.GOLHandler = gameOfLife(WIDTH,HEIGHT)
        setPixels(self.canvasImage, self.GOLHandler.board)
        self.canvas.create_image((5+WIDTH/2,5+HEIGHT/2),image = self.canvasImage)#ImageTk.PhotoImage(
        
    def update(self):
        self.updateObject = self.master.after(TIMESTEP,self.update)

    def updateDimensions(self):
        self.canvas.configure(width=int(float(self.canvasWidth.get())))
        self.canvas.configure(height=int(float(self.canvasHeight.get())))

    def updateBoard(self):
        self.GOLHandler.getNextBoard()
        setPixels(self.canvasImage, self.GOLHandler.board)
        self.canvas.create_image((5+WIDTH/2,5+HEIGHT/2),
                                 image = self.canvasImage)
        
    def play(self):
        if self.updateObject==None:
            self.updateObject = self.master.after(100,self.update)
            
    def pause(self):
        if not self.updateObject==None:
            self.master.after_cancel(self.updateObject)
            self.updateObject=None

root = Tk()
app = App(root)
root.mainloop()
root.destroy()
