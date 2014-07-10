import model
import view
import wx
import copy
import collections
import json
from datetime import datetime

#from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

class Controller:
    def __init__(self, app):
        self.model = model.Model()
        self.model.set_coils_from_file("innercoils.dict")
        self.view = view.View(None)

        self.view.mainWin.startbtn.Bind(wx.EVT_BUTTON, self.StartBtn)
        self.view.mainWin.abortbtn.Bind(wx.EVT_BUTTON, self.AbortBtn)
        self.view.mainWin.advbtn.Bind(wx.EVT_BUTTON, self.AdvBtn)
        self.view.mainWin.saveStatus.Bind(wx.EVT_CHECKBOX, self.checkstatus)

        self.overalltimer = wx.Timer()
        self.overalltimer.Bind(wx.EVT_TIMER, self.OnTimer)

        pub.subscribe(self.CoilsChanged, "COILCHANGE")
        pub.subscribe(self.statusUpdate, "status.update")
        pub.subscribe(self.degaussprogress, "degauss.progress")

    def setModelCoils(self, coils):
        self.model.setCoils(coils)

    def setModelCoilsfromfile(self, dictfile):
        self.model.set_coils_from_file(dictfile)

    def getModelCoilsfromfile(self, dictfile):
        with open(str(dictfile), "r") as f:
            coils = json.loads(f.read(), object_pairs_hook =
                    collections.OrderedDict)
            if self.model.checkCoils(coils):
                pub.sendMessage("COILCHANGE", status="Coils read from file")
                return coils
            else:
                pub.sendMessage("COILCHANGE", status = "Error: file wrong")

    def AdvBtn(self, e):
        self.tmpcoils = copy.deepcopy(self.model.coils)
        self.view.createAdvWin(self.tmpcoils)
        self.view.advWin.okbutton.Bind(wx.EVT_BUTTON, self.onAdvOk)
        self.view.advWin.resetbutton.Bind(wx.EVT_BUTTON, self.onAdvReset)
        self.view.advWin.cancelbutton.Bind(wx.EVT_BUTTON, self.onAdvCancel)
        self.view.advWin.degaP.coilselector.Bind(wx.EVT_COMBOBOX, self.coilselection)
        self.view.advWin.degaP.textAmp.Bind(wx.EVT_TEXT, self.changeAmp)
        self.view.advWin.degaP.textFreq.Bind(wx.EVT_TEXT, self.changeFreq)
        self.view.advWin.degaP.textDur.Bind(wx.EVT_TEXT, self.changeDur)
        self.view.advWin.degaP.textKeep.Bind(wx.EVT_TEXT, self.changeKeep)

        self.view.advWin.coilP.rb1.Bind(wx.EVT_RADIOBUTTON, self.radioselection)
        self.view.advWin.coilP.rb2.Bind(wx.EVT_RADIOBUTTON, self.radioselection)
        self.view.advWin.coilP.rb3.Bind(wx.EVT_RADIOBUTTON, self.radioselection)
        self.view.advWin.coilP.rb4.Bind(wx.EVT_RADIOBUTTON, self.radioselection)
        self.view.advWin.coilP.rb5.Bind(wx.EVT_RADIOBUTTON, self.radioselection)

        self.view.advWin.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED,
                self.nbpagechange)

    def StartBtn(self, e):
        if not self.model.degaussingcontrol:
            pub.sendMessage('status.update', status="Started: %s" % datetime.now().strftime("%d.%m.%Y - %X"))
            runs = self.view.mainWin.runNrCtrl.GetValue()
            pub.sendMessage('status.update', status="Nr of runs %s" % str(runs))
            self.totalcount = 0
            self.totaldur = 2
            for coil in self.model.coils:
                if coil != 'All' and coil != 'Device' and coil != 'Offset':
                    self.totaldur += int(self.model.coils[coil]['Dur']) + int(self.model.coils[coil]['Keep']) + int(4)
            self.totaldur = self.totaldur * runs
            pub.sendMessage('status.update', status="Total duration approx %s" % str(self.totaldur) + " s" )
            self.view.mainWin.overallbar.SetRange(self.totaldur*10-50)
            self.overalltimer.Start(100)
            self.model.degauss(runs)
        elif self.model.degaussingcontrol.is_alive():
            pub.sendMessage('status.update', status='Already degaussing')
            self.view.showRunningAlert()

    def OnTimer(self, event):
        self.totalcount += 1
        self.view.mainWin.overallbar.SetValue(self.totalcount)
        if self.totalcount == self.totaldur*10:
            self.overalltimer.Stop()

    def AbortBtn(self, e): 
        if not self.model.degaussingcontrol:
            if self.view.confirmAbort() == wx.ID_OK:
                self.overalltimer.Stop()
                self.view.mainWin.Destroy()
        elif self.model.degaussingcontrol.is_alive():
            if self.view.confirmInterrupt() == wx.ID_OK:
                self.overalltimer.Stop()
                self.model.interruptdegauss()
        else:
            if self.view.confirmAbort() == wx.ID_OK:
                self.overalltimer.Stop()
                self.view.mainWin.Destroy()

    def onAdvOk(self, e):
        if self.view.advWin.coilP.rb5.GetValue():
            fil = self.view.advWin.coilP.text.GetValue()
            if fil == "":
                self.view.advWin.nb.SetSelection(0)
                self.view.showCustomFileAlert()
            else:
                self.tmpcoils = self.getModelCoilsfromfile(str(fil))
                pub.sendMessage("status.update", status=str(fil))
        elif self.view.advWin.coilP.rb1.GetValue():
            pub.sendMessage("status.update", status="Inner coils selected")
            self.tmpcoils = self.getModelCoilsfromfile("innercoils.dict")
        elif self.view.advWin.coilP.rb2.GetValue():
            pub.sendMessage("status.update", status="Middle coils selected")
            self.tmpcoils = self.getModelCoilsfromfile("middlecoils.dict")
        elif self.view.advWin.coilP.rb3.GetValue():
            pub.sendMessage("status.update", status="Outer coils selected")
            self.tmpcoils = self.getModelCoilsfromfile("outercoils.dict")
        elif self.view.advWin.coilP.rb4.GetValue():
            pub.sendMessage("status.update", status="All coils selected")
            self.tmpcoils = self.getModelCoilsfromfile("allcoils.dict")
        else:
            # Fehlerfall
            pass
        self.setModelCoils(self.tmpcoils)
        #pub.sendMessage("status.update", status = "Coils set")
        self.view.advWin.Destroy()

    def onAdvReset(self, e):
        self.tmpcoils = copy.deepcopy(self.model.coils)
        choice = self.view.advWin.degaP.coilselector.GetValue()
        self.view.advWin.degaP.textAmp.SetValue(str(self.tmpcoils[str(choice)]["Amp"]))
        self.view.advWin.degaP.textFreq.SetValue(str(self.tmpcoils[str(choice)]["Freq"]))
        self.view.advWin.degaP.textDur.SetValue(str(self.tmpcoils[str(choice)]["Dur"]))
        self.view.advWin.degaP.textKeep.SetValue(str(self.tmpcoils[str(choice)]["Keep"]))

    def onAdvCancel(self, e):
        self.view.advWin.Destroy()

    def coilselection(self, e):
        choice = self.view.advWin.degaP.coilselector.GetValue()
        self.view.advWin.degaP.textAmp.SetValue(str(self.tmpcoils[str(choice)]["Amp"]))
        self.view.advWin.degaP.textFreq.SetValue(str(self.tmpcoils[str(choice)]["Freq"]))
        self.view.advWin.degaP.textDur.SetValue(str(self.tmpcoils[str(choice)]["Dur"]))
        self.view.advWin.degaP.textKeep.SetValue(str(self.tmpcoils[str(choice)]["Keep"]))

    def radioselection(self, e):
        state1 = self.view.advWin.coilP.rb1.GetValue()
        state2 = self.view.advWin.coilP.rb2.GetValue()
        state3 = self.view.advWin.coilP.rb3.GetValue()
        state4 = self.view.advWin.coilP.rb4.GetValue()
        state5 = self.view.advWin.coilP.rb5.GetValue()
        if state5 == True:
            self.view.showAdvTextLine(True)
        else:
            self.view.advWin.coilP.text.SetValue("")
            self.view.showAdvTextLine(False)

    def nbpagechange(self, e):
        if self.view.advWin.nb.GetSelection() == 1:
            if self.view.advWin.coilP.rb5.GetValue():
                fil = self.view.advWin.coilP.text.GetValue()
                if fil == "":
                    self.view.advWin.nb.SetSelection(0)
                    self.view.showCustomFileAlert()
                else:
                    self.tmpcoils = self.getModelCoilsfromfile(str(fil))
                    pub.sendMessage("status.update", status=str(fil))
            elif self.view.advWin.coilP.rb1.GetValue():
                pub.sendMessage("status.update", status="Inner coils selected")
                self.tmpcoils = self.getModelCoilsfromfile("innercoils.dict")
            elif self.view.advWin.coilP.rb2.GetValue():
                pub.sendMessage("status.update", status="Middle coils selected")
                self.tmpcoils = self.getModelCoilsfromfile("middlecoils.dict")
            elif self.view.advWin.coilP.rb3.GetValue():
                pub.sendMessage("status.update", status="Outer coils selected")
                self.tmpcoils = self.getModelCoilsfromfile("outercoils.dict")
            elif self.view.advWin.coilP.rb4.GetValue():
                pub.sendMessage("status.update", status="All coils selected")
                self.tmpcoils = self.getModelCoilsfromfile("allcoils.dict")
            else:
                # Fehlerfall
                pass
            self.view.setCoilSelectorList(self.tmpcoils)

    def checkstatus(self, e):
        sender = e.GetEventObject()
        isChecked = sender.GetValue()

        if isChecked:
            pub.subscribe(self.writeStatus, "status.update")
        else:
            pub.unsubscribe(self.writeStatus, "status.update")

    def changeAmp(self, e):
        choice = self.view.advWin.degaP.coilselector.GetValue()
        self.tmpcoils[str(choice)]["Amp"] = self.view.advWin.degaP.textAmp.GetValue()
    
    def changeFreq(self, e):
        choice = self.view.advWin.degaP.coilselector.GetValue()
        self.tmpcoils[str(choice)]["Freq"] = self.view.advWin.degaP.textFreq.GetValue()

    def changeDur(self, e):
        choice = self.view.advWin.degaP.coilselector.GetValue()
        self.tmpcoils[str(choice)]["Dur"] = self.view.advWin.degaP.textDur.GetValue()
    
    def changeKeep(self, e):
        choice = self.view.advWin.degaP.coilselector.GetValue()
        self.tmpcoils[str(choice)]["Keep"] = self.view.advWin.degaP.textKeep.GetValue()

    def writeStatus(self, status, extra=None):
        with open("log.txt", "a") as f:
            f.write("["+datetime.now().strftime("%X")+"] "+str(status) + "\n")
    
    def statusUpdate(self, status, extra=None):
        self.view.mainWin.status.AppendText("["+datetime.now().strftime("%X")+"] "+str(status) + "\n")

    def CoilsChanged(self, status):
        self.view.mainWin.status.AppendText("Coils set" + "\n")
    
    def degaussprogress(self, status, extra=None):
        self.view.mainWin.status.AppendText(str(status) + "\n")

