from wx.lib.pubsub import Publisher as pub
import threading
import collections
import json
import controldeg

class DegaussingWorkerThread(threading.Thread):
    """ 
    dogaussing in own thread so that gui does not lock
    """
    def __init__(self, coils):
        print "worker thread init"
        threading.Thread.__init__(self)
        self.running = 1
        self.c = controldeg.controldegauss(coils)

    def run(self):
        pub.sendMessage("statusupdate", "Degaussing Thread Worker started")
        print "thread running degaussing started"
        if self.running == 1:
            self.c.degauss()

    def abort(self):
        print "worker thread abort called"
        self.c.abort()
        self.running = 0


class Model():
    def __init__(self):
        self.coils = None
        self.degaussingcontrol = None

    def set_coils_from_file(self, dictfile):
        with open(str(dictfile), "r") as f:
            self.coils = json.loads(f.read(), object_pairs_hook =
                    collections.OrderedDict)
            pub.sendMessage("COILCHANGE", self.coils)
    
    def degauss(self):
        self.degaussingcontrol = DegaussingWorkerThread(self.coils)
        self.degaussingcontrol.start()

    def activateCoil(self):
        pass

    def readSwitch(self):
        pass

