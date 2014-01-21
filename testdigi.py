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

task = TaskHandle(0)
dat = numpy.array([0])

def CHK(err):
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

def writed( val ):
    CHK(nidaq.DAQmxWriteDigitalU32( task, 1, 1, float64(10.0),
        DAQmx_Val_GroupByChannel, val.ctypes.data, None, None))


CHK(nidaq.DAQmxCreateTask("", ctypes.byref( task )))
CHK(nidaq.DAQmxCreateDOChan( task, "Dev1/port0/line0", "", DAQmx_Val_ChanPerLine))
writed( numpy.array([0]) )
