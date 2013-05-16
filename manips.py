# -*- coding: utf-8 -*-
# manips.py
"""Graphical User Interface for plotting the results
calculated in the script: Wurfp3.m and Wurf3D.m in Octave -
Simulation of particle flight - GIT"""

import time
import numpy as nm
import random
from oct2py import octave as oc
from mpl_toolkits.mplot3d import axes3d
import Tkinter as tki
import multiprocessing
from pfCalculates import *


def multipcalc(data, mode='2d'):
    pool_size = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=pool_size)
    if mode == '3d':
        results = pool.map_async(calculate_m3d, data).get()
    else:
        results = pool.map_async(calculate_m, data).get()
    # print results
    # print "Pool is over"
    return results


def calculate_m(indata):
    print 'Reading values and calling Octave'
    [CalculateN.y, CalculateN.y2] = \
        oc.call('Wurfp3m.m', [indata],
                verbose=False)
    print 'Done! Data from Octave available'
    return [CalculateN.y, CalculateN.y2]


def calculate_m3d(indata):
    print 'Reading values and calling Octave'
    [CalculateN.y, CalculateN.y2] = \
        oc.call('Wurf3D.m', [indata],
                verbose=False)
    print 'Done! Data from Octave available'
    return [CalculateN.y, CalculateN.y2]


