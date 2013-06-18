# -*- coding: utf-8 -*-
# manips.py
"""This file contains all functions and methods we need to process
the data input from the interface. It does all manipulations necessary.
The core of any feature should be found here."""

# Importing modules
import numpy as nm
import random
import decimal as dc
from mpl_toolkits.mplot3d import axes3d  # This moduls is needed!
import Tkinter as tki
from pfCalculates import *
import multiprocessing


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
        return

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
        return

    # Write a message into the info text-field
    def msgboard(self, message):
        self.info.config(state=tki.NORMAL)
        self.info.insert(tki.END, message)
        # Scroll to end of window.
        self.info.yview(tki.END)
        self.info.config(state=tki.DISABLED)
        return

    def RunThiss(self, event):
        """Triggers Runthis2, event type will be ignored"""
        # This comes in handy if someone would like to run the program
        # just by focusing the button and hitting 'Return'
        self.RunThis2s()
        return

    def RunThis2s(self):
        """Reads entries, prints status messages and calls
        the Calculate function in order to do some work"""
        # Read the given values for the variables.
        # If anything goes wrong here, of of the entries is not a number
        # or not convertibel to a float.
        kill = self.picker.get_children()
        for item in kill:
            self.picker.delete(item)
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
            return
        else:  # In 3D Mode
            CL = Calculate3D(self, self.rhop, self.dp, self.v, self.anglee,
                             self.anglea, self.prec, self.duration, self.windx,
                             self.windy, self.windz, self.rhog, self.eta, self.grav,
                             self.posx, self.posy, self.posz)
            # Starts the new thread and the actual calculation
            CL.start()
        return

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
        # self.DrawGrid()
        self.a.ticklabel_format(style='sci', scilimits=(0, 0), axis='both')
        if self.set3dstatevar == 0:  # In 2D Mode
            self.multi = Slave(self, self.dataset)
            self.multires = self.multi.start()  # Processing the Data in octave multicore
            return
        if self.set3dstatevar == 1:  # In 3D Mode
            self.multi = Slave(self, self.dataset, mode='3d')
            self.multires = self.multi.start()  # Calling octave
            return

    def SecondHalf2d(self):
        # Plotting the Data
        self.multires = Manips.multires
        self.myplot(0, self.multires[0][0][:, 2], self.multires[0][0][:, 4], 'Horizontal distance in [m]',
                    'Vertical distance in [m]]', pttl='Trajectory')
        # Adding a line for every dataset
        for i in range(1, int(self.partnumentm.get())):
            self.a.plot(self.multires[i][0][:, 2], self.multires[i][0][:, 4])
        kill = self.picker.get_children()
        for item in kill:
            self.picker.delete(item)
        for i in range(0, int(self.partnumentm.get())):
            self.picker.insert('', 'end', values=[i, self.d3(self.dataset[i][1]),
                               self.d3(self.dataset[i][0]), self.d3(self.dataset[i][2]),
                               self.d3(self.dataset[i][3]), '/', self.d3(self.dataset[i][6]),
                               '/', self.d3(self.dataset[i][7])])
        self.scilables()
        self.Paper.show()
        return

    def SecondHalf3d(self):
        self.multires = Manips.multires
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
        kill = self.picker.get_children()
        for item in kill:
            self.picker.delete(item)
        for i in range(0, int(self.partnumentm.get())):
            self.picker.insert('', 'end', text=str(i), values=[i, self.d3(self.dataset[i][1]),
                               self.d3(self.dataset[i][0]), self.d3(self.dataset[i][2]),
                               self.d3(self.dataset[i][3]), self.d3(self.dataset[i][4]),
                               self.d3(self.dataset[i][13]), self.d3(self.dataset[i][14]),
                               self.d3(self.dataset[i][15])])
        # Update the canvas to show the plots
        self.scilables()
        self.Paper.show()
        return

    def d3(self, numin):
        decout = dc.Decimal(numin).quantize(dc.Decimal('.01'),
                                            rounding=dc.ROUND_HALF_DOWN)
        return decout

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
    #[x,nghs,nghp,ngvs,ngvp,nuhs,nuhp,nuvs,nuvp,shs,shp,svs,svp,nwhs,nwhp,nwvs,nwvp,re];
    #[0  1    2    3    4    5    6    7    8   9   10  11  12  13   14   15   16   17]
    # numerical = +4
    # stokes = +8
    # newton = +12
    # dat2=[duration,trelax,VTSN,VTSS,nusv];
    # 3D Data
    # [ngt,ngxs,ngys,ngzs,ngxp,ngyp,ngzp,re];
    #  0   1    2    3    4    5    6    7
    # [duration,trelax,VTSN,VTSS,nusv];
    #  0        1      2    3    4
    # Setting up the options in a dictionary
    # First string: Option as shown in GUI

    def redraw(self, event):
        """Forwarding """
        self.redraw2()
        return

    def redraw2(self):
        if self.set3dstatevar == 1:  # In 3D Mode
            ind = self.viewopt[self.view.get()]
            self.msgboard('View: '+self.view.get()+'\n')
            if self.currentdata == 2:  # If single particle 3D
                # Plot the corresponding data
                self.myplot(ind[1], Calculate3D.y[:, ind[2]], Calculate3D.y[:, ind[3]],
                            ind[5], ind[6],
                            zdat=Calculate3D.y[:, ind[4]], zttl=ind[7], pttl=ind[8])
                if ind[0] == 4:  # means Reynolds
                    rest1 = Calculate3D.y[:, ind[3]]
                    rest2 = []
                    rest3 = []
                    for i in range(len(Calculate3D.y[:, ind[3]])):
                        if Calculate3D.y[i, ind[3]] > 1500:  # Newton, rather
                            rest2.append(Calculate3D.y[i, ind[3]])
                        else:
                            rest2.append(nm.NaN)
                        if Calculate3D.y[i, ind[3]] > 1 and Calculate3D.y[i, ind[3]] <= 2000:  # Transistion
                            rest3.append(Calculate3D.y[i, ind[3]])
                        else:
                            rest3.append(nm.NaN)
                    # In blue, Stokes behaviour
                    # In red, transition behaviour
                    # In green, newton behaviour
                    self.myplot(0, Calculate3D.y[:, ind[2]], Calculate3D.y[:, ind[3]],
                                ind[5], ind[6], pttl='Reynolds')
                    self.a.plot(Calculate3D.y[:, ind[2]], rest2, color='g')
                    self.a.plot(Calculate3D.y[:, ind[2]], rest3, color='red')
            if self.currentdata == 4:  # If multiple particle 3D Mode
                self.myplot(ind[1], self.multires[0][0][:, ind[2]], self.multires[0][0][:, ind[3]],
                            ind[5], ind[6],
                            zdat=self.multires[0][0][:, ind[4]], zttl=ind[7],
                            pttl=ind[8])
                if ind[1] == 0:
                    for i in range(1, int(self.partnumentm.get())):
                        self.a.plot(self.multires[i][0][:, ind[2]], self.multires[i][0][:, ind[3]])
                else:
                    for i in range(1, int(self.partnumentm.get())):
                        self.a.plot(self.multires[i][0][:, ind[2]], self.multires[i][0][:, ind[3]],
                                    self.multires[i][0][:, ind[4]])
                if ind[0] == 4:  # means Reynolds
                    remax = self.multires[0][0][:, ind[3]] * 1
                    remin = self.multires[0][0][:, ind[3]] * 1
                    for i in range(len(self.multires[:])):
                        for x in range(len(self.multires[i][0][:, ind[3]])):
                            if remax[x] < self.multires[i][0][x, ind[3]]:
                                remax[x] = self.multires[i][0][x, ind[3]] * 1
                            elif remin[x] > self.multires[i][0][x, ind[3]]:
                                remin[x] = self.multires[i][0][x, ind[3]] * 1
                            else:
                                pass
                    self.myplot(ind[1], self.multires[0][0][:, ind[2]], remax,
                                'Time in [s]', 'Reynolds', pttl='Reynolds')
                    self.a.plot(self.multires[0][0][:, ind[2]], remin, color='b')
                    self.a.fill_between(self.multires[0][0][:, ind[2]], remin, remax, where=None, color='b', alpha=0.3)
        else:  # We are in 2D Mode
            try:
                self.linesin = self.lines.get()
                self.msgboard('Drawing: '+self.linesin+'\n')
                self.plotx = self.drawopt[self.linesin][0]
                self.ploty = self.drawopt[self.linesin][1]
                self.titlexax = self.drawopt[self.linesin][2]
                self.titleyax = self.drawopt[self.linesin][3]
                self.figtitle = self.linesin
                if self.ploty != 17:  # If we are not plotting Reynolds
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
                else:  # We are plotting Reynolds
                    if self.currentdata == 1:  # Single Particle in 2D
                        rest1 = Calculate.y[:, self.ploty]
                        rest2 = []
                        rest3 = []
                        for i in range(len(Calculate.y[:, self.ploty])):
                            if Calculate.y[i, self.ploty] > 2000:  # Newton, rather
                                rest2.append(Calculate.y[i, self.ploty])
                            else:
                                rest2.append(nm.NaN)
                            if Calculate.y[i, self.ploty] > 0.1 and Calculate.y[i, self.ploty] <= 2000:  # Transistion
                                rest3.append(Calculate.y[i, self.ploty])
                            else:
                                rest3.append(nm.NaN)
                        # In blue, Stokes behaviour
                        # In red, transition behaviour
                        # In green, newton behaviour
                        self.myplot(0, Calculate.y[:, self.plotx], rest1,
                                    'Time in [s]', 'Reynolds', pttl='Reynolds')
                        self.a.plot(Calculate.y[:, self.plotx], rest2, color='g')
                        self.a.plot(Calculate.y[:, self.plotx], rest3, color='red')
                    if self.currentdata == 3:  # Multiple particles in 2D
                        remax = self.multires[0][0][:, self.ploty] * 1
                        remin = self.multires[0][0][:, self.ploty] * 1
                        for i in range(len(self.multires[:])):
                            for x in range(len(self.multires[i][0][:, self.ploty])):
                                if remax[x] < self.multires[i][0][x, self.ploty]:
                                    remax[x] = self.multires[i][0][x, self.ploty] * 1
                                elif remin[x] > self.multires[i][0][x, self.ploty]:
                                    remin[x] = self.multires[i][0][x, self.ploty] * 1
                                else:
                                    pass
                        self.myplot(0, self.multires[0][0][:, self.plotx], remax,
                                    'Time in [s]', 'Reynolds', pttl='Reynolds')
                        self.a.plot(self.multires[0][0][:, self.plotx], remin, color='b')
                        self.a.fill_between(self.multires[0][0][:, self.plotx], remin, remax, where=None, color='b', alpha=0.3)
                # self.Paper.show()
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
        self.log()
        self.scilables()
        self.Paper.show()
        return

    def shownewton(self, event):
        self.shownewton2()
        return

    def shownewton2(self):
        try:
            self.linesin = self.lines.get()
            self.nwplotx = self.drawopt[self.linesin][0]
            if self.drawopt[self.linesin][1] == 17:
                print "This is Reynolds"
                return
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
            return
        return

    def showstokes(self, event):
        self.showstokes2()
        return

    def showstokes2(self):
        try:
            # Very same priciple as for shownewton2 just above, with different indices of course
            self.linesin = self.lines.get()
            self.stplotx = self.drawopt[self.linesin][0]
            if self.drawopt[self.linesin][1] == 17:
                print "This is Reynolds"
                return
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
        return

    def DrawGrid(self):
        """A grid might improve the view"""
        try:
            if self.chdrawgrid.get() == 1:
                self.a.grid(True)
            else:
                self.a.grid(False)
            #self.Paper.show()
        except AttributeError:
            print "No plot shown"
        return

    def SetAxis(self, event):
        self.SetAxis2()
        return

    def SetAxis2(self):
        """Scaling is quite important for a good data interpretation.
        So I made it very accessible in here"""
        sel = self.picker.selection()
        selnr = []
        if len(sel) != 0:
            for i in range(len(sel)):
                selnr.append(int(self.picker.set(sel[i], column='ID')))
        else:
            for i in range(int(self.partnumentm.get())):
                selnr.append(i)
        self.viewset = self.view.get()
        try:  # Reading the input
            self.x1 = float(self.xaxisscalef.get())
            self.x2 = float(self.xaxisscalet.get())
            self.y1 = float(self.yaxisscalef.get())
            self.y2 = float(self.yaxisscalet.get())
            if self.set3dstatevar == 1:
                try:
                    self.z1 = float(self.zaxisscalef.get())
                    self.z2 = float(self.zaxisscalet.get())
                except ValueError or AttributeError:
                    print "Entry in Z not valid"
                    return
            else:
                print "Z not read"
        # In 3D Mode Corner View:
            if self.set3dstatevar == 1 and self.viewopt[self.viewset][0] == 3:
                if self.currentdata == 2:  # Single Particle 3D mode
                    # Has to undergo manual clipping as the mplot3D library
                    # is not capable enough to properly display the lines
                    xdat = Calculate3D.y[:, 4]*1
                    ydat = Calculate3D.y[:, 5]*1
                    zdat = Calculate3D.y[:, 6]*1
                if self.currentdata == 4:  # Multiple Particle 3D
                    # Has to undergo manual clipping as the mplot3D library
                    # Is not capable enough to properly display the lines
                    xdat = self.multires[0][0][:, 4]*1
                    ydat = self.multires[0][0][:, 5]*1
                    zdat = self.multires[0][0][:, 6]*1
                xdat, ydat, zdat = self.intersect(xdat, xdat, ydat, zdat,
                                                  self.x1, 0)
                xdat, ydat, zdat = self.intersect(xdat, xdat, ydat, zdat,
                                                  self.x2, 0)
                xdat, ydat, zdat = self.intersect(ydat, xdat, ydat, zdat,
                                                  self.y1, 1)
                xdat, ydat, zdat = self.intersect(ydat, xdat, ydat, zdat,
                                                  self.y2, 1)
                xdat, ydat, zdat = self.intersect(zdat, xdat, ydat, zdat,
                                                  self.z1, 2)
                xdat, ydat, zdat = self.intersect(zdat, xdat, ydat, zdat,
                                                  self.z2, 2)
                xclip, yclip, zclip =\
                    self.manclip(xdat, ydat, zdat,
                                 (self.x1, self.x2),
                                 (self.y1, self.y2),
                                 (self.z1, self.z2))
                # plotting processed data
                self.myplot(1, xclip, yclip, 'XDistance in [m]',
                            'YDistance in [m]', zttl='ZHeight in [m]',
                            zdat=zclip, pttl='Trajectory')
                if self.currentdata == 4:  # Multiple Particle 3D
                    # Has to undergo manual clipping as the mplot3D library
                    # Is not capable enough to properly display the lines
                    # plotting all other lines of the dataset
                        if selnr[0] != 0:
                            firstline = self.firstplot.pop(0)
                            firstline.remove()
                            del firstline
                        for i in selnr:
                            xdat = self.multires[i][0][:, 4]*1
                            ydat = self.multires[i][0][:, 5]*1
                            zdat = self.multires[i][0][:, 6]*1
                            xdat, ydat, zdat = self.intersect(xdat, xdat, ydat, zdat,
                                                              self.x1, 0)
                            xdat, ydat, zdat = self.intersect(xdat, xdat, ydat, zdat,
                                                              self.x2, 0)
                            xdat, ydat, zdat = self.intersect(ydat, xdat, ydat, zdat,
                                                              self.y1, 1)
                            xdat, ydat, zdat = self.intersect(ydat, xdat, ydat, zdat,
                                                              self.y2, 1)
                            xdat, ydat, zdat = self.intersect(zdat, xdat, ydat, zdat,
                                                              self.z1, 2)
                            xdat, ydat, zdat = self.intersect(zdat, xdat, ydat, zdat,
                                                              self.z2, 2)
                            xclip, yclip, zclip =\
                                self.manclip(xdat, ydat, zdat,
                                             (self.x1, self.x2),
                                             (self.y1, self.y2),
                                             (self.z1, self.z2))
                            self.a.plot(xclip, yclip, zclip)
                    # Finally, set the scale
                self.a.set_zlim(self.z1, self.z2)
                self.a.set_xlim(self.x1, self.x2)
                self.a.set_ylim(self.y1, self.y2)
            elif self.set3dstatevar == 1 and self.viewopt[self.viewset][0] != 3:
                print "3D Mode, but 2D view"
                if self.currentdata == 2:  # Single Particle 3D mode
                    print "We have one particle in 3D"
                    # Has to undergo manual clipping as the mplot3D library
                    # is not capable enough to properly display the lines
                    xdat = Calculate3D.y[:, 4]*1
                    ydat = Calculate3D.y[:, 5]*1
                    zdat = Calculate3D.y[:, 6]*1
                    xdat, ydat, zdat = self.intersect(xdat, xdat, ydat, zdat,
                                                      self.x1, 0)
                    xdat, ydat, zdat = self.intersect(xdat, xdat, ydat, zdat,
                                                      self.x2, 0)
                    xdat, ydat, zdat = self.intersect(ydat, xdat, ydat, zdat,
                                                      self.y1, 1)
                    xdat, ydat, zdat = self.intersect(ydat, xdat, ydat, zdat,
                                                      self.y2, 1)
                    xdat, ydat, zdat = self.intersect(zdat, xdat, ydat, zdat,
                                                      self.z1, 2)
                    xdat, ydat, zdat = self.intersect(zdat, xdat, ydat, zdat,
                                                      self.z2, 2)
                    xclip, yclip, zclip =\
                        self.manclip(xdat, ydat, zdat,
                                     (self.x1, self.x2),
                                     (self.y1, self.y2),
                                     (self.z1, self.z2))
                    # Plot the corresponding data
                    if self.viewopt[self.viewset][0] == 1:  # means X View
                        self.myplot(0, xclip, zclip,
                                    'X Distance in [m]', 'Z Distance in [m]',
                                    pttl='X-Z Trajectory Projection')
                        self.a.set_xlim(self.x1, self.x2)
                        self.a.set_ylim(self.z1, self.z2)
                    elif self.viewopt[self.viewset][0] == 2:  # means Y View
                        self.myplot(0, yclip, zclip,
                                    'Y Distance in [m]', 'Z Distance in [m]',
                                    pttl='Y-Z Trajectory Projection')
                        self.a.set_xlim(self.y1, self.y2)
                        self.a.set_ylim(self.z1, self.z2)
                    elif self.viewopt[self.viewset][0] == 0:  # means Topview
                        self.myplot(0, xclip, yclip,
                                    'X Distance in [m]', 'Y Distance in [m]',
                                    pttl='X-Y Trajectory Projection')
                        self.a.set_xlim(self.x1, self.x2)
                        self.a.set_ylim(self.y1, self.y2)
                    else:  # means Reynolds or some Speed view
                        self.a.set_xlim(self.x1, self.x2)
                        self.a.set_ylim(self.y1, self.y2)
                if self.currentdata == 4:  # If multiple particle 3D Mode
                    print "We are having a few particles in 3D"
                    xclipm = []
                    yclipm = []
                    zclipm = []
                    for i in selnr:
                        xdat = self.multires[i][0][:, 4]
                        ydat = self.multires[i][0][:, 5]
                        zdat = self.multires[i][0][:, 6]
                        xdat, ydat, zdat = self.intersect(xdat, xdat, ydat, zdat,
                                                          self.x1, 0)
                        xdat, ydat, zdat = self.intersect(xdat, xdat, ydat, zdat,
                                                          self.x2, 0)
                        xdat, ydat, zdat = self.intersect(ydat, xdat, ydat, zdat,
                                                          self.y1, 1)
                        xdat, ydat, zdat = self.intersect(ydat, xdat, ydat, zdat,
                                                          self.y2, 1)
                        xdat, ydat, zdat = self.intersect(zdat, xdat, ydat, zdat,
                                                          self.z1, 2)
                        xdat, ydat, zdat = self.intersect(zdat, xdat, ydat, zdat,
                                                          self.z2, 2)
                        xclip, yclip, zclip =\
                            self.manclip(xdat, ydat, zdat,
                                         (self.x1, self.x2),
                                         (self.y1, self.y2),
                                         (self.z1, self.z2))
                        xclipm.append(xclip)
                        yclipm.append(yclip)
                        zclipm.append(zclip)
                    if self.viewopt[self.viewset][0] == 1:  # means X View
                        self.myplot(0, xclipm[0], zclipm[0],
                                    'X Distance in [m]', 'Z Distance in [m]',
                                    pttl='X-Z Trajectory Projection')
                        for i in range(len(selnr)):
                            self.a.plot(xclipm[i], zclipm[i])
                        self.a.set_xlim(self.x1, self.x2)
                        self.a.set_ylim(self.z1, self.z2)
                    elif self.viewopt[self.viewset][0] == 2:  # means Y View
                        self.myplot(0, yclipm[0], zclipm[0],
                                    'Y Distance in [m]', 'Z Distance in [m]',
                                    pttl='Y-Z Trajectory Projection')
                        for i in range(len(selnr)):
                            self.a.plot(yclipm[i], zclipm[i])
                        self.a.set_xlim(self.y1, self.y2)
                        self.a.set_ylim(self.z1, self.z2)
                    elif self.viewopt[self.viewset][0] == 0:  # means Topview
                        self.myplot(0, xclipm[0], yclipm[0],
                                    'X Distance in [m]', 'Y Distance in [m]',
                                    pttl='X-Y Trajectory Projection')
                        for i in range(len(selnr)):
                            self.a.plot(xclipm[i], yclipm[i])
                        self.a.set_xlim(self.x1, self.x2)
                        self.a.set_ylim(self.y1, self.y2)
                    elif self.viewopt[self.viewset][0] == 4:  # means Reynolds
                        print nm.size(range(len(selnr)))
                        if nm.size(range(len(selnr))) == 1:  # Only one particle is selected in the picker
                            rest1 = self.multires[selnr[0]][0][:, 7]
                            rest2 = []
                            rest3 = []
                            for i in range(len(self.multires[selnr[0]][0][:, 7])):
                                if self.multires[selnr[0]][0][i, 7] > 1500:  # Newton, rather
                                    rest2.append(self.multires[selnr[0]][0][i, 7])
                                else:
                                    rest2.append(nm.NaN)
                                if self.multires[selnr[0]][0][i, 7] > 1 and self.multires[selnr[0]][0][i, 7] <= 2000:  # Transistion
                                    rest3.append(self.multires[selnr[0]][0][i, 7])
                                else:
                                    rest3.append(nm.NaN)
                            # In blue, Stokes behaviour
                            # In red, transition behaviour
                            # In green, newton behaviour
                            self.myplot(0, self.multires[selnr[0]][0][:, 0], rest1,
                                        'Time in [s]', 'Reynolds', pttl='Reynolds')
                            self.a.plot(self.multires[selnr[0]][0][:, 0], rest2, color='g')
                            self.a.plot(self.multires[selnr[0]][0][:, 0], rest3, color='red')
                        else:  # More than one particle are selected in the picker
                            remax = self.multires[selnr[0]][0][:, 7] * 1
                            remin = self.multires[selnr[0]][0][:, 7] * 1
                            for i in selnr:
                                for x in range(len(self.multires[i][0][:, 7])):
                                    if remax[x] < self.multires[i][0][x, 7]:
                                        remax[x] = self.multires[i][0][x, 7] * 1
                                    elif remin[x] > self.multires[i][0][x, 7]:
                                        remin[x] = self.multires[i][0][x, 7] * 1
                                    else:
                                        pass
                            self.myplot(0, self.multires[0][0][:, 0], remax,
                                        'Time in [s]', 'Reynolds', pttl='Reynolds')
                            self.a.plot(self.multires[0][0][:, 0], remin, color='b')
                            self.a.fill_between(self.multires[0][0][:, 0], remin, remax, where=None, color='black', alpha=0.2)
                        self.a.set_xlim(self.x1, self.x2)
                        self.a.set_ylim(self.y1, self.y2)
                    else:  # Some Speed-View
                        if nm.size(range(len(selnr))) == 1:  # Only one particle is selected in the picker
                            self.myplot(0, self.multires[selnr[0]][0][:, 0],
                                        self.multires[selnr[0]][0][:, self.viewopt[self.viewset][3]],
                                        self.viewopt[self.viewset][5],
                                        self.viewopt[self.viewset][6],
                                        pttl=self.viewopt[self.viewset][8])
                        else:  # more than one particle is selected
                            self.myplot(0, self.multires[selnr[0]][0][:, 0],
                                        self.multires[selnr[0]][0][:, self.viewopt[self.viewset][3]],
                                        self.viewopt[self.viewset][5],
                                        self.viewopt[self.viewset][6],
                                        pttl=self.viewopt[self.viewset][8])
                            for i in selnr:
                                self.a.plot(self.multires[i][0][:, 0],
                                            self.multires[i][0][:, self.viewopt[self.viewset][3]])
                        self.a.set_xlim(self.x1, self.x2)
                        self.a.set_ylim(self.y1, self.y2)
                        # print "People ask for Reynolds!"
            elif self.currentdata == 3:  # Not 3D Mode and no corner view, but maybe 2D multi
                sel = self.picker.selection()
                selnr = []
                if len(sel) != 0:
                    for i in range(len(sel)):
                        selnr.append(int(self.picker.set(sel[i], column='ID')))
                else:
                    for i in range(int(self.partnumentm.get())):
                        selnr.append(i)
                self.linesin = self.lines.get()
                self.msgboard('Drawing: '+self.linesin+'\n')
                self.plotx = self.drawopt[self.linesin][0]
                self.ploty = self.drawopt[self.linesin][1]
                self.titlexax = self.drawopt[self.linesin][2]
                self.titleyax = self.drawopt[self.linesin][3]
                self.figtitle = self.linesin
                if self.ploty != 17:  # If we are not plotting Reynolds
                    self.myplot(0, self.multires[0][0][:, self.plotx],
                                self.multires[0][0][:, self.ploty],
                                self.titlexax, self.titleyax,
                                pttl=self.figtitle)
                    if selnr[0] != 0:
                        firstline = self.firstplot.pop(0)
                        firstline.remove()
                        del firstline
                    for i in selnr:
                        self.a.plot(self.multires[i][0][:, self.plotx],
                                    self.multires[i][0][:, self.ploty])
                else:  # We are plotting Reynolds
                    if len(selnr) == 1:  # Single line in 2D
                        rest1 = self.multires[selnr[0]][0][:, self.ploty]
                        rest2 = []
                        rest3 = []
                        for i in range(len(self.multires[selnr[0]][0][:, self.ploty])):
                            if self.multires[selnr[0]][0][i, self.ploty] > 2000:  # Newton, rather
                                rest2.append(self.multires[selnr[0]][0][i, self.ploty])
                            else:
                                rest2.append(nm.NaN)
                            if (self.multires[selnr[0]][0][i, self.ploty] > 0.1 and
                               self.multires[selnr[0]][0][i, self.ploty] <= 2000):  # Transistion
                                rest3.append(self.multires[selnr[0]][0][i, self.ploty])
                            else:
                                rest3.append(nm.NaN)
                        # In blue, Stokes behaviour
                        # In red, transition behaviour
                        # In green, newton behaviour
                        self.myplot(0, self.multires[selnr[0]][0][:, self.plotx], rest1,
                                    'Time in [s]', 'Reynolds', pttl='Reynolds')
                        self.a.plot(self.multires[selnr[0]][0][:, self.plotx], rest2, color='g')
                        self.a.plot(self.multires[selnr[0]][0][:, self.plotx], rest3, color='red')
                    else:  # Multiple particles in 2D
                        remax = self.multires[selnr[0]][0][:, self.ploty] * 1
                        remin = self.multires[selnr[0]][0][:, self.ploty] * 1
                        for i in selnr:
                            for x in range(len(self.multires[i][0][:, self.ploty])):
                                if remax[x] < self.multires[i][0][x, self.ploty]:
                                    remax[x] = self.multires[i][0][x, self.ploty] * 1
                                elif remin[x] > self.multires[i][0][x, self.ploty]:
                                    remin[x] = self.multires[i][0][x, self.ploty] * 1
                                else:
                                    pass
                        self.myplot(0, self.multires[0][0][:, self.plotx], remax,
                                    'Time in [s]', 'Reynolds', pttl='Reynolds')
                        self.a.plot(self.multires[0][0][:, self.plotx], remin, color='b')
                        self.a.fill_between(self.multires[0][0][:, self.plotx],
                                            remin, remax, where=None, color='b', alpha=0.3)
                self.a.set_xlim(self.x1, self.x2)
                self.a.set_ylim(self.y1, self.y2)
            else:
                print "something else"
                self.a.set_xlim(self.x1, self.x2)
                self.a.set_ylim(self.y1, self.y2)
            self.log()
            self.scilables()
            self.Paper.show()
        except ValueError:
            # If the values can't be converted to a float
            print "Something is wrong with the axis fields"
        print "Set axis"
        return

    def validate(self, action, index, value_if_allowed, prior_value, text,
                 validation_type, trigger_type, widget_name):
        # A little help for some value fields. Only allow certain charakters
        print text
        if text in 'e0123456789.-+':
            return True
        else:
            try:  # The insert method of the entry boxes needs this version
                float(text)
                return True
            except ValueError:
                # Bad input
                return False
        return

    def myplot(self, persp3D, xdat, ydat, xttl, yttl,
               zdat=nm.NaN, zttl=nm.NaN, pttl=''):
        """Plotting can be quite complicated, so I shortened my code by
        creating these routines for the most common cases"""
        self.f.clf()
        if persp3D == 1:
            self.a = self.f.add_subplot(111, projection='3d')
            self.f.subplots_adjust(bottom=0.05, left=0.05,
                                   right=0.95, top=0.95)
            self.firstplot = self.a.plot(xdat, ydat, zdat)
            self.a.set_xlabel(xttl, fontsize=10)
            self.a.set_ylabel(yttl, fontsize=10)
            self.a.set_title(pttl, fontsize=10)
            self.a.tick_params(axis='both', labelsize=10)
            self.DrawGrid()
            #self.a.ticklabel_format(style='sci', scilimits=(0, 0), axis='both')
            self.scilables()
            self.a.set_zlabel(zttl, fontsize=10)
            self.a.mouse_init()
        else:
            self.a = self.f.add_subplot(111)
            self.f.subplots_adjust(bottom=0.11, left=0.11,
                                   right=0.92, top=0.92)
            self.firstplot = self.a.plot(xdat, ydat)
            self.a.set_xlabel(xttl, fontsize=10)
            self.a.set_ylabel(yttl, fontsize=10)
            self.a.set_title(pttl, fontsize=10)
            self.a.tick_params(axis='both', labelsize=10)
            self.DrawGrid()
            self.scilables()
            #self.a.ticklabel_format(style='sci', scilimits=(0, 0), axis='both')
        return

    # def logy(self, event):
    #     self.logy2()

    def scilables(self):
        self.a.ticklabel_format(style='sci', scilimits=(0, 0), axis='both')

    def log(self):
        if self.chlogxvar.get() == 1:  # If the checkmark is set
            self.a.set_xscale('log')
        else:
            self.a.set_xscale('linear')
        if self.chlogyvar.get() == 1:  # If the checkmark is set
            self.a.set_yscale('log')
        else:
            self.a.set_yscale('linear')
        self.Paper.show()
        return

    # This function is not used yet, might become usefull later
    def myplot_add(self, persp3D, xdat, ydat, zdat=nm.NaN):
        if persp3D == 1:
            self.a.plot(xdat, ydat, zdat)
            self.a.mouse_init()
        else:
            self.a.plot(xdat, ydat, color='red')
        # self.DrawGrid()
        return

    # Manual clipping for the screwed up view in mplot3D
    def manclip(self, xdat, ydat, zdat, xlim, ylim, zlim):
        # Clipping manually
        # Find intersections
        xdatre = 1*xdat
        ydatre = 1*ydat
        zdatre = 1*zdat

        for i in nm.arange(len(xdat)):
            if xdat[i] < xlim[0]:
                xdatre[i], ydatre[i], zdatre[i] = [nm.NaN, nm.NaN, nm.NaN]
            if xdat[i] > xlim[1]:
                xdatre[i], ydatre[i], zdatre[i] = [nm.NaN, nm.NaN, nm.NaN]
            else:
                pass
        for i in nm.arange(len(ydat)):
            if ydat[i] < ylim[0]:
                xdatre[i], ydatre[i], zdatre[i] = [nm.NaN, nm.NaN, nm.NaN]
            if ydat[i] > ylim[1]:
                xdatre[i], ydatre[i], zdatre[i] = [nm.NaN, nm.NaN, nm.NaN]
            else:
                pass
        for i in nm.arange(len(zdat)):
            if zdat[i] < zlim[0]:
                xdatre[i], ydatre[i], zdatre[i] = [nm.NaN, nm.NaN, nm.NaN]
            if zdat[i] > zlim[1]:
                xdatre[i], ydatre[i], zdatre[i] = [nm.NaN, nm.NaN, nm.NaN]
            else:
                pass
        return xdatre, ydatre, zdatre

    # Manual clipping for the screwed up view in mplot3D
    def intersect(self, adat, xdat, ydat, zdat, alim, axis):
        # Clipping manually
        # Find intersection in a range
        # Pull down intersection points to lower limit, so zero crossing occurs
        asec = adat - alim
        # Signum for positiv-negative. Diff for signchange (0 non, 2 or -2 for change)
        # Where gives back the indices where an array is 0 (default)
        zero_crossings = nm.where(nm.diff(self.sign(asec)))[0]
        # Transfer to points
        # Read out corresponding points and store in sects
        for i in nm.arange(len(zero_crossings)-1, -1, -1):
            a = [xdat[zero_crossings[i]], ydat[zero_crossings[i]], zdat[zero_crossings[i]]]
            b = [xdat[zero_crossings[i]+1], ydat[zero_crossings[i]+1], zdat[zero_crossings[i]+1]]
            vect = nm.subtract(a, b)
            x = (alim-a[axis])/vect[axis]
            np = (a + x*vect)
            # if axis == 0:
            #     self.a.scatter(np[0], np[1], np[2], marker='o', color='r')
            # if axis == 1:
            #     self.a.scatter(np[0], np[1], np[2], marker='o', color='g')
            # if axis == 2:
            #     self.a.scatter(np[0], np[1], np[2], marker='o', color='m')
            xdat = nm.insert(xdat, (zero_crossings[i]+1), np[0])
            ydat = nm.insert(ydat, (zero_crossings[i]+1), np[1])
            zdat = nm.insert(zdat, (zero_crossings[i]+1), np[2])
        return xdat, ydat, zdat

    def sectvect(self, asects0, asects1, alim, axis):
        Asects = []
        for i in range(0, len(asects0), 2):
            a = [asects0[i][0], asects0[i][1], asects0[i][2]]
            b = [asects0[i+1][0], asects0[i+1][1], asects0[i+1][2]]
            vect = nm.subtract(a, b)
            x = (alim[0]-a[axis])/vect[axis]
            Asects.append(a + x*vect)
        for i in range(0, len(asects1), 2):
            a = [asects1[i][0], asects1[i][1], asects1[i][2]]
            b = [asects1[i+1][0], asects1[i+1][1], asects1[i+1][2]]
            vect = nm.subtract(a, b)
            x = (alim[1]-a[axis])/vect[axis]
            Asects.append(a + x*vect)
        return Asects

    def sign(self, val):
        for i in range(len(val)):
            if val[i] < 0:
                val[i] = -1
            else:
                val[i] = 1
        return val

    def pickclick(self, event):
        # sel = self.picker.selection()
        # for i in range(len(sel)):
        #     print self.picker.set(sel[i], column='Nr')
        self.SetAxis2()
        return

    def TreeSort(self, who, reverse):
        l = [(float(self.picker.set(k, who)), k) for k in self.picker.get_children()]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            self.picker.move(k, '', index)

        # reverse sort next time
        self.picker.heading(who, command=lambda: self.TreeSort(who, not reverse))


