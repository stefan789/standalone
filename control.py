import wx
import copy
import collections
import controldeg
import json
import threading

class WorkerThread(threading.Thread):
    """ 
    dogaussing in own thread so that gui does not lock
    """
    def __init__(self, coils):
        print "worker thread init"
        threading.Thread.__init__(self)
        self.running = 1
        self.c = controldeg.controldegauss(coils)

    def run(self):
        print "thread running degaussing started"
        if self.running == 1:
            self.c.degauss()

    def abort(self):
        print "worker thread abort called"
        self.c.abort()
        self.running = 0


class control():
    def __init__(self, klasse):
        self.gui = klasse
        self.main = klasse.mainwin

        # bind buttons in mainwindow
        self.main.Bind(wx.EVT_BUTTON, self.onStart, self.main.startbtn)
        self.main.Bind(wx.EVT_BUTTON, self.onAbort, self.main.abortbtn)
        self.main.Bind(wx.EVT_BUTTON, self.onAdv, self.main.advbtn)

        # create timers for progress bars
        self.overallbar = self.main.overallbar
        self.overalltimer = wx.Timer(self.main, 999)
        self.currentbar = self.main.currentbar
        self.currenttimer = wx.Timer(self.main, 1000)

        self.coils = self.get_coil_from_file("coils.dict")
        self.usedcoils = copy.deepcopy(self.coils)
        self.tmpcoils = copy.deepcopy(self.coils)

        self.worker = None

    def get_coil_from_file(self, dictfile):

        self.coils = collections.OrderedDict([
            ("A-X", dict([('Amp', 4),('Freq', 10),('Dur', 10),('Keep', 1)])), 
            ("A-Y", dict([('Amp', 3),('Freq', 11),('Dur', 10),('Keep', 1)])), 
            ("A-Z", dict([('Amp', 3.5),('Freq', 12),('Dur', 9),('Keep', 1)])),       
            ("I-X", dict([('Amp', 9.5),('Freq', 13),('Dur', 8),('Keep', 1)])),
            ("I-Y", dict([('Amp', 8.7),('Freq', 14),('Dur', 7),('Keep', 1)])), 
            ("I-Z", dict([('Amp', 9.1),('Freq', 15),('Dur', 6),('Keep', 1)])), 
            ("All", dict([('Amp', 0),('Freq', 16),('Dur', 5),('Keep', 1)])),
            ("Offset", 0),
            ("Device", "Dev1")])

        readcoils = collections.OrderedDict()
       
        with open(str(dictfile), "r") as f:
            readcoils = json.loads(f.read(),
                    object_pairs_hook=collections.OrderedDict)
        return readcoils

    def on_overalltimer(self, e):
        self.overallcount += 100*0.5/(self.duration)
        self.overallbar.SetValue(self.overallcount)
        if self.overallcount >= 100:
            self.overallcount = 0
            self.overalltimer.Stop()
            self.overallbar.SetValue(100)
            dia = wx.MessageDialog(self.main.panel, "Done", "Info", wx.OK)
            dia.ShowModal()

    def on_currenttimer(self, e):
        self.count += (100*0.1)/self.coilduration
        self.currentbar.SetValue(self.count)
        if self.count >= 100:
            self.coilcounter += 1
            if self.coilcounter == self.nrCoils:
                self.currenttimer.Stop()
                self.currentbar.SetValue(0)
                self.count = 0
            else:
                self.currenttimer.Stop()
                self.currentbar.SetValue(0)
                self.count = 0
                self.currenttimer.Start(100)


    def onAbort(self, e):
        """
        dialog to abort degaussing
        """
        if not self.worker:
            dlg = wx.MessageDialog(self.main.panel, "Do you really want to quit the app?", "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
            result = dlg.ShowModal()
            if result == wx.ID_OK:
                self.main.Destroy()
            dlg.Destroy()

        elif self.worker:
            dlg = wx.MessageDialog(self.main.panel, "Interrupt degaussing?",
            "Confirm interrupt", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
            result = dlg.ShowModal()
            if result == wx.ID_OK:
                self.worker.abort()
                self.worker = None
            dlg.Destroy()


    def onStart(self, e):
        """
        begins degaussing by instanciating and starting workerthread
        """
        print "start pressed"
        if not self.worker:
            print "worker not running, started"
            self.worker = WorkerThread(self.usedcoils)
            self.worker.start()

        # bind timers and start
        #self.main.Bind(wx.EVT_TIMER, self.on_overalltimer, self.overalltimer, 999)
        #self.main.Bind(wx.EVT_TIMER, self.on_currenttimer, self.currenttimer, 1000)
        #self.currenttimer.Start(100)
        #self.overalltimer.Start(500)

    def onAdv(self, e):
        """ 
        creates advanced settings window
        """
        self.gui.createAdvWindow(self.tmpcoils)
        self.adv = self.gui.advwin
        self.main.Bind(wx.EVT_BUTTON, self.onAdvOk, self.adv.okbutton)
        self.main.Bind(wx.EVT_BUTTON, self.onAdvCancel, self.adv.cancelbutton)
        self.main.Bind(wx.EVT_BUTTON, self.onAdvReset, self.adv.resetbutton)
        self.main.Bind(wx.EVT_COMBOBOX, self.coilselection, self.adv.degaP.coilselector)
        self.main.Bind(wx.EVT_TEXT, self.changeAmp, self.adv.degaP.textAmp)
        self.main.Bind(wx.EVT_TEXT, self.changeFreq, self.adv.degaP.textFreq)
        self.main.Bind(wx.EVT_TEXT, self.changeDur, self.adv.degaP.textDur)
        self.main.Bind(wx.EVT_TEXT, self.changeKeep, self.adv.degaP.textKeep)
        self.main.Bind(wx.EVT_TEXT, self.changeOffset, self.adv.degaP.textOffset)
        self.main.Bind(wx.EVT_COMBOBOX, self.deviceselection, self.adv.degaP.inputDev)
        self.adv.Show()

    def onAdvReset(self, e):
        self.tmpcoils = copy.deepcopy(self.coils)
        choice = self.adv.degaP.coilselector.GetValue()
        self.adv.degaP.updateCoilSet(self.tmpcoils)
        self.adv.degaP.textAmp.SetValue(str(self.adv.degaP.coils[choice]['Amp']))
        self.adv.degaP.textFreq.SetValue(str(self.adv.degaP.coils[choice]['Freq']))
        self.adv.degaP.textDur.SetValue(str(self.adv.degaP.coils[choice]['Dur']))
        self.adv.degaP.textKeep.SetValue(str(self.adv.degaP.coils[choice]['Keep']))
        self.adv.degaP.textOffset.SetValue(str(self.adv.degaP.coils['Offset']))
        self.adv.degaP.inputDev.SetValue(str(self.adv.degaP.coils['Device']))


    def onAdvOk(self, e):
        """
        called on click on ok button in advanced settings window
        """
        self.usedcoils = copy.deepcopy(self.tmpcoils)
        print self.usedcoils
        self.adv.Destroy()

    def onAdvCancel(self, e):
        """
        called on click on cancel button in advanced settings window
        """
        self.adv.Destroy()

    def changeAmp(self, e):
        ''' bound to EVT_TXT for amp text field'''
        choice = self.adv.degaP.coilselector.GetValue()
        self.tmpcoils[choice]['Amp'] = self.adv.degaP.textAmp.GetValue()

    def changeFreq(self, e):
        choice = self.adv.degaP.coilselector.GetValue()
        self.tmpcoils[choice]['Freq'] = float(self.adv.degaP.textFreq.GetValue())

    def changeDur(self, e):
        choice = self.adv.degaP.coilselector.GetValue()
        self.tmpcoils[choice]['Dur'] = float(self.adv.degaP.textDur.GetValue())

    def changeKeep(self, e):
        choice = self.adv.degaP.coilselector.GetValue()
        self.tmpcoils[choice]['Keep'] = float(self.adv.degaP.textKeep.GetValue())

    def changeOffset(self, e):
        self.tmpcoils['Offset'] = float(self.adv.degaP.textOffset.GetValue())

    def changeDev(self, e):
        self.tmpcoils['Device'] = self.adv.degaP.textOffset.GetValue()

    def coilselection(self, e):
        choice = self.adv.degaP.coilselector.GetValue()
        if choice != "All":
            self.adv.degaP.textAmp.SetValue(str(self.adv.degaP.coils[choice]['Amp']))
            self.adv.degaP.textFreq.SetValue(str(self.adv.degaP.coils[choice]['Freq']))
            self.adv.degaP.textDur.SetValue(str(self.adv.degaP.coils[choice]['Dur']))
            self.adv.degaP.textKeep.SetValue(str(self.adv.degaP.coils[choice]['Keep']))
        if choice == "All":
            pop = wx.TextEntryDialog(self.adv.degaP.panel, "Enter Amplitude for ALL coils: ", "Amplitude", "")
            answ = pop.ShowModal()
            if answ == wx.ID_OK:
                nr = pop.GetValue()
            else:
                nr = "No Amplitude"
            try:
                isfloat = float(nr)
                self.adv.degaP.textAmp.SetValue(str(nr))
            except ValueError:
                self.adv.degaP.textAmp.SetValue("No Amplitude set")
                self.adv.degaP.textAmp.SetFocus()
            pop.Destroy()

    def deviceselection(self, e):
        choice = self.adv.degaP.inputDev.GetValue()
        self.tmpcoils['Device'] = choice
