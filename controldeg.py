import dodegauss as deg
import digiportlib as digilib
import collections
import time
import copy

from wx.lib.pubsub import pub

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

        
        self.swc = digilib.SwitchCoil(str(self.dev))
        self.swc.alloff()
        self.vd = digilib.VoltageDivider(str(self.dev))
        self.vd.resetall()
        time.sleep(1)
        self._running = 1

    def degauss(self, runs):
        for i in range(runs):
            for coil in self.degcoils:
                if self._running == 1:
                    amp = float(self.degcoils[coil]['Amp'])
                    freq = float(self.degcoils[coil]['Freq'])
                    dur = float(self.degcoils[coil]['Dur'])
                    keep = float(self.degcoils[coil]['Keep'])
                
                    # hier prints mit aktuellem status, bzw setlabel fuer ein textfeld
                    self.dega.createNpWaveform(amp, freq, self.offset, dur, keep, 20000)
                    pub.sendMessage("status.update", status = "Waveform parameters: %s" % str("A = " + str(amp) + " V, Freq = " + str(freq) + " Hz, Dur = " + str(dur) + " s, keep = " + str(keep) + " s"))
                    self.swc.alloff()
                    pub.sendMessage("status.update", status = "All coils off")
                    time.sleep(0.5)
                    self.vd.setnr(self.degcoils[coil]["VoltageDivider"])
                    pub.sendMessage("status.update", status = "Voltagedivider set to %s" % str(self.degcoils[coil]["VoltageDivider"]))
                    self.swc.activate(self.degcoils[coil]["RelayPort"])
                    pub.sendMessage("status.update", status = "Coil %s activated" %str(self.degcoils[coil]["RelayPort"]))
                    time.sleep(1)
                    self.dega.playWaveform()
                    pub.sendMessage("staus.update", status =  "Waveform played")
                    self.swc.alloff()
                    pub.sendMessage("status.update", status = "All coils off")
                    time.sleep(0.5)
                    self.vd.resetall()
                    pub.sendMessage("status.update", status = "Voltagedivider reset")
                else:
                    self.swc.alloff()
                    self.vd.resetall()
            pub.sendMessage("status.update", status = "DONE")

    def abort(self):
        self.dega.abortWaveform()
        self._running = 0