def calc_m3d(arg, **kwarg):
    return CalculateM.calculate_m3d(*arg, **kwarg)


def calc_m(arg, **kwarg):
    return CalculateM.calculate_m(*arg, **kwarg)


class Slave(threading.Thread):
    def __init__(self, guest, data, mode='2d'):
        self.data = data
        self.mode = mode
        self.guest = guest
        threading.Thread.__init__(self)

    def run(self):
        Esel = CalculateM()
        Luggage = Esel.run(self.guest, self.data, self.mode)
        return Luggage


class CalculateM(object):

    def run(self, guest, data, mode='2d'):
        begin = time.time()
        # Counting the number of available CPUs in System
        pool_size = multiprocessing.cpu_count()
        # Creating a pool of processes with the maximal number of CPUs possible
        pool = multiprocessing.Pool(processes=pool_size)
        # Call the corresponding function depending on 2D or 3D mode
        if mode == '3d':
            Manips.multires = pool.map_async(calc_m3d, zip([self]*len(data), data)).get()
        else:
            Manips.multires = pool.map_async(calc_m, zip([self]*len(data), data)).get()
        # Properly close and end all processes, once we're done
        pool.close()
        pool.join()
        end = time.time()
        if mode == '3d':
            guest.SecondHalf3d()
        else:
            guest.SecondHalf2d()
        print (end - begin)
        return

    # Function to be called for multiple particles in 2D mode
    # Receives all parameters needed in a list: indata
    def calculate_m(self, indata):
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
    def calculate_m3d(self, indata):
        # This might print oddly as there are no locks used
        print 'Reading values and calling Octave'
        [Calculate.y, Calculate.y2] = \
            oc.call('Wurf3D.m', [indata],
                    verbose=False)  # Use octave for debugging, keep on false
        print 'Done! Data from Octave available'
        return [Calculate.y, Calculate.y2]
