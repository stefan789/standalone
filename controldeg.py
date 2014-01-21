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

    def degauss(self):
        for coil in self.degcoils:
            amp = float(self.degcoils[coil]['Amp'])
            freq = float(self.degcoils[coil]['Freq'])
            dur = float(self.degcoils[coil]['Dur'])
            keep = float(self.degcoils[coil]['Keep'])

            
            # hier prints mit aktuellem status, bzw setlabel fuer ein textfeld
            self.dega.createNpWaveform(amp, freq, self.offset, dur, keep, 20000)
            # 
            self.swc.alloff()
            #
            time.sleep(0.5)
            self.vd.setnr(self.degcoils[coil]["VoltageDivider"])
            #
            self.swc.activate(self.degcoils[coil]["RelayPort"])
            #
            time.sleep(1)
            self.dega.playWaveform()
            #
            self.swc.alloff()
            time.sleep(0.5)
            self.vd.resetall()
