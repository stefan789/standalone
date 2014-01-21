# -*- coding: UTF-8 -*-
import dodegauss as d
import digiport as do
import time

dur = 20
keep = 2
p0 = do.DigiPort("Dev1", 0)
p0.off()
i = d.Degausser("Dev1", 0)
i.createNpWaveform(2.0,10.0,0,dur,keep,10000)
i.playWaveform()
p0.on()
time.sleep(1)
p0.off()
i.createNpWaveform(4.0,10.0,0,dur,keep,10000)
i.playWaveform()
p0.on()
time.sleep(1)
p0.off()