class Manips(object):
    """docstring for Manips"""
    def __init__(self, guest):
        self.guest = guest
        self.currentdata = 0  
        # [0=No Data; 1=2D single, 2=3D single, 3=2D multi, 4=3D multi]
        pass

    def set3dstate(self):
        if self.set3dstatevar == 1:
        # Turn 3D off
            self.set3dstatevar = 0
            self.set3DButton.configure(text="3D mode is off",
                                       bg='grey', relief='raised')
            self.zaxisscalef.state(['disabled'])
            self.zaxisscalet.state(['disabled'])
            self.checknewton.state(['!disabled'])
            self.checkstokes.state(['!disabled'])
            self.drawselectmview.grid_forget()
            self.drawselectm.grid(row=0, column=0, columnspan=2, sticky="NSWE")
            self.parameters.add(self.para2D)
            self.parameters.hide(self.para3D)
        else:
        # Turn 3D on
            self.set3dstatevar = 1
            self.set3DButton.configure(text="3D mode is on",
                                       bg='green', relief='sunken')
            self.zaxisscalef.state(['!disabled'])
            self.zaxisscalet.state(['!disabled'])
            self.checknewton.state(['disabled'])
            self.checkstokes.state(['disabled'])
            self.drawselectmview.grid(row=0, column=0,
                                      columnspan=2, sticky="NSWE")
            self.drawselectm.grid_forget()
            self.parameters.add(self.para3D)
            self.parameters.hide(self.para2D)

    def ClickClose(self, event):
        """Calls ClickClose2. The event type will be ignored"""
        self.ClickClose2()

    def ClickClose2(self):
        """Closes the application"""
        self.ThisParent.quit()
        self.ThisParent.destroy()

    def Reset(self, event):
        """Forwards the binding without event information"""
        self.Reset2()

    def Reset2(self):
        """This has no use"""
        print "Not assigned yet"
        self.info.config(state=tki.NORMAL)
        self.info.insert(tki.END, "Not assigned yet \n")
        self.info.yview(tki.END)
        self.info.config(state=tki.DISABLED)

    def RunThiss(self, event):
        """Triggers Runthis2, event type will be ignored"""
        self.RunThis2s()

    def RunThis2s(self):
        """Reads entries, prints status messages and calls
        the Calculate function in order to do some work"""
        # Read the given values for the variables.
        try:
            self.e1 = float(self.rhopent.get())
            self.e2 = float(self.dpent.get())
            self.e3 = float(self.velent.get())
            if self.set3dstatevar == 0:
                self.currentdata = 1
                self.e4 = float(self.angleeent.get())
                self.e5 = float(self.precent2d.get())
                self.e6 = float(self.durationent2d.get())
                self.e7 = float(self.windxent2d.get())
                self.e8 = float(self.windyent2d.get())

                # Inform user about the configuration.
                self.entries = "Density: %.2f kg/m³ \n"\
                               "Particle size: %.2f µm\n" \
                               "Velocity: %.2f m/s \nElevation: %.2f°\n"\
                               "Precision set to %s \nDuration set to %s\n"\
                               "Horizontal Wind: %.2f m/s\n"\
                               "Vertical Wind: %.2f m/s\n"\
                               "Calculations running, please wait ... \n" \
                               % (self.e1, self.e2, self.e3, self.e4, self.e5,
                                  self.e6, self.e7, self.e8)
            else:
                self.currentdata = 2
                self.e4 = float(self.angleeent.get())
                self.e5 = float(self.angleaent.get())
                self.e6 = float(self.precent3d.get())
                self.e7 = float(self.durationent3d.get())
                self.e8 = float(self.windxent3d.get())
                self.e9 = float(self.windyent3d.get())
                self.e10 = float(self.windzent3d.get())

                # Inform user about the configuration.
                self.entries = "Density: %.2f kg/m³ \n"\
                               "Particle size: %.2f µm\n" \
                               "Velocity: %.2f m/s \n"\
                               "Elevation: %.2f°\nAzimuth: %.2f°\n"\
                               "Precision set to %s \nDuration set to %s\n"\
                               "Wind in X: %.2f m/s\nWind in Y : %.2f m/s\n"\
                               "Wind in Z: %.2f m/s\n"\
                               "Calculations running, please wait ... \n" \
                               % (self.e1, self.e2, self.e3, self.e4, self.e5,
                                  self.e6, self.e7, self.e8, self.e9, self.e10)

        except ValueError:
            self.message = "No valid values entered\n"
            self.info.config(state=tki.NORMAL)
            self.info.insert(tki.END, self.message)
            # Scroll to end of window.
            self.info.yview(tki.END)
            self.info.config(state=tki.DISABLED)
            return

        self.info.config(state=tki.NORMAL)
        self.info.insert(tki.END, self.entries)
        # Scroll to end of window.
        self.info.yview(tki.END)
        self.info.config(state=tki.DISABLED)
        print 'RunThis2s called'  # Shows in prompt, not in GUI
        # Call Calculate, invokes a new thread in order to keep the
        # GUI alive while calculating
        if self.set3dstatevar == 0:
            CL = Calculate(self, self.e1, self.e2,
                           self.e3, self.e4, self.e5, self.e6,
                           self.e7, self.e8)
            # Starts the new thread and the actual calculation
            CL.start()
        else:
            CL = Calculate3D(self, self.e1, self.e2,
                             self.e3, self.e4, self.e5, self.e6,
                             self.e7, self.e8, self.e9, self.e10)
            # Starts the new thread and the actual calculation
            CL.start()

    def RunThis2m(self):
        """Reads entries, prints status messages and calls
        the Calculate function in order to do some work"""
        # Read the given values for the variables.
        try:
            self.e1r = tuple(map(float, self.rhopentm.get().split('-')))
            self.e1 = \
                self.ingen(self.multpartslcrhop.get(), self.e1r)
            self.e2r = tuple(map(float, self.dpentm.get().split('-')))
            self.e2 = \
                self.ingen(self.multpartslcdp.get(), self.e2r)
            self.e3r = tuple(map(float, self.velentm.get().split('-')))
            self.e3 = \
                self.ingen(self.multpartslcvel.get(), self.e3r)
            self.e4r = tuple(map(float, self.angleeentm.get().split('-')))
            self.e4 = \
                self.ingen(self.multpartslcanglee.get(), self.e4r)
            if self.set3dstatevar == 0:
                self.currentdata = 3
                self.e5 = float(self.precent2d.get())
                self.e6 = float(self.durationent2d.get())
                self.e7 = float(self.windxent2d.get())
                self.e8 = float(self.windyent2d.get())
                # Inform user about the configuration.
                self.entries = "Density: %.2f to %.2f kg/m³ \n"\
                               "Particle size: %.2f to %.2f µm\n" \
                               "Velocity: %.2f to %.2f m/s \n"\
                               "Elevation: %.2f to %.2f°\n"\
                               "Precision set to %s \nDuration set to %s\n"\
                               "Horizontal Wind: %.2f m/s\n"\
                               "Vertical Wind: %.2f m/s\n"\
                               "Calculations running, please wait ... \n" \
                               % (self.e1r[0], self.e1r[1], self.e2r[0],
                                  self.e2r[1], self.e3r[0], self.e3r[1],
                                  self.e4r[0], self.e4r[1], self.e5,
                                  self.e6, self.e7, self.e8)
            else:
                self.currentdata = 4
                self.e5r = tuple(map(float, self.angleaentm.get().split('-')))
                self.e5 = \
                    self.ingen(self.multpartslcanglea.get(), self.e5r)
                self.e6 = float(self.precent3d.get())
                self.e7 = float(self.durationent3d.get())
                self.e8 = float(self.windxent3d.get())
                self.e9 = float(self.windyent3d.get())
                self.e10 = float(self.windzent3d.get())
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
                               % (self.e1r[0], self.e1r[1], self.e2r[0],
                                  self.e2r[1], self.e3r[0], self.e3r[1],
                                  self.e4r[0], self.e4r[1], self.e5r[0],
                                  self.e5r[1], self.e6, self.e7,
                                  self.e8, self.e9, self.e10)

        except ValueError:
            self.message = "No valid values entered\n"
            self.info.config(state=tki.NORMAL)
            self.info.insert(tki.END, self.message)
            # Scroll to end of window.
            self.info.yview(tki.END)
            self.info.config(state=tki.DISABLED)
            return

        self.info.config(state=tki.NORMAL)
        self.info.insert(tki.END, self.entries)
        # Scroll to end of window.
        self.info.yview(tki.END)
        self.info.config(state=tki.DISABLED)
        print 'RunThis2m called'
        # Call Calculate, invokes a new thread in order to keep the
        # GUI alive while calculating
        if self.set3dstatevar == 0:
            n = int(self.partnumentm.get())
            self.dataset = []
            for x in range(0, n):
                print x
                self.dataset.append((self.e1[x], self.e2[x], self.e3[x],
                                    self.e4[x], self.e5, self.e6,
                                    self.e7, self.e8))
        else:
            n = int(self.partnumentm.get())
            self.dataset = []
            for x in range(0, n):
                print x
                self.dataset.append((self.e1[x], self.e2[x], self.e3[x],
                                    self.e4[x], self.e5[x], self.e6,
                                    self.e7, self.e8, self.e9, self.e10))
        # These datasets need to be sent to Octave individually
        self.f.clf()
        if self.set3dstatevar == 1:
            self.a = self.f.add_subplot(111, projection='3d')
            self.f.subplots_adjust(bottom=0.05, left=0.05,
                                   right=0.95, top=0.95)
        else:
            self.a = self.f.add_subplot(111)
            self.f.subplots_adjust(bottom=0.11, left=0.11,
                                   right=0.92, top=0.92)
        self.DrawGrid()
        self.a.ticklabel_format(style='sci', scilimits=(0, 0), axis='both')
        if self.set3dstatevar == 0:
            self.multires = multipcalc(self.dataset)
            # print nm.size(self.multires)
            # print nm.shape(self.multires)
            # print self.multires[0][:,0]
            # print self.multires[0][:,1]
            self.myplot(0, self.multires[0][0][:, 2], self.multires[0][0][:, 4], 'Time in [s]',
                        'Speed in [m/s]', pttl='Speed-Time-Horizontal')
            for i in range(1, int(self.partnumentm.get())):
                self.a.plot(self.multires[i][0][:, 2], self.multires[i][0][:, 4])

        if self.set3dstatevar == 1:
            self.multires = multipcalc(self.dataset, mode='3d')
            # print nm.size(self.multires)
            # print nm.shape(self.multires)
            # print self.multires[0][:,0]
            # print self.multires[0][:,1]
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

        self.Paper.show()
        # self.octdata = self.calculate_m(self, self.dataset[0])
        # print self.octdata
        # print __name__
        # print self.dataset
        # pool_size = multiprocessing.cpu_count()
        # print pool_size
        # pool = multiprocessing.Pool(processes=pool_size)
        # results = pool.map_async(calculate_m, self.dataset).get()
        # print results
        # print "Pool is over"

    def ingen(self, gen_mode, valin):
        n = int(self.partnumentm.get())
        # print n
        valout = []
        if gen_mode == 'Set':
            valout = list(valin)
            print valout
            return valout
        elif gen_mode == 'Range':
            steps = (valin[1]-valin[0])/(n-1)
            valout = [valin[0]]
            for x in range(1, n):
                valout.append(valin[0]+steps*x)
            print valout
            return valout
        elif gen_mode == 'Random':
            print 'Randoming'
            print n
            for i in range(1, n+1):
                print "Creating values "
                print i
                valout.append(random.uniform(valin[0], valin[1]))
            # valout.sort()
            print valout
            return valout
        else:
            print "No, nothing happened"
        return

    def redraw(self, event):
        """Forwarding """
        self.redraw2()

    def redraw2(self):
        if self.set3dstatevar == 1:
            self.viewin = self.view.get()
            self.info.config(state=tki.NORMAL)
            self.viewid = str(self.viewopt[self.viewin])
            self.info.insert(tki.END, 'View: '+self.viewin+'\n')
            self.info.yview(tki.END)
            self.info.config(state=tki.DISABLED)
            # self.a.elev = self.viewopt[self.viewin][0]
            # self.a.azim = self.viewopt[self.viewin][1]
            if self.currentdata == 2:
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
            if self.currentdata == 4:
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

        else:
            try:
                # self.present = Calculate.y
                self.linesin = self.lines.get()
                self.info.config(state=tki.NORMAL)
                self.drawid = str(self.drawopt[self.linesin])
                self.info.insert(tki.END, 'Drawing: '+self.linesin+'\n')
                self.info.yview(tki.END)
                self.info.config(state=tki.DISABLED)
                self.plotx = self.drawopt[self.linesin][0]
                self.ploty = self.drawopt[self.linesin][1]
                self.titlexax = self.drawopt[self.linesin][2]
                self.titleyax = self.drawopt[self.linesin][3]
                self.figtitle = self.linesin
                if self.currentdata == 1:
                    self.myplot(0, Calculate.y[:, self.plotx],
                                Calculate.y[:, self.ploty],
                                self.titlexax, self.titleyax,
                                pttl=self.figtitle)
                if self.currentdata == 3:
                    self.myplot(0, self.multires[0][0][:, self.plotx],
                                self.multires[0][0][:, self.ploty], 
                                self.titlexax, self.titleyax,
                                pttl=self.figtitle)
                    for i in range(1, int(self.partnumentm.get())):
                        self.a.plot(self.multires[i][0][:, self.plotx],
                                    self.multires[i][0][:, self.ploty])

                self.Paper.show()
                if self.chnwvar.get() == 1:
                    self.shownewton2()
                if self.chstvar.get() == 1:
                    self.showstokes2()
            except AttributeError:
                print "No values for redraw2"
                pass
        self.Paper.show()

    def shownewton(self, event):
        self.shownewton()

    def shownewton2(self):
        try:
            # self.present = Calculate.y
            self.linesin = self.lines.get()
            self.nwplotx = self.drawopt[self.linesin][0]
            if self.nwplotx == 2:
                self.nwplotx = 14
            self.nwploty = self.drawopt[self.linesin][1]+12
            print "running shownewton2"
            if self.chnwvar.get() == 1:
                self.newtonline = self.a.plot(Calculate.y[:, self.nwplotx],
                                              Calculate.y[:, self.nwploty],
                                              color='magenta')
                self.Paper.show()
            else:
                try:
                    l = self.newtonline.pop(0)
                    l.remove()
                    del l
                    self.Paper.show()
                except AttributeError or IndexError:
                    self.Paper.show()
        except AttributeError:
            print "No values for newton2"
            pass

    def showstokes(self, event):
        self.showstokes2()

    def showstokes2(self):
        try:
            # self.present = Calculate.y
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
        self.viewset = self.view.get()
        if self.set3dstatevar == 1 and self.viewopt[self.viewset][0] == 35:
            try:
                self.x1 = float(self.xaxisscalef.get())
                self.x2 = float(self.xaxisscalet.get())
                self.y1 = float(self.yaxisscalef.get())
                self.y2 = float(self.yaxisscalet.get())
                self.z1 = float(self.zaxisscalef.get())
                self.z2 = float(self.zaxisscalet.get())
                if self.currentdata == 2:
                    xclip, yclip, zclip =\
                        self.manclip(Calculate3D.y[:, 4]*1, Calculate3D.y[:, 5]*1,
                                     Calculate3D.y[:, 6]*1, (self.x1, self.x2),
                                     (self.y1, self.y2),
                                     (self.z1, self.z2))
                    self.myplot(1, xclip, yclip, 'XDistance in [m]',
                                'YDistance in [m]', zttl='ZHeight in [m]',
                                zdat=zclip, pttl='Trajectory')
                if self.currentdata == 4:
                    xclip, yclip, zclip =\
                        self.manclip(self.multires[0][0][:, 4]*1,
                                     self.multires[0][0][:, 5]*1,
                                     self.multires[0][0][:, 6]*1,
                                     (self.x1, self.x2),
                                     (self.y1, self.y2),
                                     (self.z1, self.z2))
                    self.myplot(1, xclip, yclip, 'XDistance in [m]',
                                'YDistance in [m]', zttl='ZHeight in [m]',
                                zdat=zclip, pttl='Trajectory')
                    for i in range(1, int(self.partnumentm.get())):
                        xclip, yclip, zclip =\
                            self.manclip(self.multires[i][0][:, 4]*1,
                                         self.multires[i][0][:, 5]*1,
                                         self.multires[i][0][:, 6]*1,
                                         (self.x1, self.x2),
                                         (self.y1, self.y2),
                                         (self.z1, self.z2))
                        self.a.plot(xclip, yclip, zclip)
                self.a.set_zlim(self.z1, self.z2)
                self.a.set_xlim(self.x1, self.x2)
                self.a.set_ylim(self.y1, self.y2)
            except ValueError:
                print "Something is wrong with the axis fields"
                pass
        else:
            try:
                self.x1 = float(self.xaxisscalef.get())
                self.x2 = float(self.xaxisscalet.get())
                self.y1 = float(self.yaxisscalef.get())
                self.y2 = float(self.yaxisscalet.get())
                self.a.set_xlim(self.x1, self.x2)
                self.a.set_ylim(self.y1, self.y2)
            except ValueError:
                print "Something is wrong with the axis fields"
                pass
        self.Paper.show()
        print "Set axis"

    def validate(self, action, index, value_if_allowed, prior_value, text,
                 validation_type, trigger_type, widget_name):
        #print "Yes, I saw you"
        print text
        if text in '0123456789.-+':
            return True
        else:
            try:
                float(text)
                return True
            except ValueError:
                return False

    def myplot(self, persp3D, xdat, ydat, xttl, yttl,
               zdat=nm.NaN, zttl=nm.NaN, pttl=''):
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
        #self.Paper.show()
        return

    def myplot_add(self, persp3D, xdat, ydat, zdat=nm.NaN):
        if persp3D == 1:
            self.a.plot(xdat, ydat, zdat)
            self.a.mouse_init()
        else:
            self.a.plot(xdat, ydat, color='red')
        self.DrawGrid()
        return

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
