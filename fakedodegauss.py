import time
import numpy
import threading
import matplotlib.pyplot as plt


class ownThread(threading.Thread):
    def __init__(self, threadID, duration):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.duration = duration

    def run(self):
        print "Starting"
        time.sleep(self.duration)
        print "Done"

class Degausser():
    def __init__(self, device, chnnr):
        self.dev = str(device) + "/" + "ao" + str(chnnr)


    def createWaveform(self, amplitude, frequency, offset, duration, keeptime, sampleRate):
        self.sampleRate = sampleRate
        t = numpy.arange(0, duration + 1.0/sampleRate, 1.0/self.sampleRate)
#        x = numpy.piecewise(t, [self.test(t,keeptime,True), self.test(t, keeptime, False)], 
#                [self.keep(amp, freq, offset, duration, keeptime, sampleRate, t), 
#                self.decrease(amp, freq, offset, duration, keeptime, sampleRate, t)])
        x = (amplitude - (amplitude/(duration)) * t) * (-1) * numpy.sin( 2*numpy.math.pi*frequency*t ) + offset 
        self.periodLength = len( x )
        self.time = t
        self.data = numpy.zeros((self.periodLength, ))
        self.data = x
        plt.plot(self.time, self.data)
        plt.show(block=False)
        thread1 = ownThread(1, duration)
        thread1.start()
        thread1.join()


if __name__ == "__main__":
    gaus = Degausser("Dev0", 0)
    gaus.createWaveform(1,1,0,30.0,1,10000)
