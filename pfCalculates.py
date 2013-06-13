# -*- coding: utf-8 -*-
# Calculates.py
"""Calculations in separate threads"""

# importing libraries
import time
import threading
import numpy as nm
import decimal as dc
from oct2py import octave as oc
import Tkinter as tki


class Calculate3D(threading.Thread):
    def __init__(self, guest, rhop, dp, v, anglee, anglea, prec,
                 duration, windx, windy, windz, rhog, eta, grav,
                 posx, posy, posz):
        threading.Thread.__init__(self)
        self.rhop = (rhop)
        self.dp = (dp)
        self.v = (v)
        self.rhog = (rhog)
        self.eta = (eta)
        self.grav = (grav)
        self.anglee = (anglee)
        self.anglea = (anglea)
        self.prec = (prec)
        self.duration = (duration)
        self.windx = (windx)
        self.windy = (windy)
        self.windz = (windz)
        self.posx = posx
        self.posy = posy
        self.posz = posz
        self.guest = guest
        print self.rhop
        print self.dp
        print self.v
        print self.anglee
        print self.anglea
        print prec
        print duration
        print windx
        print windy
        print windz

    def decimalize(self, numin):
        decout = dc.Decimal(numin).quantize(dc.Decimal('.000001'),
                                            rounding=dc.ROUND_HALF_DOWN)
        return decout

    def run(self):
        print 'Reading values and calling Octave - mode 3D'
        [Calculate3D.y, Calculate3D.y2] = \
            oc.call('Wurf3D.m', [self.rhop, self.dp, self.v,
                    self.anglee, self.anglea, self.prec, self.duration,
                    self.windx, self.windy, self.windz, self.rhog,
                    self.eta, self.grav, self.posx, self.posy, self.posz],
                    verbose=False)
        print 'Done! Data from Octave available - mode 3D'
        self.guest.myplot(1, self.y[:, 4], self.y[:, 5], 'XDistance in [m]',
                          'YDistance in [m]', self.y[:, 6], 'ZHeight in [m]',
                          'Speed-Time-Horizontal')
        self.guest.Paper.show()

        # Return from octave:
        # dat1=[ngt,ngxs,ngys,ngzs,ngxp,ngyp,ngzp];
        # dat2=[duration,trelax,VTSN,VTSS,nusv];
        self.maxhight = str(max(Calculate3D.y[:, 6]))
        self.maxhightxid = nm.argmax(Calculate3D.y[:, 6])
        self.maxhightx = str(Calculate3D.y[self.maxhightxid, 4])
        self.maxhighty = str(Calculate3D.y[self.maxhightxid, 5])
        self.duration = str(Calculate3D.y2[0, 0])
        self.relaxtime = str(Calculate3D.y2[0, 1])
        self.VTSN = str(Calculate3D.y2[0, 2])
        self.VTSS = str(Calculate3D.y2[0, 3])
        self.nusv = str(Calculate3D.y2[0, 4])
        self.absolutez = [abs(x) for x in Calculate3D.y[1:, 6]]
        self.hitgroundx = str(Calculate3D.y[nm.argmin(self.absolutez), 4])
        self.hitgroundy = str(Calculate3D.y[nm.argmin(self.absolutez), 5])
        self.hitgroundxf = float(Calculate3D.y[nm.argmin(self.absolutez), 4])
        self.hitgroundyf = float(Calculate3D.y[nm.argmin(self.absolutez), 5])
        self.hitgrounddist = nm.sqrt(nm.square(self.hitgroundxf)
                                     + nm.square(self.hitgroundyf))
        dc.getcontext().prec = 12
        self.maxhightdec = self.decimalize(self.maxhight)
        self.maxhightxdec = self.decimalize(self.maxhightx)
        self.maxhightydec = self.decimalize(self.maxhighty)
        self.hitgroundxdec = self.decimalize(self.hitgroundx)
        self.hitgroundydec = self.decimalize(self.hitgroundy)
        self.hitgrounddist = self.decimalize(self.hitgrounddist)
        self.relaxtimedec = self.decimalize(self.relaxtime)
        self.durationdec = self.decimalize(self.duration)
        self.VTSNdec = self.decimalize(self.VTSN)
        self.VTSSdec = self.decimalize(self.VTSS)
        self.nusvdec = self.decimalize(self.nusv)
        maxflight = "Max flight height: \n" \
            + str(self.maxhightdec)+" meters in Z at \n"\
            + str(self.maxhightxdec)+" meters in X\n"\
            + str(self.maxhightydec)+" meters in Y\n"\
            + str(self.VTSNdec)+" m/s Newton settling velocity\n"\
            + str(self.VTSSdec)+" m/s Stokes settling velocity\n"\
            + str(self.nusvdec)+" m/s numerical settling velocity\n"
        if self.maxhightxid < nm.argmin(self.absolutez):
            hitground = "Hits ground at: \n"\
                + str(self.hitgroundxdec)+" meters X \n"\
                + str(self.hitgroundydec)+" meters Y \n"\
                + str(self.hitgrounddist)+" meters from source \n"
        else:
            hitground = "Does not reach the ground in observed timespan \n"
        entries = "Done \n"+"Relax-time: "+self.relaxtime+" seconds\n" +\
            "Duration: "+self.duration+" seconds\n"+maxflight+hitground\

        self.guest.info.config(state=tki.NORMAL)
        self.guest.info.insert(tki.END, entries)
        self.guest.info.yview(tki.END)
        self.guest.info.config(state=tki.DISABLED)
        self.guest.redraw2()
        return


