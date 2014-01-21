# -*- coding: UTF-8 -*-
import threading
import ctypes
import numpy

nidaq = ctypes.windll.nicaiu

int32 = ctypes.c_long
uInt32 = ctypes.c_ulong
uInt64 = ctypes.c_ulonglong
float64 = ctypes.c_double
bool32 = uInt32
TaskHandle = uInt32

DAQmx_Val_Cfg_Default = int32(-1)
DAQmx_Val_Volts = 10348
DAQmx_Val_Rising = 10280
DAQmx_Val_FiniteSamps = 10178
DAQmx_Val_ContSamps = 10123
DAQmx_Val_GroupByChannel = 0
DAQmx_Val_ChanForAllLines = 1
DAQmx_Val_ChanPerLine = 0

class DigiPortThread(threading.Thread):
    def __init__(self, device, chnnr, state):
        self.running = True
        self.device = device
        self.chnnr = chnnr
        self.taskHandle = TaskHandle( 0 )
        if state == 1:
            self.data = numpy.array([1])
        elif state == 0:
            self.data = numpy.array([0])
        else:
            print "wrong state"
            self.data = numpy.array([0])
        dev = str(self.device) + "/port0/line" + str(self.chnnr)
        self.CHK(nidaq.DAQmxCreateTask("", ctypes.byref( self.taskHandle )))
        self.CHK(nidaq.DAQmxCreateDOChan( self.taskHandle, dev, "",
            DAQmx_Val_ChanPerLine))
        self.CHK(nidaq.DAQmxWriteDigitalU32( self.taskHandle, 1, 1,
            float64(10.0), DAQmx_Val_GroupByChannel, self.data.ctypes.data,
            None, None))
        threading.Thread.__init__(self)

    def CHK(self, err):
        '''a simple error checking routine'''
        if err < 0:
            buf_size = 100
            buf = ctypes.create_string_buffer('\000' * buf_size)
            nidaq.DAQmxGetErrorString(err, ctypes.byref(buf), buf_size)
            raise RuntimeError('nidaq failed with error %d: %s'%(err, repr(buf.value)))
        if err > 0:
            buf_size = 100
            buf = ctypes.create_string_buffer('\000' * buf_size)
            nidaq.DAQmxGetErrorString(err, ctypes.byref(buf), buf_size)
            raise RuntimeError('nidaq generated waring %d: %s'%(err, repr(buf.value)))
    
    def run(self):
        self.CHK(nidaq.DAQmxStartTask( self.taskHandle ))
        
    def stop(self):
        self.running = False
        nidaq.DAQmxStopTask( self.taskHandle )
    
    def __del__(self):
        nidaq.DAQmxClearTask( self.taskHandle )

