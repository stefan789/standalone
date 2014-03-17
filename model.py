from wx.lib.pubsub import pub
import threading
import collections
import json
import controldeg
import copy

class DegaussingWorkerThread(threading.Thread):
    """ 
    dogaussing in own thread so that gui does not lock
    """
    def __init__(self, coils, runs):
        threading.Thread.__init__(self)
        self.runs = runs
        self.running = 1
        self.c = controldeg.controldegauss(coils)

    def run(self):
        pub.sendMessage("status.update", status = "Degaussing Thread Worker started")
        if self.running == 1:
            self.c.degauss(self.runs)

    def abort(self):
        pub.sendMessage("status.update", status = "degaussing interrupted")
        self.c.abort()
        self.running = 0


class Model():
    def __init__(self):
        self.coils = None
        self.degaussingcontrol = None

    def setCoils(self, coildict):
        self.coils = coildict

    def checkCoils(self, coils):
        a = True
        ccoils = copy.copy(coils)
        ccoils.pop("Device")
        ccoils.pop("Offset")
        for coil in ccoils:
            a = a and (ccoils[coil].keys() == ['Amp', 'Freq', 'Dur', 'Keep', 'RelayPort', 'VoltageDivider'])
        return a

    def set_coils_from_file(self, dictfile):
        with open(str(dictfile), "r") as f:
            coils = json.loads(f.read(), object_pairs_hook =
                    collections.OrderedDict)
            if self.checkCoils(coils):
                self.coils = coils
                pub.sendMessage("COILCHANGE", status=self.coils)
            else:
                pub.sendMessage("COILCHANGE", status = "Error: file wrong")
    
    def degauss(self, runs):
        self.degaussingcontrol = DegaussingWorkerThread(self.coils, runs)
        self.degaussingcontrol.start()

    def interruptdegauss(self):
        self.degaussingcontrol.abort()
        pub.sendMessage("status.update", status = "Interrupted")

    def activateCoil(self):
        pass

    def readSwitch(self):
        pass

