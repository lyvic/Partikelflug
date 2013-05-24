# -*- coding: utf-8 -*-
# manips.py
"""This file contains all functions and methods we need to process
the data input from the interface. It does all manipulations necessary.
The core of any feature should be found here."""

# Importing modules
import time
import numpy as nm
import random
from oct2py import octave as oc
from mpl_toolkits.mplot3d import axes3d  # This moduls is needed!
import Tkinter as tki
import multiprocessing
from pfCalculates import *


### The following functions are outside of the manips class
### Why? I don't really know, but otherwise the multiprocessing doesn't work.
# Multiparticle calculations
def multipcalc(data, mode='2d'):
    begin = time.time()
    # Counting the number of available CPUs in System
    pool_size = multiprocessing.cpu_count()
    # Creating a pool of processes with the maximal number of CPUs possible
    pool = multiprocessing.Pool(processes=pool_size)
    # Call the corresponding function depending on 2D or 3D mode
    if mode == '3d':
        results = pool.map_async(calculate_m3d, data).get()
    else:
        results = pool.map_async(calculate_m, data).get()
    # Properly close and end all processes, once we're done
    pool.close()
    pool.join()
    end = time.time()
    print (end-begin)
    return results


# Function to be called for multiple particles in 2D mode
# Receives all parameters needed in a list: indata
def calculate_m(indata):
    # This might print oddly as we haven't applied any locks
    print 'Reading values and calling Octave'
    # Calling octave
    [Calculate.y, Calculate.y2] = \
        oc.call('Wurfp3.m', [indata],
                verbose=False)  # For debugging change to TRUE or use octave
    print 'Done! Data from Octave available'
    return [Calculate.y, Calculate.y2]


# Function to be called for multiple particles in 3D mode
# Receives all parameters needed in a list: indata
def calculate_m3d(indata):
    # This might print oddly as there are no locks used
    print 'Reading values and calling Octave'
    [Calculate.y, Calculate.y2] = \
        oc.call('Wurf3D.m', [indata],
                verbose=False)  # Use octave for debugging, keep on false
    print 'Done! Data from Octave available'
    return [Calculate.y, Calculate.y2]


