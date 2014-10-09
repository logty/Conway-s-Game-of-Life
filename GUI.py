from Tkinter import *
from utilities import *
from numpy import *
from settings import *
from gameOfLife import *
import h5py
from tkFileDialog import *
from tkMessageBox import *

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

        self.TS = TIMESTEP
        
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
                                   text="Export",
                                   command = self.exportDataset
                                   ).grid(row = 5, column = 0)
        self.importButton = Button(master,
                                   text="Import",
                                   command = self.importDataset
                                   ).grid(row = 6, column = 0)
        self.newFileButton = Button(master,
                                    text="New File!",
                                    command = self.createNewFile
                                    ).grid(row=7,column=0,columnspan=2)

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
        
        timeStepTextVar = StringVar(master)
        timeStepTextVar.set('0.1')
        timeStepGUI = apply(OptionMenu,
                              (master,timeStepTextVar)+tuple(TIME_STEP_OPTIONS))
        #TIME_STEP_OPTIONS stored in settings file
        timeStepGUI.grid(row=2,column=1)
        self.timeStep = timeStepTextVar
        self.timeStep.trace('w',self.timeStepUpdate)
        #Trace binds a function to a change in the text
        
        self.setDimensions = Button(master, text="Set Dimensions", command=self.updateDimensions).grid(row = 3, column = 1)
        self.pauseButton = Button(master, text="Pause", command=self.pause).grid(row = 4, column = 1)

        self.exportDataButton = Button(master,
                                       text=SELECT_FILE_TEXT,
                                       command=self.getExportFile,
                                       relief=GROOVE)
        self.exportDataButton.grid(row=5,column=1)
        self.exportDataFile = SELECT_FILE_TEXT
        
        self.importDataButton = Button(master,
                                 text=SELECT_FILE_TEXT,
                                 command=self.getImportFile,
                                 relief=GROOVE)
        self.importDataButton.grid(row = 6, column = 1)
        self.importDataFile=SELECT_FILE_TEXT
        
        #self.importData = Button(master,"No file selected

        ##############
        ### Column 3
        ##############

        ''' Canvas, Blank, Blank'''
        
        self.GOLHandler = gameOfLife(WIDTH,HEIGHT)
        self.display()

        ##############
        ### End Graphics
        ##############
        
    def update(self):
        self.updateBoard()
        self.updateObject = self.master.after(int(self.TS*1000),self.update)

    def updateDimensions(self):
        self.restart()

    def display(self): #Plots the given board given by GOL Handler
        f = Figure(figsize=(5,5), dpi=DPI)
        a = f.add_subplot(111)
        a.imshow(self.GOLHandler.board,cmap='hot',interpolation='nearest')
        self.canvas = FigureCanvasTkAgg(f,master=self.master)
        self.canvas._tkcanvas.grid(row=0,column=2,rowspan=8)

    def canvasDimGet(self):
        #Error handling, if Canvas dimensions not integers default to 100
        try:
            temp_x = int(float(self.canvasWidth.get()))
        except ValueError:
            temp_x = 100
            self.canvasWidth.delete(0,END)
            self.canvasWidth.insert(0,'100')
        try:
            temp_y = int(float(self.canvasHeight.get()))
        except ValueError:
            temp_y = 100
            self.canvasHeight.delete(0,END)
            self.canvasHeight.insert(0,'100')
        return (temp_x,temp_y)
    
    def updateBoard(self):
        self.GOLHandler.getNextBoard()
        self.display()
        
    def play(self):
        if self.updateObject==None:
            self.updateObject = self.master.after(int(1000*self.TS),self.update)
            
    def pause(self):
        if not self.updateObject==None:
            self.master.after_cancel(self.updateObject)
            self.updateObject=None

    def exportDataset(self):
        if not self.exportDataFile.split('.')[-1]=='hdf5':
            showinfo(title="Warning!", message="No valid file!")
        else:
            f = h5py.File(self.exportDataFile,'a')
            try:
                t = f['/default']
                del f['/default']
                f['/default'] = self.GOLHandler.board
            except KeyError:
                f.create_dataset("default",data=self.GOLHandler.board)
            f.close()

    def importDataset(self):
        if not self.importDataFile.split('.')[-1]=='hdf5':
            showinfo(title='Warning!', message="No valid file!")
        else:
            try:
                f = h5py.File(self.importDataFile,'r+')
                t = f['/default']
                self.restart(t[:])
                f.close()
            except IOError:
                self.importData.insert(0,'No existe!')
            
    def getExportFile(self,temp_file=None):
        if not temp_file==None:
            self.exportDateFile=temp_file
        else:
            self.exportDataFile=askopenfilename(parent=self.master,
                                                  filetypes=[('HDF5','*.hdf5')])
        
        print self.exportDataFile + "Why isn't this working?????"
        if self.exportDataFile=='':
            self.exportDataFile=SELECT_FILE_TEXT
        self.exportDataButton.config(text=self.exportDataFile.split('/')[-1])

    def getImportFile(self):
        self.importDataFile = askopenfilename(parent=self.master,
                                              filetypes=[('HDF5','*.hdf5')])
        if self.importDataFile=='':
            self.importDataFile=SELECT_FILE_TEXT
        self.importDataButton.config(text=self.importDataFile.split('/')[-1])

    def createNewFile(self):
        l = asksaveasfilename(parent=self.master,
                              filetypes=[('HDF5','*.hdf5')])
        self.getExportFile( l)
    
    def restart(self, array=None): #defaults to random board unless board is put in
        x, y = self.canvasDimGet()
        self.GOLHandler.restart(x,y, array)
        self.display()
        
    def timeStepUpdate(self,*args):
        self.TS = float(self.timeStep.get())
root = Tk()
app = App(root)
root.mainloop()
#root.destroy()
