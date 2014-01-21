# -*- coding: UTF-8 -*-
import digiportthread as digip

class DigiPort():
    def __init__(self, device, chnnr):
        self.device = device
        self.chnnr = chnnr

    def on(self):
        mydigi = digip.DigiPortThread(self.device, self.chnnr, 0)
        mydigi.start()
        mydigi.join()
    
    def off(self):
        mydigi = digip.DigiPortThread(self.device, self.chnnr, 1)
        mydigi.start()
        mydigi.join()