### Manips class. Everything here is basically encapsuled
### I don't know if I really need this, but so far everything works.
class Manips(object):
    """Functions for manipulations"""
    # Since we are entering another class and applying the functions
    # and methods on external Objects, we call these externals 'guest'
    # This doesn't really make sense to me, but it works so far.
    def __init__(self, guest):
        self.guest = guest
        # Depending on the current dataset, functions are going to follow
        # different procedures
        self.currentdata = 0
        # 0=No Data; 1=2D single, 2=3D single, 3=2D multi, 4=3D multi
        pass

    # Change between 2D and 3D mode and enable/disable options
    def set3dstate(self):
        if self.set3dstatevar == 1:  # If 3D Mode is on
        # Turn 3D off
            self.set3dstatevar = 0
            self.set3DButton.configure(text="3D mode is off",
                                       bg='grey', relief='raised')
            self.zaxisscalef.state(['disabled'])
            self.zaxisscalet.state(['disabled'])
            self.checknewton.state(['!disabled'])
            self.checkstokes.state(['!disabled'])
            self.windyent.state(['disabled'])
            self.posyentm.state(['disabled'])
            self.posyent.state(['disabled'])
            self.drawselectmview.grid_forget()
            self.drawselectm.grid(row=0, column=0, columnspan=2, sticky="NSWE")
        else:
        # Turn 3D on
            self.set3dstatevar = 1
            self.set3DButton.configure(text="3D mode is on",
                                       bg='green', relief='sunken')
            self.zaxisscalef.state(['!disabled'])
            self.zaxisscalet.state(['!disabled'])
            self.checknewton.state(['disabled'])
            self.checkstokes.state(['disabled'])
            self.windyent.state(['!disabled'])
            self.posyentm.state(['!disabled'])
            self.posyent.state(['!disabled'])
            self.drawselectmview.grid(row=0, column=0,
                                      columnspan=2, sticky="NSWE")
            self.drawselectm.grid_forget()

    # Write a message into the info text-field
    def msgboard(self, message):
        self.info.config(state=tki.NORMAL)
        self.info.insert(tki.END, message)
        # Scroll to end of window.
        self.info.yview(tki.END)
        self.info.config(state=tki.DISABLED)

    def RunThiss(self, event):
        """Triggers Runthis2, event type will be ignored"""
        # This comes in handy if someone would like to run the program
        # just by focusing the button and hitting 'Return'
        self.RunThis2s()

    def RunThis2s(self):
        """Reads entries, prints status messages and calls
        the Calculate function in order to do some work"""
        # Read the given values for the variables.
        # If anything goes wrong here, of of the entries is not a number
        # or not convertibel to a float.
        try:
            self.rhop = float(self.rhopent.get())
            self.dp = float(self.dpent.get())
            self.v = float(self.velent.get())
            self.anglee = float(self.angleeent.get())
            self.prec = float(self.precent.get())
            self.duration = float(self.durationent.get())
            self.rhog = float(self.rhogent.get())
            self.eta = float(self.etaent.get())
            self.grav = float(self.gravent.get())
            self.windx = float(self.windxent.get())
            self.windz = float(self.windzent.get())
            self.posx = float(self.posxent.get())
            self.posz = float(self.poszent.get())
            if self.set3dstatevar == 0:  # If 2D Mode
                self.currentdata = 1  # Current Data is single particle 2D
                # Inform user about the configuration.
                self.entries = "Density: %.2f kg/m³ \n"\
                               "Particle size: %.2f µm\n" \
                               "Velocity: %.2f m/s \nElevation: %.2f°\n"\
                               "Precision set to %s \nDuration set to %s\n"\
                               "Gravity %s \nFluid Density set to %s\n"\
                               "Horizontal Wind: %.2f m/s\n"\
                               "Vertical Wind: %.2f m/s\n"\
                               "Initial Coordinates: %.2f horizontal %.2f vertical\n"\
                               "Calculations running, please wait ... \n" \
                               % (self.rhop, self.dp, self.v, self.anglee,
                                  self.prec, self.duration, self.grav, self.rhog,
                                  self.windx, self.windz, self.posx, self.posz)
            else:  # We are in 3D
                self.currentdata = 2  # Current Data is single particle 3D
                # In 3D we have two more options
                self.anglea = float(self.angleaent.get())
                self.windy = float(self.windyent.get())
                self.posy = float(self.posyent.get())
                # Inform user about the configuration.
                self.entries = "Density: %.2f kg/m³ \n"\
                               "Particle size: %.2f µm\n" \
                               "Velocity: %.2f m/s \n"\
                               "Elevation: %.2f°\nAzimuth: %.2f°\n"\
                               "Precision set to %s \nDuration set to %s\n"\
                               "Gravity %s \nFluid Density set to %s\n"\
                               "Wind in X: %.2f m/s\nWind in Y : %.2f m/s\n"\
                               "Wind in Z: %.2f m/s\n"\
                               "Initial Coordinates: %.2f x, %.2f y, horizontal\n"\
                               "%.2f z vertical\n"\
                               "Calculations running, please wait ... \n" \
                               % (self.rhop, self.dp, self.v, self.anglee, self.anglea,
                                  self.prec, self.duration,  self.grav, self.rhog,
                                  self.windx, self.windy, self.windz, self.posx, self.posy, self.posz)

        except ValueError:  # If reading the input fields failes
            self.message = "No valid values entered\n"
            self.msgboard(self.message)
            return
        # In case of success, we print the settings to the message board
        self.msgboard(self.entries)
        print 'RunThis2s called'  # Shows in prompt, not in GUI
        # Call Calculate, invokes a new thread in order to keep the
        # GUI alive while calculating (this would be nice for multiprocessing too)
        if self.set3dstatevar == 0:  # In 2D Mode
            CL = Calculate(self, self.rhop, self.rhog, self.dp, self.v, self.anglee,
                           self.prec, self.duration, self.eta, self.grav,
                           self.windx, self.windz, self.posx, self.posz)
            # Starts the new thread and the actual calculation
            CL.start()
        else:  # In 3D Mode
            CL = Calculate3D(self, self.rhop, self.dp, self.v, self.anglee,
                             self.anglea, self.prec, self.duration, self.windx,
                             self.windy, self.windz, self.rhog, self.eta, self.grav,
                             self.posx, self.posy, self.posz)
            # Starts the new thread and the actual calculation
            CL.start()

    def RunThis2m(self):
        """Reads entries, prints status messages and calls
        the Calculate function in order to do some work"""
        # Same principle as RunThis2s, but with a '-' to split
        # the entries from each other.
        try:
            # Creates tuples of two and processes them with self.ingen()
            # Depending on the mode, we get a set, range or random datainput
            self.rhopraw = tuple(map(float, self.rhopentm.get().split('-')))
            self.rhop = self.ingen(self.multpartslcrhop.get(), self.rhopraw)
            self.dpraw = tuple(map(float, self.dpentm.get().split('-')))
            self.dp = self.ingen(self.multpartslcdp.get(), self.dpraw)
            self.vraw = tuple(map(float, self.velentm.get().split('-')))
            self.v = self.ingen(self.multpartslcvel.get(), self.vraw)
            self.angleeraw = tuple(map(float, self.angleeentm.get().split('-')))
            self.anglee = self.ingen(self.multpartslcanglee.get(), self.angleeraw)
            self.posxraw = tuple(map(float, self.posxentm.get().split('-')))
            self.posx = self.ingen(self.multpartslcposx.get(), self.posxraw)
            self.poszraw = tuple(map(float, self.poszentm.get().split('-')))
            self.posz = self.ingen(self.multpartslcposz.get(), self.poszraw)
            # The following values should rather be fixed and not randomized. 
            self.prec = float(self.precent.get())
            self.duration = float(self.durationent.get())
            self.windx = float(self.windxent.get())
            self.windz = float(self.windzent.get())
            self.rhog = float(self.rhogent.get())
            self.eta = float(self.etaent.get())
            self.grav = float(self.gravent.get())
            if self.set3dstatevar == 0:  # In 2D Mode
                self.currentdata = 3  # Multiple particles in 2D
                # Inform user about the configuration.
                self.entries = "Density: %.2f to %.2f kg/m³ \n"\
                               "Particle size: %.2f to %.2f µm\n" \
                               "Velocity: %.2f to %.2f m/s \n"\
                               "Elevation: %.2f to %.2f°\n"\
                               "Precision set to %s \nDuration set to %s\n"\
                               "Horizontal Wind: %.2f m/s\n"\
                               "Vertical Wind: %.2f m/s\n"\
                               "Calculations running, please wait ... \n" \
                               % (self.rhopraw[0], self.rhopraw[1], self.dpraw[0],
                                  self.dpraw[1], self.vraw[0], self.vraw[1],
                                  self.angleeraw[0], self.angleeraw[1], self.prec,
                                  self.duration, self.windx, self.windz)
            else:  # in 3D Mode
                self.currentdata = 4  # Multiple particles in 3D
                # Here we have two more options to read
                self.anglearaw = tuple(map(float, self.angleaentm.get().split('-')))
                self.anglea = self.ingen(self.multpartslcanglea.get(), self.anglearaw)
                self.posyraw = tuple(map(float, self.posyentm.get().split('-')))
                self.posy = self.ingen(self.multpartslcposy.get(), self.posyraw)
                self.windy = float(self.windyent.get())
                # Inform user about the configuration.
                self.entries = "Density: %.2f to %.2f kg/m³ \n"\
                               "Particle size: %.2f to %.2f µm\n" \
                               "Velocity: %.2f to %.2f m/s \n"\
                               "Elevation: %.2f° to %.2f°\n"\
                               "Azimuth: %.2f° to %.2f°\n"\
                               "Precision set to %s \nDuration set to %s\n"\
                               "Wind in X: %.2f m/s\nWind in Y : %.2f m/s\n"\
                               "Wind in Z: %.2f m/s\n"\
                               "Calculations running, please wait ... \n" \
                               % (self.rhopraw[0], self.rhopraw[1], self.dpraw[0],
                                  self.dpraw[1], self.vraw[0], self.vraw[1],
                                  self.angleeraw[0], self.angleeraw[1], self.anglearaw[0],
                                  self.anglearaw[1], self.prec, self.duration, self.windx,
                                  self.windy, self.windz)

        except ValueError:  # If reading the values failes
            self.message = "No valid values entered\n"
            self.msgboard(self.message)
            return
        # If our parameters could be set up properly, we can proceed to calling octave
        self.msgboard(self.entries)
        print 'RunThis2m called'
        # Call Calculate, invokes a new thread in order to keep the
        # GUI alive while calculating
        if self.set3dstatevar == 0:  # In 2D Mode
            n = int(self.partnumentm.get())
            self.dataset = []
            for x in range(0, n):
                print x
                self.dataset.append((self.rhop[x], self.dp[x], self.v[x],
                                    self.anglee[x], self.prec, self.duration,
                                    self.windx, self.windz, self.rhog, self.eta,
                                    self.grav, self.posx[x], self.posz[x]))
        else:  # In 3D Mode (with more options)
            n = int(self.partnumentm.get())
            self.dataset = []
            for x in range(0, n):
                print x
                self.dataset.append((self.rhop[x], self.dp[x], self.v[x],
                                    self.anglee[x], self.anglea[x], self.prec,
                                    self.duration, self.windx, self.windy,
                                    self.windz, self.rhog, self.eta, self.grav,
                                    self.posx[x], self.posy[x], self.posz[x]))
        # These datasets need to be sent to Octave individually
        # But first we prepare the canvas for a new drawing
        self.f.clf()
        if self.set3dstatevar == 1:  # In 3D Mode
            self.a = self.f.add_subplot(111, projection='3d')
            self.f.subplots_adjust(bottom=0.05, left=0.05,
                                   right=0.95, top=0.95)
        else:  # In 2D Mode
            self.a = self.f.add_subplot(111)
            self.f.subplots_adjust(bottom=0.11, left=0.11,
                                   right=0.92, top=0.92)
        self.DrawGrid()
        self.a.ticklabel_format(style='sci', scilimits=(0, 0), axis='both')
        if self.set3dstatevar == 0:  # In 2D Mode
            self.multires = multipcalc(self.dataset)  # Processing the Data in octave multicore
            # Plotting the Data
            self.myplot(0, self.multires[0][0][:, 2], self.multires[0][0][:, 4], 'Time in [s]',
                        'Speed in [m/s]', pttl='Speed-Time-Horizontal')
            # Adding a line for every dataset
            for i in range(1, int(self.partnumentm.get())):
                self.a.plot(self.multires[i][0][:, 2], self.multires[i][0][:, 4])

        if self.set3dstatevar == 1:  # In 3D Mode
            self.multires = multipcalc(self.dataset, mode='3d') # Calling octave
            # Plotting the Data
            self.myplot(1, self.multires[0][0][:, 4],
                        self.multires[0][0][:, 5],
                        'XDistance in [m]',
                        'YDistance in [m]',
                        zttl='ZHeight in [m]',
                        zdat=self.multires[0][0][:, 6],
                        pttl='Trajectory')
            # Adding a line for every dataset
            for i in range(1, int(self.partnumentm.get())):
                self.a.plot(self.multires[i][0][:, 4], self.multires[i][0][:, 5],
                            self.multires[i][0][:, 6])
        # Update the canvas to show the plots
        self.Paper.show()

    # processing the input data to create the different datasets
    def ingen(self, gen_mode, valin):
        # Number of particle = Number of datasets
        n = int(self.partnumentm.get())
        # Output matrix
        valout = []
        # A set is the simple separation of input values by '-'
        if gen_mode == 'Set':
            valout = list(valin)
            print valout
            return valout
        # For Range, the given interval is split up in equally long sets
        elif gen_mode == 'Range':
            steps = (valin[1]-valin[0])/(n-1)
            valout = [valin[0]]
            for x in range(1, n):
                valout.append(valin[0]+steps*x)
            print valout
            return valout
        # For random, the values are randomly chosen from within the given interval
        elif gen_mode == 'Random':
            for i in range(1, n+1):
                valout.append(random.uniform(valin[0], valin[1]))
            print valout
            return valout
        else:
        # Otherwise none of the upper options was selected.
        # There might by nonsense in the option field.
            print "No, nothing happened"
        return

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
    # 3D Data
    # dat1=[ngt,ngxs,ngys,ngzs,ngxp,ngyp,ngzp];
    # dat2=[duration,trelax,VTSN,VTSS,nusv];
    # Setting up the options in a dictionary
    # First string: Option as shown in GUI

    def redraw(self, event):
        """Forwarding """
        self.redraw2()

    def redraw2(self):
        if self.set3dstatevar == 1:  # In 3D Mode
            self.viewin = self.view.get()
            self.msgboard('View: '+self.viewin+'\n')
            # self.info.config(state=tki.NORMAL)
            # self.viewid = str(self.viewopt[self.viewin])
            # self.info.insert(tki.END, 'View: '+self.viewin+'\n')
            # self.info.yview(tki.END)
            # self.info.config(state=tki.DISABLED)
            if self.currentdata == 2:  # If single particle 2D
                # Plot the corresponding data
                if self.viewopt[self.viewin][0] == 0:  # means X View
                    self.myplot(0, Calculate3D.y[:, 4], Calculate3D.y[:, 6],
                                'X Distance in [m]', 'Z Distance in [m]',
                                pttl='X-Z Trajecotry Projection')
                if self.viewopt[self.viewin][0] == 1:  # means Y View
                    self.myplot(0, Calculate3D.y[:, 5], Calculate3D.y[:, 6],
                                'Y Distance in [m]', 'Z Distance in [m]',
                                pttl='Y-Z Trajecotry Projection')
                if self.viewopt[self.viewin][0] == 90:  # means Topview
                    self.myplot(0, Calculate3D.y[:, 4], Calculate3D.y[:, 5],
                                'X Distance in [m]', 'Y Distance in [m]',
                                pttl='X-Y Trajecotry Projection')
                if self.viewopt[self.viewin][0] == 35:  # means Corner
                    self.myplot(1, Calculate3D.y[:, 4], Calculate3D.y[:, 5],
                                'XDistance in [m]', 'YDistance in [m]',
                                zttl='ZHeight in [m]', zdat=Calculate3D.y[:, 6],
                                pttl='Trajectory')
            if self.currentdata == 4:  # If multiple particle 3D Mode
                if self.viewopt[self.viewin][0] == 0:  # means X View
                    self.myplot(0, self.multires[0][0][:, 4], self.multires[0][0][:, 6],
                                'X Distance in [m]', 'Z Distance in [m]',
                                pttl='X-Z Trajecotry Projection')
                    for i in range(1, int(self.partnumentm.get())):
                        self.a.plot(self.multires[i][0][:, 4], self.multires[i][0][:, 6])
                if self.viewopt[self.viewin][0] == 1:  # means Y View
                    self.myplot(0, self.multires[0][0][:, 5], self.multires[0][0][:, 6],
                                'Y Distance in [m]', 'Z Distance in [m]',
                                pttl='Y-Z Trajecotry Projection')
                    for i in range(1, int(self.partnumentm.get())):
                        self.a.plot(self.multires[i][0][:, 5], self.multires[i][0][:, 6])
                if self.viewopt[self.viewin][0] == 90:  # means Topview
                    self.myplot(0, self.multires[0][0][:, 4], self.multires[0][0][:, 5],
                                'X Distance in [m]', 'Y Distance in [m]',
                                pttl='X-Y Trajecotry Projection')
                    for i in range(1, int(self.partnumentm.get())):
                        self.a.plot(self.multires[i][0][:, 4], self.multires[i][0][:, 5])
                if self.viewopt[self.viewin][0] == 35:  # means Corner
                    self.myplot(1, self.multires[0][0][:, 4],
                                self.multires[0][0][:, 5],
                                'XDistance in [m]',
                                'YDistance in [m]',
                                zttl='ZHeight in [m]',
                                zdat=self.multires[0][0][:, 6],
                                pttl='Trajectory')
                    for i in range(1, int(self.partnumentm.get())):
                        self.a.plot(self.multires[i][0][:, 4], self.multires[i][0][:, 5],
                                    self.multires[i][0][:, 6])

        else:  # We are in 2D Mode
            try:
                self.linesin = self.lines.get()
                self.msgboard('Drawing: '+self.linesin+'\n')
                # self.info.config(state=tki.NORMAL)
                # self.drawid = str(self.drawopt[self.linesin])
                # self.info.insert(tki.END, 'Drawing: '+self.linesin+'\n')
                # self.info.yview(tki.END)
                # self.info.config(state=tki.DISABLED)
                self.plotx = self.drawopt[self.linesin][0]
                self.ploty = self.drawopt[self.linesin][1]
                self.titlexax = self.drawopt[self.linesin][2]
                self.titleyax = self.drawopt[self.linesin][3]
                self.figtitle = self.linesin
                if self.currentdata == 1:  # Single particle in 2D
                    self.myplot(0, Calculate.y[:, self.plotx],
                                Calculate.y[:, self.ploty],
                                self.titlexax, self.titleyax,
                                pttl=self.figtitle)
                if self.currentdata == 3:  # Multiple particles in 2D
                    self.myplot(0, self.multires[0][0][:, self.plotx],
                                self.multires[0][0][:, self.ploty], 
                                self.titlexax, self.titleyax,
                                pttl=self.figtitle)
                    for i in range(1, int(self.partnumentm.get())):
                        self.a.plot(self.multires[i][0][:, self.plotx],
                                    self.multires[i][0][:, self.ploty])

                self.Paper.show()
                # Draw Stokes and Newton if checked
                if self.chnwvar.get() == 1:
                    self.shownewton2()
                if self.chstvar.get() == 1:
                    self.showstokes2()
            except AttributeError:
                # Somebody must have hit the Draw Button without creating any data
                print "No values for redraw2"
                pass
        # Make changes visible
        self.Paper.show()

    def shownewton(self, event):
        self.shownewton()

    def shownewton2(self):
        try:
            self.linesin = self.lines.get()
            self.nwplotx = self.drawopt[self.linesin][0]
            # This might be hard to understand: The numbers are refering to the indices
            # of the corresponding datasets. This is hard coded and can be looked up above.
            # It all depends on what octave returns.
            if self.nwplotx == 2:
                self.nwplotx = 14
            self.nwploty = self.drawopt[self.linesin][1]+12
            print "running shownewton2"
            if self.chnwvar.get() == 1:  # If the checkmark is set, draw the line
                self.newtonline = self.a.plot(Calculate.y[:, self.nwplotx],
                                              Calculate.y[:, self.nwploty],
                                              color='magenta')
                self.Paper.show()
            else:  # If the checkmark is not set, delete the line
                try:
                    l = self.newtonline.pop(0)
                    l.remove()
                    del l
                    self.Paper.show()
                except AttributeError or IndexError:
                    self.Paper.show()
        except AttributeError:
            # This happens if you check the CheckButton without having any data available
            print "No values for newton2"
            pass

    def showstokes(self, event):
        self.showstokes2()

    def showstokes2(self):
        try:
            # Very same priciple as for shownewton2 just above, with different indices of course
            self.linesin = self.lines.get()
            self.stplotx = self.drawopt[self.linesin][0]
            if self.stplotx == 2:
                self.stplotx = 10
            self.stploty = self.drawopt[self.linesin][1]+8
            print "running showstokes2"
            if self.chstvar.get() == 1:
                self.stokesline = self.a.plot(Calculate.y[:, self.stplotx],
                                              Calculate.y[:, self.stploty],
                                              color='red')
                self.Paper.show()
            else:
                try:
                    l = self.stokesline.pop(0)
                    l.remove()
                    del l
                    self.Paper.show()
                except IndexError or AttributeError:
                    self.Paper.show()
        except AttributeError:
            print "No values for stokes2"
            pass

    def DrawGrid(self):
        """A grid might improve the view"""
        try:
            if self.chdrawgrid.get() == 1:
                self.a.grid(True)
            else:
                self.a.grid(False)
            self.Paper.show()
        except AttributeError:
            print "No plot shown"

    def SetAxis(self, event):
        self.SetAxis2()

    def SetAxis2(self):
        """Scaling is quite important for a good data interpretation.
        So I made it very accessible in here"""
        self.viewset = self.view.get()
        # In 3D Mode Corner View:
        if self.set3dstatevar == 1 and self.viewopt[self.viewset][0] == 35:
            try:  # Reading the input
                self.x1 = float(self.xaxisscalef.get())
                self.x2 = float(self.xaxisscalet.get())
                self.y1 = float(self.yaxisscalef.get())
                self.y2 = float(self.yaxisscalet.get())
                self.z1 = float(self.zaxisscalef.get())
                self.z2 = float(self.zaxisscalet.get())
                if self.currentdata == 2:  # Single Particle 3D mode
                    # Has to undergo manual clipping as the mplot3D library
                    # Is not capable enough to properly display the lines
                    xclip, yclip, zclip =\
                        self.manclip(Calculate3D.y[:, 4]*1, Calculate3D.y[:, 5]*1,
                                     Calculate3D.y[:, 6]*1, (self.x1, self.x2),
                                     (self.y1, self.y2),
                                     (self.z1, self.z2))
                    # plotting processed data
                    self.myplot(1, xclip, yclip, 'XDistance in [m]',
                                'YDistance in [m]', zttl='ZHeight in [m]',
                                zdat=zclip, pttl='Trajectory')
                if self.currentdata == 4:  # Multiple Particle 3D
                    # Has to undergo manual clipping as the mplot3D library
                    # Is not capable enough to properly display the lines
                    xclip, yclip, zclip =\
                        self.manclip(self.multires[0][0][:, 4]*1,
                                     self.multires[0][0][:, 5]*1,
                                     self.multires[0][0][:, 6]*1,
                                     (self.x1, self.x2),
                                     (self.y1, self.y2),
                                     (self.z1, self.z2))
                    # plotting processed data
                    self.myplot(1, xclip, yclip, 'XDistance in [m]',
                                'YDistance in [m]', zttl='ZHeight in [m]',
                                zdat=zclip, pttl='Trajectory')
                    # plotting all other lines of the dataset
                    for i in range(1, int(self.partnumentm.get())):
                        xclip, yclip, zclip =\
                            self.manclip(self.multires[i][0][:, 4]*1,
                                         self.multires[i][0][:, 5]*1,
                                         self.multires[i][0][:, 6]*1,
                                         (self.x1, self.x2),
                                         (self.y1, self.y2),
                                         (self.z1, self.z2))
                        self.a.plot(xclip, yclip, zclip)
                # Finally, set the scale
                self.a.set_zlim(self.z1, self.z2)
                self.a.set_xlim(self.x1, self.x2)
                self.a.set_ylim(self.y1, self.y2)
            except ValueError:
                # If the values can't be converted to a float
                print "Something is wrong with the axis fields"
                pass
        else:  # This not 3D Mode and no corner view
            try:  # then it's simple since we need no manual clipping or anything
                self.x1 = float(self.xaxisscalef.get())
                self.x2 = float(self.xaxisscalet.get())
                self.y1 = float(self.yaxisscalef.get())
                self.y2 = float(self.yaxisscalet.get())
                self.a.set_xlim(self.x1, self.x2)
                self.a.set_ylim(self.y1, self.y2)
            except ValueError:
                # Bad input in the axis fields: strings or similar things. 
                print "Something is wrong with the axis fields"
                pass
        self.Paper.show()
        print "Set axis"

    def validate(self, action, index, value_if_allowed, prior_value, text,
                 validation_type, trigger_type, widget_name):
        # A little help for some value fields. Only allow certain charakters
        print text
        if text in 'e0123456789.-+':
            return True
        else:
            try:  # The insert method of the entry boxes need this version
                float(text)
                return True
            except ValueError:
                # Bad input
                return False

    def myplot(self, persp3D, xdat, ydat, xttl, yttl,
               zdat=nm.NaN, zttl=nm.NaN, pttl=''):
        """Plotting can be quite complicated, so I shortened my code by
        creating these routines for the most common cases"""
        self.f.clf()
        if persp3D == 1:
            self.a = self.f.add_subplot(111, projection='3d')
            self.f.subplots_adjust(bottom=0.05, left=0.05,
                                   right=0.95, top=0.95)
            self.a.plot(xdat, ydat, zdat)
            self.a.set_zlabel(zttl)
            self.a.mouse_init()
        else:
            self.a = self.f.add_subplot(111)
            self.f.subplots_adjust(bottom=0.11, left=0.11,
                                   right=0.92, top=0.92)
            self.a.plot(xdat, ydat)
        self.a.set_xlabel(xttl)
        self.a.set_ylabel(yttl)
        self.a.set_title(pttl)
        self.DrawGrid()
        self.a.ticklabel_format(style='sci', scilimits=(0, 0), axis='both')
        return

    # This function is not used yet, might become usefull later
    def myplot_add(self, persp3D, xdat, ydat, zdat=nm.NaN):
        if persp3D == 1:
            self.a.plot(xdat, ydat, zdat)
            self.a.mouse_init()
        else:
            self.a.plot(xdat, ydat, color='red')
        self.DrawGrid()
        return

    # Manual clipping for the screwed up view in mplot3D
    def manclip(self, xdat, ydat, zdat, xlim, ylim, zlim):
        #clipping manually
        for i in nm.arange(len(xdat)):
            if xdat[i] < xlim[0]:
                xdat[i] = nm.NaN
            if xdat[i] > xlim[1]:
                xdat[i] = nm.NaN
            else:
                pass

        for i in nm.arange(len(ydat)):
            if ydat[i] < ylim[0]:
                ydat[i] = nm.NaN
            if ydat[i] > ylim[1]:
                ydat[i] = nm.NaN
            else:
                pass

        for i in nm.arange(len(zdat)):
            if zdat[i] < zlim[0]:
                zdat[i] = nm.NaN
            if zdat[i] > zlim[1]:
                zdat[i] = nm.NaN
            else:
                pass
        return xdat, ydat, zdat
