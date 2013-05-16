# -*- coding: utf-8 -*-
# Interface2.py
"""Graphical User Interface for plotting the results
calculated in the script: Wurfp3.m and Wurf3D.m in Octave -
Simulation of particle flight"""

# importing libraries
import matplotlib
import ttk
# import threading
matplotlib.use('TkAgg')
#import numpy as nm
#import decimal as dc
#import pylab as pl
#from mpl_toolkits.mplot3d import axes3d
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
# from oct2py import octave as oc
import Tkinter as tki
from pfCalculates import *
from manips import *


class Controlset(Manips):
    """CS - Controlset. This class creates the GUI with all important
    Elements. Major changes and calculations will be executed
    in the Calculation-Class in a seperate thread. This prevents the
    GUI from hanging"""
    def __init__(self):
        self.buildGUI()

    def buildGUI(self):
        if __name__ == '__main__':
            self.mainw = tki.Tk()
            self.mainw.title("Partikelflug")
            self.mainw.geometry('+10+10')
            self.set3dstatevar = 1  # 3D mode is on and will be disabled
            self.boxtext = 'Status information:\n'
            ### Entire Window
            # Mainframe that contains everything.
            self.main = tki.Frame(self.mainw)
            # Pack manager to expand the mainframe as the windowsize changes.
            self.main.pack(fill=tki.BOTH, expand=tki.YES)
            # Configure the grid of the mainframe so that only the top left
            # cell grows if the users expands the window.
            self.main.grid_rowconfigure(0, weight=1)
            self.main.grid_rowconfigure(1, weight=1)
            #self.main.grid_rowconfigure(2, weight=1)
            self.main.grid_columnconfigure(0, weight=1)
            self.main.grid_columnconfigure(1, weight=0)

            ### Information display
            # A Frame to put the textbox and its scrollbar in.
            self.infoframe = tki.Frame(self.main, bg='yellow')
            self.infoframe.grid(row=0, rowspan=2, column=1, sticky=tki.N+tki.S+tki.E+tki.W)
            self.infoframe.grid_columnconfigure(0, weight=1)
            self.infoframe.grid_rowconfigure(0, weight=1)
            # Creating the Textbox with a fixed width of 20 characters
            self.info = tki.Text(self.infoframe, width=50)
            self.info.grid(row=0, column=0, sticky=tki.N+tki.S+tki.E+tki.W)
            # Creating a scrollbar for the textbox
            self.sbar = ttk.Scrollbar(self.infoframe)
            # connect the yview command to the scrollbar
            self.sbar.config(command=self.info.yview)
            self.info.config(yscrollcommand=self.sbar.set)
            self.sbar.grid(row=0, column=1, sticky=tki.N+tki.S+tki.E+tki.W)
            # insert initial text into textbox
            self.info.insert(tki.END, self.boxtext)
            # scroll to the end of the textbox
            self.info.yview(tki.END)
            # disable writing to prevent users from writing into the textbox.
            self.info.config(state=tki.DISABLED)

            ### Menu containing field for DropDown.
            self.drawselect = tki.Frame(self.main)  # , bg='red')
            self.drawselect.grid_columnconfigure(0, weight=1)
            self.drawselect.grid(row=4, column=0, sticky='NSWE')

            ### DropDownMenu for drawing selection.
            # Button for the redraw-option.
            self.redraw = ttk.Button(self.drawselect, text='Draw', command=self.redraw2)
            # Also react if user hits Return.
            self.redraw.bind('<Return>', self.redraw)
            self.redraw.grid(row=0, column=2, sticky="NSWE")

            ### This is a little help in order to understand how to configure the
            ### different drawing-options:
            # Return from octave: ng=numerical coupled, nu= numerical, s = stokes, n =newton
            # h = horizontal, v = vertical, s = speed, p = path:
            # e.g. nuhp= numerical horizontal path
            #[x,nghs,nghp,ngvs,ngvp,nuhs,nuhp,nuvs,nuvp,shs,shp,svs,svp,nwhs,nwhp,nwvs,nwvp];
            #[0  1    2    3    4    5    6    7    8   9   10  11  12  13   14   15   16]
            # numerical = +4
            # stokes = +8
            # newton = +12
            # dat2=[duration,trelax,VTSN,VTSS,nusv];
            # Setting up the options in a dictionary
            # First string: Option as shown in GUI

            # Declare variable for the dropdown-menu.
            self.lines = tki.StringVar(self.drawselect)
            self.view = tki.StringVar(self.drawselect)
            # Set standard Variable.
            self.lines.set('Speed-Time-Horizontal')
            self.view.set('Corner')
            # Create selectionlist for Dropdown Menu
            self.linesslc = ('Speed-Time-Horizontal', 'Speed-Time-Vertical',
                             'Path-Time-Horizontal', 'Path-Time-Vertical', 'Trajectory')
            self.viewslc = ('Topview', 'View from X', 'View from Y', 'Corner')
            self.viewopt = {'Topview': (90, 0),
                            'View from X': (0, 0),
                            'View from Y': (1, 0),
                            'Corner': (35, 215)}
            # Tuple with indeces of relevant columns for the plot, axis labels
            self.drawopt = {'Speed-Time-Horizontal': (0, 1, 'Time in [s]', 'Speed in [m/s]'),
                            'Path-Time-Horizontal': (0, 2, 'Time in [s]', 'Distance in [m]'),
                            'Speed-Time-Vertical': (0, 3, 'Time in [s]', 'Speed in [m/s]'),
                            'Path-Time-Vertical': (0, 4, 'Time in [s]', 'Distance in [m]'),
                            'Trajectory': (2, 4, 'Horizontal distance in [m]', 'Vertical distance in [m]')}
            # Creating the actual dropdown-menu and naming the corresponding labels
            self.drawselectmview = ttk.Combobox(self.drawselect, values=self.viewslc, textvariable=self.view)
            self.drawselectmview.grid(row=0, column=0, columnspan=2, sticky="NSWE")
            self.drawselectm = ttk.Combobox(self.drawselect, values=self.linesslc, textvariable=self.lines)
            self.drawselectm.grid(row=0, column=0, columnspan=2, sticky="NSWE")

            ### Parameters entries menus
            # Wrapping Notebook to set up parameters menus
            self.parameters = ttk.Notebook(self.main)
            self.parameters.grid(row=3, rowspan=3, column=1, sticky="SWE")
            self.parasingpart = tki.Frame()
            self.paramultpart = tki.Frame()
            self.para2D = tki.Frame()
            self.para3D = tki.Frame()
            # Add to Notebook
            self.parameters.add(self.parasingpart, text='Single particle')
            self.parameters.add(self.paramultpart, text='Multiple particles')
            self.parameters.add(self.para2D, text='2D Setup')
            self.parameters.add(self.para3D, text='3D Setup')
            # Creating multiple entry-boxes for the corresponding parameters
            # validation command
            vcmd = (self.parasingpart.register(self.validate),
                    '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

            ### Single particle
            ## Elements
            # Density
            self.rhopent = ttk.Entry(self.parasingpart, validate='key', validatecommand=vcmd, width=10)
            self.rhopent.insert(0, 7800)
            # diameter
            self.dpent = ttk.Entry(self.parasingpart, validate='key', validatecommand=vcmd, width=10)
            self.dpent.insert(0, 200)
            # velocity
            self.velent = ttk.Entry(self.parasingpart, validate='key', validatecommand=vcmd, width=10)
            self.velent.insert(0, 6)
            # angle lift
            self.angleeent = ttk.Entry(self.parasingpart, validate='key', validatecommand=vcmd, width=10)
            self.angleeent.insert(0, 35)
            # angle turn
            self.angleaent = ttk.Entry(self.parasingpart, validate='key', validatecommand=vcmd, width=10)
            self.angleaent.insert(0, 30)
            # Run Button 2D
            self.RunButton1 = ttk.Button(self.parasingpart, text='Run',
                                         command=self.RunThis2s)

            # Creating labels next to corresponding entry-boxes
            self.rhoplab = ttk.Label(self.parasingpart, text='Density in kg/m³')
            self.dplab = ttk.Label(self.parasingpart, text='Particle size in µm')
            self.vellab = ttk.Label(self.parasingpart, text='Velocity in m/s')
            self.angleelab = ttk.Label(self.parasingpart, text='Elevation in deg°')
            self.anglealab = ttk.Label(self.parasingpart, text='Azimuth in deg° (3D)')

            # Positioning
            self.rhoplab.grid(row=0, column=0, sticky="W")
            self.rhopent.grid(row=0, column=2, sticky="E")
            self.dplab.grid(row=1, column=0, sticky="W")
            self.dpent.grid(row=1, column=2, sticky="E")
            self.vellab.grid(row=2, column=0, sticky="W")
            self.velent.grid(row=2, column=2, sticky="E")
            self.angleelab.grid(row=3, column=0, sticky="W")
            self.angleeent.grid(row=3, column=2, sticky="E")
            self.anglealab.grid(row=4, column=0, sticky="W")
            self.angleaent.grid(row=4, column=2, sticky="E")
            self.RunButton1.grid(row=5, column=0, sticky="SW")
            self.RunButton1.bind('<Return>', self.RunThiss)

            ### Multiple particles
            ## Elements
            # Number of particles
            self.partnumentm = ttk.Entry(self.paramultpart, width=10)
            self.partnumentm.insert(0, 10)
            # Density
            self.rhopentm = ttk.Entry(self.paramultpart, width=10)
            self.rhopentm.insert(0, '2900-9000')
            # diameter
            self.dpentm = ttk.Entry(self.paramultpart, width=10)
            self.dpentm.insert(0, '50-500')
            # velocity
            self.velentm = ttk.Entry(self.paramultpart, width=10)
            self.velentm.insert(0, '1-50')
            # angle lift
            self.angleeentm = ttk.Entry(self.paramultpart, width=10)
            self.angleeentm.insert(0, '5-50')
            # angle turn
            self.angleaentm = ttk.Entry(self.paramultpart, width=10)
            self.angleaentm.insert(0, '5-50')
            # Run Button 2D
            self.RunButton1m = ttk.Button(self.paramultpart, text='Run',
                                          command=self.RunThis2m)
            # Set, Range, Random options
            self.multselval = ('Set', 'Range', 'Random')
            #numb
            self.multpartslcnum = tki.StringVar(self.paramultpart)
            self.multselpartnum = ttk.Combobox(self.paramultpart, values=self.multselval,
                                               textvariable=self.multpartslcnum)
            #rhop
            self.multpartslcrhop = tki.StringVar(self.paramultpart)
            self.multselrhop = ttk.Combobox(self.paramultpart, values=self.multselval,
                                            textvariable=self.multpartslcrhop)
            self.multselrhop.set('Range')
            #dp
            self.multpartslcdp = tki.StringVar(self.paramultpart)
            self.multseldp = ttk.Combobox(self.paramultpart, values=self.multselval,
                                          textvariable=self.multpartslcdp)
            self.multseldp.set('Range')
            #V
            self.multpartslcvel = tki.StringVar(self.paramultpart)
            self.multselvel = ttk.Combobox(self.paramultpart, values=self.multselval,
                                           textvariable=self.multpartslcvel)
            self.multselvel.set('Range')
            #anglee
            self.multpartslcanglee = tki.StringVar(self.paramultpart)
            self.multselanglee = ttk.Combobox(self.paramultpart, values=self.multselval,
                                              textvariable=self.multpartslcanglee)
            self.multselanglee.set('Range')
            #anglea
            self.multpartslcanglea = tki.StringVar(self.paramultpart)
            self.multselanglea = ttk.Combobox(self.paramultpart, values=self.multselval,
                                              textvariable=self.multpartslcanglea)
            self.multselanglea.set('Range')

            # Creating labels next to corresponding entry-boxes
            self.partnumlabm = ttk.Label(self.paramultpart, text='Number of particles')
            self.rhoplabm = ttk.Label(self.paramultpart, text='Density in kg/m³')
            self.dplabm = ttk.Label(self.paramultpart, text='Particle size in µm')
            self.vellabm = ttk.Label(self.paramultpart, text='Velocity in m/s')
            self.angleelabm = ttk.Label(self.paramultpart, text='Elevation in deg°')
            self.anglealabm = ttk.Label(self.paramultpart, text='Azimuth in deg° (3D)')

            # Positioning
            self.partnumlabm.grid(row=0, column=0, sticky="W")
            self.partnumentm.grid(row=0, column=2, sticky="W")
            self.rhoplabm.grid(row=1, column=0, sticky="W")
            self.rhopentm.grid(row=1, column=2, sticky="E")
            self.dplabm.grid(row=2, column=0, sticky="W")
            self.dpentm.grid(row=2, column=2, sticky="E")
            self.vellabm.grid(row=3, column=0, sticky="W")
            self.velentm.grid(row=3, column=2, sticky="E")
            self.angleelabm.grid(row=4, column=0, sticky="W")
            self.angleeentm.grid(row=4, column=2, sticky="E")
            self.anglealabm.grid(row=5, column=0, sticky="W")
            self.angleaentm.grid(row=5, column=2, sticky="E")
            # self.multselpartnum.grid(row=0, column=1, sticky="W")
            self.multselrhop.grid(row=1, column=1, sticky="W")
            self.multseldp.grid(row=2, column=1, sticky="W")
            self.multselvel.grid(row=3, column=1, sticky="W")
            self.multselanglee.grid(row=4, column=1, sticky="W")
            self.multselanglea.grid(row=5, column=1, sticky="W")
            self.RunButton1m.grid(row=6, column=0, sticky="SW")
            self.RunButton1m.bind('<Return>', self.RunThis2m)

            ### 2D Setup
            ## Elements
            # Precision
            self.precent2d = ttk.Entry(self.para2D, validate='key', validatecommand=vcmd, width=10)
            self.precent2d.insert(0, 500)
            # Duration
            self.durationent2d = ttk.Entry(self.para2D, validate='key', validatecommand=vcmd, width=10)
            self.durationent2d.insert(0, 0)
            # Wind in X
            self.windxent2d = ttk.Entry(self.para2D, validate='key', validatecommand=vcmd, width=10)
            self.windxent2d.insert(0, 0)
            # Wind in Y
            self.windyent2d = ttk.Entry(self.para2D, validate='key', validatecommand=vcmd, width=10)
            self.windyent2d.insert(0, 0)
            # Run Button 2D
            self.RunButton2d = ttk.Button(self.para2D, text='Run', command=self.RunThis2s)

            # Creating labels next to corresponding entry-boxes
            self.preclab2d = ttk.Label(self.para2D, text='Precision/Steps')
            self.durationlab2d = ttk.Label(self.para2D, text='Duration in s')
            self.windxlab2d = ttk.Label(self.para2D, text='Horizontal wind in m/s')
            self.windylab2d = ttk.Label(self.para2D, text='Vertical wind in m/s')

            # Positioning
            self.preclab2d.grid(row=0, column=0, sticky="W")
            self.precent2d.grid(row=0, column=2, sticky="E")
            self.durationlab2d.grid(row=1, column=0, sticky="W")
            self.durationent2d.grid(row=1, column=2, sticky="E")
            self.windxlab2d.grid(row=2, column=0, sticky="W")
            self.windxent2d.grid(row=2, column=2, sticky="E")
            self.windylab2d.grid(row=3, column=0, sticky="W")
            self.windyent2d.grid(row=3, column=2, sticky="E")
            self.RunButton2d.grid(row=5, column=0, sticky="SW")
            self.RunButton2d.bind('<Return>', self.RunThis2s)

            ### 3D Setup
            ## Elements
            # Precision
            self.precent3d = ttk.Entry(self.para3D, validate='key', validatecommand=vcmd, width=10)
            self.precent3d.insert(0, 500)
            # Duration
            self.durationent3d = ttk.Entry(self.para3D, validate='key', validatecommand=vcmd, width=10)
            self.durationent3d.insert(0, 0)
            # Wind in X
            self.windxent3d = ttk.Entry(self.para3D, validate='key', validatecommand=vcmd, width=10)
            self.windxent3d.insert(0, 0)
            # Wind in Y
            self.windyent3d = ttk.Entry(self.para3D, validate='key', validatecommand=vcmd, width=10)
            self.windyent3d.insert(0, 0)
            # Wind in Z
            self.windzent3d = ttk.Entry(self.para3D, validate='key', validatecommand=vcmd, width=10)
            self.windzent3d.insert(0, 0)
            # Run Button 2D
            self.RunButton3d = ttk.Button(self.para3D, text='Run', command=self.RunThis2s)

            # Creating labels next to corresponding entry-boxes
            self.preclab3d = ttk.Label(self.para3D, text='Precision/Steps')
            self.durationlab3d = ttk.Label(self.para3D, text='Duration in s')
            self.windxlab3d = ttk.Label(self.para3D, text='Horizontal x-wind in m/s')
            self.windylab3d = ttk.Label(self.para3D, text='Horizontal y-wind in m/s')
            self.windzlab3d = ttk.Label(self.para3D, text='Vertical z-wind in m/s')

            # Positioning
            self.preclab3d.grid(row=0, column=0, sticky="W")
            self.precent3d.grid(row=0, column=2, sticky="E")
            self.durationlab3d.grid(row=1, column=0, sticky="W")
            self.durationent3d.grid(row=1, column=2, sticky="E")
            self.windxlab3d.grid(row=2, column=0, sticky="W")
            self.windxent3d.grid(row=2, column=2, sticky="E")
            self.windylab3d.grid(row=3, column=0, sticky="W")
            self.windyent3d.grid(row=3, column=2, sticky="E")
            self.windzlab3d.grid(row=4, column=0, sticky="W")
            self.windzent3d.grid(row=4, column=2, sticky="E")
            self.RunButton3d.grid(row=5, column=0, sticky="SW")
            self.RunButton3d.bind('<Return>', self.RunThis2s)

            ### Control buttons
            # configuring grid
            self.parasingpart.grid_columnconfigure(1, weight=1)
            self.paramultpart.grid_columnconfigure(1, weight=1)
            self.para2D.grid_columnconfigure(1, weight=1)
            self.para3D.grid_columnconfigure(1, weight=1)
            #self.progressbar.grid(row=6, column=0, sticky="E")

            ### Canvas for drawings
            # Creating a figure of desired size
            self.f = Figure(figsize=(6.5, 6.5), dpi=100, facecolor='white')
            # Creating a canvas that lives inside the figure
            self.Paper = FigureCanvasTkAgg(self.f, master=self.main)
            # Making the canvas's drawings visible (updating)
            self.Paper.show()
            # positioning the canvas
            self.Paper.get_tk_widget().grid(row=0, rowspan=3, column=0, sticky='NSWE')
            # creating a toolbarframe for options regarding the plots
            self.toolbarframe = tki.Frame(self.main)  # , bg='black')
            self.toolbarframe.grid(row=3, column=0, sticky='NWE')
            # Creating a toolbar for saving, zooming etc. (matplotlib standard)
            self.toolbar = NavigationToolbar2TkAgg(self.Paper, self.toolbarframe)
            self.toolbar.grid(row=0, column=0, sticky='NWE')
            # setting the standard option on zoom
            self.toolbar.zoom()

            ### Axis configuration toolbar
            # A frame containing the axis config-menu
            self.axisscaleframe = tki.Frame(self.main)  # , bg='magenta')
            self.axisscaleframe.grid(row=5, column=0, sticky='SNEW')
            # In that Frame, some Entry-boxes to specify scale
            self.xaxisscalef = ttk.Entry(self.axisscaleframe, width=10, validate='key', validatecommand=vcmd)
            # put some standard value in the entry box
            self.yaxisscalef = ttk.Entry(self.axisscaleframe, width=10, validate='key', validatecommand=vcmd)
            self.xaxisscalet = ttk.Entry(self.axisscaleframe, width=10, validate='key', validatecommand=vcmd)
            self.yaxisscalet = ttk.Entry(self.axisscaleframe, width=10, validate='key', validatecommand=vcmd)
            self.zaxisscalef = ttk.Entry(self.axisscaleframe, width=10, validate='key', validatecommand=vcmd)
            self.zaxisscalet = ttk.Entry(self.axisscaleframe, width=10, validate='key', validatecommand=vcmd)
            # And some Labels so we know what the boxes are for
            self.xaxlab = ttk.Label(self.axisscaleframe, text='X-Axis', width=10)
            self.yaxlab = ttk.Label(self.axisscaleframe, text='Y-Axis', width=10)
            self.zaxlab = ttk.Label(self.axisscaleframe, text='Z-Axis', width=10)
            self.axinfolab = ttk.Label(self.axisscaleframe, text='Adjust axis scale:')
            # And a Button to validate the desired configuration
            self.scaleset = ttk.Button(self.axisscaleframe, text='Set', command=self.SetAxis2)
            self.scaleset.bind('<Return>', self.SetAxis)
            # Declare variable for the checkbutton (0/1) for newton
            # This checkbutton is used to call shownewton2
            self.chnwvar = tki.IntVar()
            self.checknewton = ttk.Checkbutton(self.axisscaleframe, text="Show results for Newton",
                                               command=self.shownewton2, variable=self.chnwvar)
            # Declare variable for the checkbutton (0/1) for Stokes
            # This checkbutton is used to call showstokes2
            self.chstvar = tki.IntVar()
            self.checkstokes = ttk.Checkbutton(self.axisscaleframe, text="Show results for Stokes",
                                               command=self.showstokes2, variable=self.chstvar)
            # Declare variable for the checkbutton (0/1) for the Grid
            # This checkbutton is used to call DrawGrid2
            self.chdrawgrid = tki.IntVar()
            self.chdrawgrid.set(1)
            self.checkgrid = ttk.Checkbutton(self.axisscaleframe, text="Show gridlines",
                                             command=self.DrawGrid, variable=self.chdrawgrid)
            # Run Button 3D
            self.set3DButton = tki.Button(self.axisscaleframe, text="3D mode is off",
                                          command=self.set3dstate, bg='orange', relief='raised')
            # Let's organize all this in the axisscaleframe-grid
            self.axinfolab.grid(row=0, column=0, sticky='W')
            self.xaxlab.grid(row=1, column=0, sticky='W')
            self.yaxlab.grid(row=2, column=0, sticky='W')
            self.zaxlab.grid(row=3, column=0, sticky='W')
            self.xaxisscalef.grid(row=1, column=1, sticky='W')
            self.yaxisscalef.grid(row=2, column=1, sticky='W')
            self.xaxisscalet.grid(row=1, column=2, sticky='W')
            self.yaxisscalet.grid(row=2, column=2, sticky='W')
            self.zaxisscalef.grid(row=3, column=1, sticky='W')
            self.zaxisscalet.grid(row=3, column=2, sticky='W')
            self.scaleset.grid(row=3, column=3, sticky='E')
            self.checknewton.grid(row=1, column=4, sticky='W')
            self.checkstokes.grid(row=2, column=4, sticky='W')
            self.checkgrid.grid(row=0, column=4, sticky='W')
            self.set3DButton.grid(row=3, column=4, sticky="EW")
            self.set3dstate()
        else:
            print "aha, "+__name__+" imported that file"
if __name__ == '__main__':
    CS1 = Controlset()
    CS1.mainw.mainloop()
# CS1.mainloop()