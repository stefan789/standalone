import dodegauss as deg
import digiportlib as digilib
import collections
import time
import copy

class controldegauss():
    def __init__(self, coils):
        self.coils = coils
        self.degcoils = copy.deepcopy(self.coils)
        self.dev = self.degcoils['Device']
        self.degcoils.pop("Device")
        self.offset = self.degcoils["Offset"]
        self.degcoils.pop("Offset")
        self.degcoils.pop("All")
        
        self.dega = deg.Degausser(str(self.dev),0)

        self.swc = digilib.SwitchCoil()
        self.swc.alloff()
        self.vd = digilib.VoltageDivider()
        self.vd.resetall()
        time.sleep(1)
        self._running = 1

    def degauss(self):
        print "degauss called"
        for coil in self.degcoils:
            if self._running == 1:
                amp = float(self.degcoils[coil]['Amp'])
                freq = float(self.degcoils[coil]['Freq'])
                dur = float(self.degcoils[coil]['Dur'])
                keep = float(self.degcoils[coil]['Keep'])
            
                # hier prints mit aktuellem status, bzw setlabel fuer ein textfeld
                self.dega.createNpWaveform(amp, freq, self.offset, dur, keep, 20000)
                print "waveform created"
                self.swc.alloff()
                print "all coils off"
                time.sleep(0.5)
                self.vd.setnr(self.degcoils[coil]["VoltageDivider"])
                print "Voltage Divider set to %s" % str(self.degcoils[coil]["VoltageDivider"])
                self.swc.activate(self.degcoils[coil]["RelayPort"])
                print "Coil %s activated" %str(self.degcoils[coil]["RelayPort"])
                time.sleep(1)
                self.dega.playWaveform()
                print "waveform played"
                self.swc.alloff()
                time.sleep(0.5)
                self.vd.resetall()
            else:
                self.swc.alloff()
                self.vd.resetall()

    def abort(self):
        print "controldeg abort called"
        self.dega.abortWaveform()
        self._running = 0