class Calculate(threading.Thread):
    def __init__(self, guest, rhop, rhog, dp, v, angle,
                 prec, duration, eta, grav, windx, windy, posx, posz):
        threading.Thread.__init__(self)
        self.rhop = (rhop)
        self.dp = (dp)
        self.v = (v)
        self.angle = (angle)
        self.prec = (prec)
        self.duration = (duration)
        self.windx = (windx)
        self.windy = (windy)
        self.rhog = (rhog)
        self.eta = (eta)
        self.grav = (grav)
        self.posx = posx
        self.posz = posz
        self.guest = guest
        print self.rhop
        print self.dp
        print self.v
        print self.angle
        print prec
        print duration
        return

    def decimalize(self, numin):
        decout = dc.Decimal(numin).quantize(dc.Decimal('.001'),
                                            rounding=dc.ROUND_HALF_DOWN)
        return decout

    def run(self):
        print 'Reading values and calling Octave'
        [Calculate.y, Calculate.y2] = \
            oc.call('Wurfp3.m', [self.rhop, self.dp, self.v,
                    self.angle, self.prec, self.duration,
                    self.windx, self.windy, self.rhog,
                    self.eta, self.grav, self.posx, self.posz], verbose=False)
        print 'Done! Data from Octave available'
        self.guest.myplot(0, self.y[:, 0], self.y[:, 1], 'Time in [s]',
                          'Speed in [m/s]', pttl='Speed-Time-Horizontal')
        self.guest.Paper.show()

        # Return from octave: [t,nghs,nghp,ngvs,ngvp,hnt,hnp,hnv,vnt,vnv,vnp]
        self.maxhight = str(max(Calculate.y[:, 4]))
        self.maxhightxid = nm.argmax(Calculate.y[:, 4])
        self.maxhightx = str(Calculate.y[self.maxhightxid, 2])
        self.duration = str(Calculate.y2[0, 0])
        self.relaxtime = str(Calculate.y2[0, 1])
        self.VTSN = str(Calculate.y2[0, 2])
        self.VTSS = str(Calculate.y2[0, 3])
        self.nusv = str(Calculate.y2[0, 4])
        self.absolutey = [abs(x) for x in Calculate.y[1:, 4]]
        self.hitground = str(Calculate.y[nm.argmin(self.absolutey), 2])
        dc.getcontext().prec = 12
        self.maxhightdec = self.decimalize(self.maxhight)
        self.maxhightxdec = self.decimalize(self.maxhightx)
        self.hitgrounddec = self.decimalize(self.hitground)
        self.VTSNdec = self.decimalize(self.VTSN)
        self.VTSSdec = self.decimalize(self.VTSS)
        self.nusvdec = self.decimalize(self.nusv)
        maxflight = "Max flight height: "+str(self.maxhightdec)+" meters at "\
            + str(self.maxhightxdec)+" meters \n"+str(self.VTSNdec)\
            + " m/s Newton settling velocity\n"\
            + str(self.VTSSdec)+" m/s Stokes settling velocity\n"\
            + str(self.nusvdec)+" m/s numerical settling velocity\n"
        if self.maxhightxid < nm.argmin(self.absolutey):
            hitground = "Hits ground in: "+str(self.hitgrounddec)\
                        + " meters distance \n"
        else:
            hitground = "Does not reach the ground in observed timespan \n"
        entries = "Done \n"+"Relax-time: "+self.relaxtime+" seconds\n" + \
            "Duration: "+self.duration+" seconds\n"+maxflight+hitground\

        self.guest.info.config(state=tki.NORMAL)
        self.guest.info.insert(tki.END, entries)
        self.guest.info.yview(tki.END)
        self.guest.info.config(state=tki.DISABLED)
        self.guest.redraw2()
        return
