import model
import view
import wx
import copy
import collections

#from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

class Controller:
    def __init__(self, app):
        self.model = model.Model()
        self.model.set_coils_from_file("coils.dict")
        self.view = view.View(None)

        self.view.mainWin.startbtn.Bind(wx.EVT_BUTTON, self.StartBtn)
        self.view.mainWin.abortbtn.Bind(wx.EVT_BUTTON, self.AbortBtn)
        self.view.mainWin.advbtn.Bind(wx.EVT_BUTTON, self.AdvBtn)

        pub.subscribe(self.CoilsChanged, "COILCHANGE")
        pub.subscribe(self.statusUpdate, "status.update")
        pub.subscribe(self.degaussprogress, "degauss.progress")

    def setCoils(self, dictfile):
        self.model.set_coils_from_file(str(dictfile))

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

        self.view.advWin.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED,
                self.nbpagechange)

    def StartBtn(self, e):
        self.model.degauss()

    def AbortBtn(self, e):
        if self.model.degaussingcontrol.is_alive():
            if self.view.confirmAbort() == wx.ID_OK:
                self.model.interruptdegauss()
        else:
            if self.view.confirmAbort() == wx.ID_OK:
                self.view.mainWin.Destroy()
            
    def onAdvOk(self, e):
        self.model.coils = copy.deepcopy(self.tmpcoils)
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
        if state4 == True:
            self.view.showAdvTextLine(True)
        else:
            self.view.advWin.coilP.text.SetValue("")
            self.view.showAdvTextLine(False)

    def nbpagechange(self, e):
        if self.view.advWin.nb.GetSelection() == 1:
            if self.view.advWin.coilP.rb4.GetValue():
                fil = self.view.advWin.coilP.text.GetValue()
                if fil == "":
                    self.view.advWin.nb.SetSelection(0)
                    self.view.showCustomFileAlert()
                else:
                    self.setCoils(str(fil))
                    pub.sendMessage("status.update", str(fil), extra = None)
            elif self.view.advWin.coilP.rb1.GetValue():
                pub.sendMessage("status.update", status="Inner coils selected")
                self.setCoils("coils.dict")
            elif self.view.advWin.coilP.rb2.GetValue():
                pub.sendMessage("status.update", status="Outer coils selected")
                self.setCoils("outercoils.dict")
            elif self.view.advWin.coilP.rb3.GetValue():
                pub.sendMessage("status.update", status="All coils selected")
                self.setCoils("coils.dict")
            else:
                # Fehlerfall
                pass
            self.tmpcoils = copy.deepcopy(self.model.coils)
            self.view.setCoilSelectorList(self.tmpcoils)


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
    
    def statusUpdate(self, status, extra=None):
        self.view.mainWin.status.AppendText(str(status) + "\n")

    def CoilsChanged(self, status):
        self.view.mainWin.status.AppendText("Coils set" + "\n")
    
    def degaussprogress(self, status, extra=None):
        self.view.mainWin.status.AppendText(str(status) + "\n")

