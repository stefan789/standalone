import digiport as digiout
import digiinportthread as digiin
import time

rel1 = digiout.DigiPort("Dev1", 0)
rel2 = digiout.DigiPort("Dev1", 1)
rel3 = digiout.DigiPort("Dev1", 2)
rel4 = digiout.DigiPort("Dev1", 3)
rel5 = digiout.DigiPort("Dev1", 4)
rel6 = digiout.DigiPort("Dev1", 5)

sw1 = digiin.DigiInPortThread("Dev1", 24)
sw2 = digiin.DigiInPortThread("Dev1", 25)
sw3 = digiin.DigiInPortThread("Dev1", 26)
sw4 = digiin.DigiInPortThread("Dev1", 27)
sw5 = digiin.DigiInPortThread("Dev1", 28)
sw6 = digiin.DigiInPortThread("Dev1", 29)

def checksw():
    for i in range(24,30):
        print digiin.DigiInPortThread("Dev1", i).readi()
        time.sleep(0.5)

def switch(nr):
    digiout.DigiPort("Dev1", nr).on()
    time.sleep(0.5)
    digiout.DigiPort("Dev1", nr).off()
