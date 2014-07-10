import numpy as np
import nidaqmx
import time
from wx.lib.pubsub import pub

class VoltageDivider():
    def __init__(self, dev):
        self.dev = dev
        self.output_str = dev+"/port0/line16:23"
        self.dotask = nidaqmx.DigitalOutputTask()
        self.dotask.create_channel(self.output_str)
    
    def resetall(self):
        ddat = np.ones(8, dtype = np.uint8)
        ddat[6] = 0
        self.dotask.write(ddat, auto_start = True, layout = "group_by_channel")
        time.sleep(1)
        ddat[6] = 1
        self.dotask.write(ddat, auto_start = True, layout = "group_by_channel")

    def setnr(self, nr):
        self.resetall()
        ddat = np.ones(8, dtype = np.uint8)
        ddat[nr] = 0
        self.dotask.write(ddat, auto_start = True, layout = "group_by_channel")
        time.sleep(1)
        ddat[nr] = 1
        self.dotask.write(ddat, auto_start = True, layout = "group_by_channel")        

class DigitalInput():
    def __init__(self, dev):
        self.dev = dev
        self.input_str = dev+"/port0/line24:31,"+dev+"/port2/line0:7"
        self.ditask = nidaqmx.DigitalInputTask()
        self.ditask.create_channel(self.input_str)

    def read(self):
        return self.ditask.read(1)[0][0]

class DigitalOutput():
    def __init__(self, dev, channels):
        self.dev = dev
        self.nrchans = int(channels.split(":")[1]) - int(channels.split(":")[0]) + 1
        self.output_str = dev+"/port0/line" + str(channels)
        self.dotask = nidaqmx.DigitalOutputTask()
        self.dotask.create_channel(self.output_str, name = "line"
                +str(channels))

    def switch(self, nr):
        ddat = np.ones(self.nrchans, dtype = np.uint8)
        ddat[nr] = 0
        self.dotask.write(ddat, auto_start = True, layout = "group_by_channel")
        time.sleep(1)
        ddat[nr] = 1
        self.dotask.write(ddat, auto_start = True, layout = "group_by_channel")
        time.sleep(1)

class SwitchCoil():
    def __init__(self, dev):
        self.di = DigitalInput(dev)
        self.do = DigitalOutput(dev, "0:15")
        self.nrchans = 16

    def alloff(self):
        curstate = self.di.read()
        if 1 in curstate:
            curon = np.where(curstate==1)[0]
            #print curon
            for a in curon:
                self.do.switch(a)
        pub.sendMessage("status.update", status="Relay states: %s" % str(self.di.read()))
        #print self.di.read()

    def activate(self, nr):
        if nr > self.nrchans-1:
            pass
        else:
            curstate = self.di.read()
            if 1 in curstate:
                curon = np.where(curstate==1)[0]
                print curon
                for a in curon:
                    if a != nr:
                        self.do.switch(a)
            if curstate[nr] == 1:
                pass
            if curstate[nr] == 0:
                self.do.switch(nr)
        pub.sendMessage("status.update", status="Relay states: %s" % str(self.di.read()))
            #print self.di.read()

