#from Tkinter import *
from utilities import *
from numpy import *
from settings import *
from gameOfLife import *
import h5py
from tkFileDialog import *
#from tkMessageBox import *

#For MatPlotLib visualization
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib

#Chaco
from traits.api import *
from traitsui.api import *
from chaco.api import *
from enable.api import *
from enable.component_editor import *
from chaco.tools.api import PanTool

#threading
from threading import Thread, Timer
from time import sleep

class App(HasTraits):
    #col1
    KILL_LOOP=False
    rows=[Instance(Group)]*8
    
    width = Int(100)
    self.width = width
    rows[0] = Group('width',orientation='horizontal')
    
    height = Int(100)
    self.height = height
    rows[1] = Group('height',orientation='horizontal')
    
    timestep=Int(TIMESTEP)
    self.TS = timestep
    rows[2] = Group('timestep',orientation='horizontal')
    
    _restart=Button('Restart')
    set_dimensions=Button()
    rows[3] = Group(Item('_restart',show_label=False),'set_dimensions',orientation='horizontal')
    
    _play = Button('Play')
    _pause = Button('Pause')
    rows[4] = Group(Item('_play',show_label=False),Item('_pause',show_label=False),orientation='horizontal')
    
    export=Button()
    select_export=File()
    rows[5] = Group('export','select_export',orientation='horizontal')
    
    imprt=Button()
    select_import=File(filter=['*.hdf5'])
    rows[6] = Group('imprt','select_import',orientation='horizontal')
    
    new_file=Button()
    rows[7] = Group('new_file',orientation='horizontal')
    
    column_1 = Group([i for i in rows],
                    orientation='vertical')
    #col3
    plot=Instance(Plot())

    view = View(Group(column_1,Item('plot',
                                    editor=ComponentEditor(),
                                    show_label=False),
                      orientation='horizontal'))
    
    def __init__(self):
        super(App,self).__init__()
        self.updateObject = None
        """update object is the
        reference/pointer to our update function"""
        cols = 3
        #set columns across
        rws = 7
        #set rows down

        self.dimensions = (100,100)
        
        ##################
        ### Graphics
        ##################

        self.GOLHandler = gameOfLife(WIDTH,HEIGHT)
        self.display()

        self.updateObject = Timer(0.1,self.updateBoard)
        self.updateObject.start()

        ##############
        ### End Graphics
        ##############
        

    def updateDimensions(self):
        self.restart()

    def display(self): 
        plotdata=ArrayPlotData(imagedata=self.GOLHandler.board)
        plot=Plot(plotdata)
        self.plotdata = plotdata
        plot.img_plot('imagedata',colomap=jet)
        plot.tools.append(PanTool(plot))
        self.plot=plot

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
        #Starts continuous board loop
        if not self.KILL_LOOP:
            self.updateObject = Timer(0.1,self.updateBoard)
            self.updateObject.start()
        else:
            self.updateObject=None
            self.KILL_LOOP=False

    def pause(self):
        self.__pause_fired()
        
    def play(self):
        self.__play_fired()
        
    def __play_fired(self):
        if self.updateObject==None:
            self.updateBoard()
            
    def __pause_fired(self):
        self.KILL_LOOP=True

    def _export_fired(self):
        self.exportDataset()

    def _imprt_fired(self):
        self.importDataset()

    def exportDataset(self):
        if not self.select_export.split('.')[-1]=='hdf5':
            showinfo(title="Warning!", message="No valid file!")
        else:
            f = h5py.File(self.select_export,'a')
            try:
                t = f['/default']
                del f['/default']
                f['/default'] = self.GOLHandler.board
            except KeyError:
                f.create_dataset("default",data=self.GOLHandler.board)
            f.close()

    def importDataset(self):
        if not self.select_import.split('.')[-1]=='hdf5':
            showinfo(title='Warning!', message="No valid file!")
        else:
            try:
                f = h5py.File(self.select_import,'r+')
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

    def _width_changed(self):
        self.pause()
        self.dimensions = (self.width, self.dimensions[1])
        self.restart()

    def _height_changed(self):
        self.pause()
        self.dimensions = (self.dimensions[0],self.height)
        self.restart()

    def __restart_fired(self):
        self.restart()
        
    def restart(self, array=None): #defaults to random board unless board is put in
        x, y = self.dimensions
        self.GOLHandler.restart(x,y, array)
        self.display()
        
    def timeStepUpdate(self,*args):
        self.TS = float(self.timeStep.get())
            

App().configure_traits()
