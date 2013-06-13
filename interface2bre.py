# -*- coding: utf-8 -*-
# Interface2.py
"""Graphical User Interface
This creates the bits and buttons for the interface.
Variables and names are also defined here. This is the
first layer of change if the program needs to be extended.
Anything that has to do with layout or appearance might be found here."""

# importing libraries
import matplotlib
import ttk
import sys
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib import pyplot as plt
import Tkinter as tki
from pfCalculates import *
from manips import *
import numpy as nm


class Controlset(Manips):
    """CS - Controlset. This class creates the GUI with all important
    Elements. Major changes and calculations will be executed
    in the Calculation-Class"""
    def __init__(self):
        self.buildGUI()
        return

    def myclose(self):
        sys.exit(0)
        return

    def buildGUI(self):
        if __name__ == '__main__':
            self.mainw = tki.Tk()
            self.mainw.protocol("WM_DELETE_WINDOW", self.myclose)  # Exit properly
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
            self.main.grid_rowconfigure(0, weight=1)  # row 0 grows 1:1
            self.main.grid_rowconfigure(1, weight=1)  # row 1 grows 1:1
            self.main.grid_columnconfigure(0, weight=1)  # column 0 grow 1:1
            self.main.grid_columnconfigure(1, weight=0)  # column 1 always stays as is

            ### Information display
            # A Frame to put the textbox and its scrollbar in.
            self.infoframe = tki.Frame(self.main)  # , bg='yellow')  # Yellow color for debugging
            self.infoframe.grid(row=0, rowspan=2, column=1, sticky=tki.N+tki.S+tki.E+tki.W)
            self.infoframe.grid_columnconfigure(0, weight=1)
            self.infoframe.grid_rowconfigure(0, weight=1)
            # Creating the Textbox with a fixed width of 50 characters
            self.info = tki.Text(self.infoframe, width=50)
            self.info.grid(row=0, column=0, sticky=tki.N+tki.S+tki.E+tki.W)
            # Creating a scrollbar for the textbox
            self.sbar = ttk.Scrollbar(self.infoframe)
            # Connect the yview command to the scrollbar
            self.sbar.config(command=self.info.yview)
            self.info.config(yscrollcommand=self.sbar.set)
            self.sbar.grid(row=0, column=1, sticky=tki.N+tki.S+tki.E+tki.W)
            # insert initial text into textbox
            self.info.insert(tki.END, self.boxtext)
            # scroll to the end of the textbox
            self.info.yview(tki.END)
            # disable writing to prevent users from writing into the textbox.
            self.info.config(state=tki.DISABLED)

            ### Menus under the canvas, axes, particleselector and objects
            self.displaymenu = ttk.Notebook(self.main)
            self.displaymenu.grid(row=4, column=0, sticky='NSWE')

            ### Menu containing field for DropDown.
            self.drawselect = tki.Frame()  # , bg='red')
            self.particleselector = tki.Frame()
            self.drawselect.grid_columnconfigure(0, weight=1)
            self.particleselector.grid_columnconfigure(0, weight=1)
            self.displaymenu.add(self.drawselect, text='Axes')
            self.displaymenu.add(self.particleselector, text='Particle picker')

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
            #[x,nghs,nghp,ngvs,ngvp,nuhs,nuhp,nuvs,nuvp,shs,shp,svs,svp,nwhs,nwhp,nwvs,nwvp,re];
            #[0  1    2    3    4    5    6    7    8   9   10  11  12  13   14   15   16   17]
            # numerical = +4
            # stokes = +8
            # newton = +12
            # dat2=[duration,trelax,VTSN,VTSS,nusv,re];
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
                             'Path-Time-Horizontal', 'Path-Time-Vertical', 'Trajectory',
                             'Reynolds')
            self.viewslc = ('Topview', 'View from X', 'View from Y', 'Corner', 'Reynolds')
            # Dict for the corresponding options
            self.viewopt = {'Topview': (0, 0, 4, 5, 0, 'X-Distance in [m]', 'Y-Distance in [m]', '', 'X-Y Trajecotry Projection'),
                            'View from X': (1, 0, 4, 6, 0, 'X-Distance in [m]', 'Z-Distance in [m]', '', 'X-Z Trajecotry Projection'),
                            'View from Y': (2, 0, 5, 6, 0, 'Y-Distance in [m]', 'Z-Distance in [m]', '', 'Y-Z Trajecotry Projection'),
                            'Corner': (3, 1, 4, 5, 6, 'X-Distance in [m]', 'Y-Distance in [m]', 'Z-Distance in [m]', 'Trajectory'),
                            'Reynolds': (4, 0, 0, 7, 0, 'Time in [s]', 'Reynoldsnumber', '', 'Renolds')}
            # Tuple with indeces of relevant columns for the plot, axis labels
            # Needs to be adapted to octave output! - Dependency!
            self.drawopt = {'Speed-Time-Horizontal': (0, 1, 'Time in [s]', 'Speed in [m/s]'),
                            'Path-Time-Horizontal': (0, 2, 'Time in [s]', 'Distance in [m]'),
                            'Speed-Time-Vertical': (0, 3, 'Time in [s]', 'Speed in [m/s]'),
                            'Path-Time-Vertical': (0, 4, 'Time in [s]', 'Distance in [m]'),
                            'Trajectory': (2, 4, 'Horizontal distance in [m]', 'Vertical distance in [m]'),
                            'Reynolds': (0, 17, 'Time in [s]', 'Reynoldsnumber')}
            # Creating the actual dropdown-menu and naming the corresponding labels
            # View version for 3D mode
            self.drawselectmview = ttk.Combobox(self.drawselect, values=self.viewslc, textvariable=self.view)
            self.drawselectmview.grid(row=0, column=0, columnspan=2, sticky="NSWE")
            # Draw version for 2D mode
            self.drawselectm = ttk.Combobox(self.drawselect, values=self.linesslc, textvariable=self.lines)
            self.drawselectm.grid(row=0, column=0, columnspan=2, sticky="NSWE")

            ### Parameters entries menus
            # Wrapping Notebook to set up parameters menus
            self.parameters = ttk.Notebook(self.main)
            self.parameters.grid(row=2, rowspan=4, column=1, sticky="SWE")
            # Single particle, Multiple particles and config Tab
            self.parasingpart = tki.Frame()
            self.paramultpart = tki.Frame()
            self.paraconfig = tki.Frame()

            # Add to Notebook
            self.parameters.add(self.parasingpart, text='Single particle')
            self.parameters.add(self.paramultpart, text='Multiple particles')
            self.parameters.add(self.paraconfig, text='Configuration')

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
            self.dpent.insert(0, 900)
            # velocity
            self.velent = ttk.Entry(self.parasingpart, validate='key', validatecommand=vcmd, width=10)
            self.velent.insert(0, 9)
            # angle elevation
            self.angleeent = ttk.Entry(self.parasingpart, validate='key', validatecommand=vcmd, width=10)
            self.angleeent.insert(0, 80)
            # angle azimut
            self.angleaent = ttk.Entry(self.parasingpart, validate='key', validatecommand=vcmd, width=10)
            self.angleaent.insert(0, 30)
            # Initial Position X
            self.posxent = ttk.Entry(self.parasingpart, validate='key', validatecommand=vcmd, width=10)
            self.posxent.insert(0, 0)
            # Initial Position Y
            self.posyent = ttk.Entry(self.parasingpart, validate='key', validatecommand=vcmd, width=10)
            self.posyent.insert(0, 0)
            # Initial Position Z
            self.poszent = ttk.Entry(self.parasingpart, validate='key', validatecommand=vcmd, width=10)
            self.poszent.insert(0, 0)
            # Run Button
            self.RunButton1 = ttk.Button(self.parasingpart, text='Run',
                                         command=self.RunThis2s)

            # Creating labels next to corresponding entry-boxes
            self.rhoplab = ttk.Label(self.parasingpart, text='Density in kg/m³')
            self.dplab = ttk.Label(self.parasingpart, text='Particle size in µm')
            self.vellab = ttk.Label(self.parasingpart, text='Velocity in m/s')
            self.angleelab = ttk.Label(self.parasingpart, text='Elevation in deg°')
            self.anglealab = ttk.Label(self.parasingpart, text='Azimuth in deg° (3D)')
            self.posxlab = ttk.Label(self.parasingpart, text='Initial X-Position in m')
            self.posylab = ttk.Label(self.parasingpart, text='Initial Y-Position in m')
            self.poszlab = ttk.Label(self.parasingpart, text='Initial Z-Position in m')

            # Positioning everything in the grid
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
            self.posxlab.grid(row=5, column=0, sticky="E")
            self.posxent.grid(row=5, column=2, sticky="E")
            self.posylab.grid(row=6, column=0, sticky="E")
            self.posyent.grid(row=6, column=2, sticky="E")
            self.poszlab.grid(row=7, column=0, sticky="E")
            self.poszent.grid(row=7, column=2, sticky="E")
            self.RunButton1.grid(row=8, column=0, sticky="SW")
            self.RunButton1.bind('<Return>', self.RunThiss)

            ### Multiple particles
            ## Elements
            # Number of particles
            self.partnumentm = ttk.Entry(self.paramultpart, width=10)
            self.partnumentm.insert(0, 10)
            # Density
            self.rhopentm = ttk.Entry(self.paramultpart, width=10)
            self.rhopentm.insert(0, '2900-2900')
            # diameter
            self.dpentm = ttk.Entry(self.paramultpart, width=10)
            self.dpentm.insert(0, '1000-1000')
            # velocity
            self.velentm = ttk.Entry(self.paramultpart, width=10)
            self.velentm.insert(0, '15-15')
            # angle lift
            self.angleeentm = ttk.Entry(self.paramultpart, width=10)
            self.angleeentm.insert(0, '20-50')
            # angle turn
            self.angleaentm = ttk.Entry(self.paramultpart, width=10)
            self.angleaentm.insert(0, '0-0')
            # Initial Position
            self.posxentm = ttk.Entry(self.paramultpart, width=10)
            self.posxentm.insert(0, '0-0')
            self.posyentm = ttk.Entry(self.paramultpart, width=10)
            self.posyentm.insert(0, '0-3')
            self.poszentm = ttk.Entry(self.paramultpart, width=10)
            self.poszentm.insert(0, '0-0')
            # Run Button
            self.RunButton1m = ttk.Button(self.paramultpart, text='Run',
                                          command=self.RunThis2m)
            # Set, Range, Random options
            self.multselval = ('Set', 'Range', 'Random')
            # Numb
            self.multpartslcnum = tki.StringVar(self.paramultpart)
            self.multselpartnum = ttk.Combobox(self.paramultpart, values=self.multselval,
                                               textvariable=self.multpartslcnum)
            # rhop
            self.multpartslcrhop = tki.StringVar(self.paramultpart)
            self.multselrhop = ttk.Combobox(self.paramultpart, values=self.multselval,
                                            textvariable=self.multpartslcrhop)
            self.multselrhop.set('Range')
            # dp
            self.multpartslcdp = tki.StringVar(self.paramultpart)
            self.multseldp = ttk.Combobox(self.paramultpart, values=self.multselval,
                                          textvariable=self.multpartslcdp)
            self.multseldp.set('Range')
            # v
            self.multpartslcvel = tki.StringVar(self.paramultpart)
            self.multselvel = ttk.Combobox(self.paramultpart, values=self.multselval,
                                           textvariable=self.multpartslcvel)
            self.multselvel.set('Range')
            # anglee
            self.multpartslcanglee = tki.StringVar(self.paramultpart)
            self.multselanglee = ttk.Combobox(self.paramultpart, values=self.multselval,
                                              textvariable=self.multpartslcanglee)
            self.multselanglee.set('Range')
            # anglea
            self.multpartslcanglea = tki.StringVar(self.paramultpart)
            self.multselanglea = ttk.Combobox(self.paramultpart, values=self.multselval,
                                              textvariable=self.multpartslcanglea)
            self.multselanglea.set('Range')
            # Position X
            self.multpartslcposx = tki.StringVar(self.paramultpart)
            self.multselposx = ttk.Combobox(self.paramultpart, values=self.multselval,
                                            textvariable=self.multpartslcposx)
            self.multselposx.set('Range')
            # Position Y
            self.multpartslcposy = tki.StringVar(self.paramultpart)
            self.multselposy = ttk.Combobox(self.paramultpart, values=self.multselval,
                                            textvariable=self.multpartslcposy)
            self.multselposy.set('Range')
            # Position Z
            self.multpartslcposz = tki.StringVar(self.paramultpart)
            self.multselposz = ttk.Combobox(self.paramultpart, values=self.multselval,
                                            textvariable=self.multpartslcposz)
            self.multselposz.set('Range')

            # Creating labels next to corresponding entry-boxes
            self.partnumlabm = ttk.Label(self.paramultpart, text='Number of particles')
            self.rhoplabm = ttk.Label(self.paramultpart, text='Density in kg/m³')
            self.dplabm = ttk.Label(self.paramultpart, text='Particle size in µm')
            self.vellabm = ttk.Label(self.paramultpart, text='Velocity in m/s')
            self.angleelabm = ttk.Label(self.paramultpart, text='Elevation in deg°')
            self.anglealabm = ttk.Label(self.paramultpart, text='Azimuth in deg° (3D)')
            self.posxlabm = ttk.Label(self.paramultpart, text='Initial X-Position in m')
            self.posylabm = ttk.Label(self.paramultpart, text='Initial Y-Position in m')
            self.poszlabm = ttk.Label(self.paramultpart, text='Initial Z-Position in m')

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
            self.posxlabm.grid(row=6, column=0, sticky="W")
            self.posxentm.grid(row=6, column=2, sticky="E")
            self.posylabm.grid(row=7, column=0, sticky="W")
            self.posyentm.grid(row=7, column=2, sticky="E")
            self.poszlabm.grid(row=8, column=0, sticky="W")
            self.poszentm.grid(row=8, column=2, sticky="E")
            self.multselrhop.grid(row=1, column=1, sticky="W")
            self.multseldp.grid(row=2, column=1, sticky="W")
            self.multselvel.grid(row=3, column=1, sticky="W")
            self.multselanglee.grid(row=4, column=1, sticky="W")
            self.multselanglea.grid(row=5, column=1, sticky="W")
            self.multselposx.grid(row=6, column=1, sticky="W")
            self.multselposy.grid(row=7, column=1, sticky="W")
            self.multselposz.grid(row=8, column=1, sticky="W")
            self.RunButton1m.grid(row=9, column=0, sticky="SW")
            self.RunButton1m.bind('<Return>', self.RunThis2m)

            ### Configuration
            ## Elements
            # Environment LabelFrame
            self.enviframe = ttk.LabelFrame(self.paraconfig, text='Environment')
            # Solver LabelFrame
            self.solframe = ttk.LabelFrame(self.paraconfig, text='Solver')
            # Precision
            self.precent = ttk.Entry(self.solframe, validate='key', validatecommand=vcmd, width=10)
            self.precent.insert(0, 200)
            # Duration
            self.durationent = ttk.Entry(self.solframe, validate='key', validatecommand=vcmd, width=10)
            self.durationent.insert(0, 3)
            # Box for Wind entries
            self.windbox = ttk.Frame(self.enviframe)
            # Wind in X
            self.windxent = ttk.Entry(self.windbox, validate='key', validatecommand=vcmd, width=3)
            self.windxent.insert(0, 0)
            # Wind in Y
            self.windyent = ttk.Entry(self.windbox, validate='key', validatecommand=vcmd, width=3)
            self.windyent.insert(0, 0)
            # Wind in Z
            self.windzent = ttk.Entry(self.windbox, validate='key', validatecommand=vcmd, width=3)
            self.windzent.insert(0, 0)
            # Gravitiy
            self.gravent = ttk.Entry(self.enviframe, validate='key', validatecommand=vcmd, width=10)
            self.gravent.insert(0, 9.81)
            # Fluid Density
            self.rhogent = ttk.Entry(self.enviframe, validate='key', validatecommand=vcmd, width=10)
            self.rhogent.insert(0, 1.205)
            # Fluid Viscosity
            self.etaent = ttk.Entry(self.enviframe, validate='key', validatecommand=vcmd, width=10)
            self.etaent.insert(0, 1.81e-5)
            # Creating labels next to corresponding entry-boxes
            self.preclab = ttk.Label(self.solframe, text='Precision/Steps')
            self.durationlab = ttk.Label(self.solframe, text='Duration in s')
            self.windlab = ttk.Label(self.enviframe, text='X-Y-Z Wind in m/s')
            self.gravlab = ttk.Label(self.enviframe, text='Gravity in m/s²')
            self.rhoglab = ttk.Label(self.enviframe, text='Fluid Density in kg/m³')
            self.etalab = ttk.Label(self.enviframe, text='Fluid Dyn. Visc. in Pa s')

            # Positioning
            self.enviframe.grid(row=0, column=0, columnspan=3, sticky="SNEW")
            self.solframe.grid(row=1, column=0, columnspan=3, sticky="SNEW")
            self.preclab.grid(row=0, column=0, sticky="W")
            self.precent.grid(row=0, column=2, sticky="E")
            self.durationlab.grid(row=1, column=0, sticky="W")
            self.durationent.grid(row=1, column=2, sticky="E")
            self.windlab.grid(row=0, column=0, sticky="W")
            self.windbox.grid(row=0, column=2, sticky="SNEW")
            self.windxent.grid(row=0, column=0, padx=1, sticky="E")
            self.windyent.grid(row=0, column=1, padx=1, sticky="E")
            self.windzent.grid(row=0, column=2, padx=1, sticky="E")
            self.gravlab.grid(row=1, column=0, sticky="W")
            self.gravent.grid(row=1, column=2, sticky="E")
            self.rhoglab.grid(row=2, column=0, sticky="W")
            self.rhogent.grid(row=2, column=2, sticky="E")
            self.etalab.grid(row=3, column=0, sticky="W")
            self.etaent.grid(row=3, column=2, sticky="E")

            ### Control buttons
            # Configuring grid
            self.parasingpart.grid_columnconfigure(1, weight=1)
            self.paramultpart.grid_columnconfigure(1, weight=1)
            self.paraconfig.grid_columnconfigure(1, weight=1)
            self.enviframe.grid_columnconfigure(1, weight=1)
            self.solframe.grid_columnconfigure(1, weight=1)
            #self.progressbar.grid(row=6, column=0, sticky="E")

            ### Canvas for drawings
            # Creating a figure of desired size
            self.f = plt.figure(figsize=(5.5, 5.5), dpi=100, facecolor='white')
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
            self.axisscaleframe = tki.Frame(self.drawselect)  # , bg='magenta')
            self.axisscaleframe.grid(row=1, column=0, columnspan=3, sticky='SNEW')
            # In that Frame, some Entry-boxes to specify the scale
            self.xaxisscalef = ttk.Entry(self.axisscaleframe, width=10, validate='key', validatecommand=vcmd)
            self.xaxisscalet = ttk.Entry(self.axisscaleframe, width=10, validate='key', validatecommand=vcmd)
            self.yaxisscalef = ttk.Entry(self.axisscaleframe, width=10, validate='key', validatecommand=vcmd)
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
            # Another Checkbutton for logarithmic scale of x
            self.chlogxvar = tki.IntVar()
            self.checklogx = ttk.Checkbutton(self.axisscaleframe, text="log(x)",
                                             command=self.log, variable=self.chlogxvar)
            # Another Checkbutton for logarithmic scale of y
            self.chlogyvar = tki.IntVar()
            self.checklogy = ttk.Checkbutton(self.axisscaleframe, text="log(y)",
                                             command=self.log, variable=self.chlogyvar)
            # 3D Mode Button
            self.set3DButton = tki.Button(self.axisscaleframe, text="3D mode is off",
                                          command=self.set3dstate, bg='green', relief='raised')
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
            self.checklogx.grid(row=1, column=3, sticky='W')
            self.checklogy.grid(row=2, column=3, sticky='W')
            self.scaleset.grid(row=3, column=3, sticky='E')
            self.checknewton.grid(row=1, column=4, sticky='W')
            self.checkstokes.grid(row=2, column=4, sticky='W')
            self.checkgrid.grid(row=0, column=4, sticky='W')
            self.set3DButton.grid(row=3, column=4, sticky="EW")

            ### The particle picker in a treeview
            self.picker = ttk.Treeview(self.particleselector, height=6)
            self.picker['columns'] = ('Nr', 'dp', 'rhop', 'v', 'elevation',
                                      'azimuth', 'Initial X-Pos',
                                      'Initial Y-Pos', 'Initial Z-Pos')
            self.picker['displaycolumns'] =[1, 2, 3, 4, 5, 6, 7, 8]
            self.picker.column('#0', width=40, anchor=tki.CENTER, stretch=True)
            self.picker.column('dp', width=80, stretch=True)
            self.picker.column('rhop', width=90, stretch=True)
            self.picker.column('v', width=60, stretch=True)
            self.picker.column('elevation', width=80, stretch=True)
            self.picker.column('azimuth', width=80, stretch=True)
            self.picker.column('Initial X-Pos', width=60, stretch=True)
            self.picker.column('Initial Y-Pos', width=60, stretch=True)
            self.picker.column('Initial Z-Pos', width=60, stretch=True)
            self.picker.heading('#0', text='ID')
            self.picker.heading('dp', text='dp in µm', anchor=tki.W)
            self.picker.heading('rhop', text='rhop in kg/m³', anchor=tki.W)
            self.picker.heading('v', text='v in m/s', anchor=tki.W)
            self.picker.heading('elevation', text='elev. in °deg', anchor=tki.W)
            self.picker.heading('azimuth', text='azim. in °deg', anchor=tki.W)
            self.picker.heading('Initial X-Pos', text='X in m', anchor=tki.W)
            self.picker.heading('Initial Y-Pos', text='Y in m', anchor=tki.W)
            self.picker.heading('Initial Z-Pos', text='Z in m', anchor=tki.W)
            self.picker.grid(row=0, column=0, sticky='NSWE')
            self.picker.bind('<<TreeviewSelect>>', self.pickclick)
            self.set3dstate()
        else:
            print "aha, "+__name__+" imported that file"
        return
if __name__ == '__main__':
    CS1 = Controlset()
    CS1.mainw.mainloop()
