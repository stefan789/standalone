from wx.lib.pubsub import pub
import threading
import collections
import json
import controldeg

class DegaussingWorkerThread(threading.Thread):
    """ 
    dogaussing in own thread so that gui does not lock
    """
    def __init__(self, coils):
        threading.Thread.__init__(self)
        self.running = 1
        self.c = controldeg.controldegauss(coils)

    def run(self):
        pub.sendMessage("status.update", status = "Degaussing Thread Worker started")
        if self.running == 1:
            self.c.degauss()

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

    def set_coils_from_file(self, dictfile):
        with open(str(dictfile), "r") as f:
            coils = json.loads(f.read(), object_pairs_hook =
                    collections.OrderedDict)
            self.coils = coils
            pub.sendMessage("COILCHANGE", status=self.coils)
    
    def degauss(self):
        self.degaussingcontrol = DegaussingWorkerThread(self.coils)
        self.degaussingcontrol.start()

    def interruptdegauss(self):
        self.degaussingcontrol.abort()
        pub.sendMessage("status.update", status = "Interrupted")

    def activateCoil(self):
        pass

    def readSwitch(self):
        pass

