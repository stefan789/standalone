import mainWindow
import advWindow
import wx

class View():
    def __init__(self, parent):
        self.mainWin = mainWindow.mainWindow(parent)
        self.mainWin.Show()

    def createAdvWin(self, coils):
        self.advWin = advWindow.advWindow(self.mainWin)
        self.setCoilSelectorList(coils)
        self.advWin.Show()

    def setCoilSelectorList(self, coils):
        self.advWin.degaP.coilselector.SetItems(coils.keys()[:-2])
        self.advWin.degaP.coilselector.SetSelection(0)
        choice = self.advWin.degaP.coilselector.GetValue()
        self.advWin.degaP.textAmp.SetValue(str(coils[str(choice)]["Amp"]))
        self.advWin.degaP.textFreq.SetValue(str(coils[str(choice)]["Freq"]))
        self.advWin.degaP.textDur.SetValue(str(coils[str(choice)]["Dur"]))
        self.advWin.degaP.textKeep.SetValue(str(coils[str(choice)]["Keep"]))

    def confirmAbort(self):
        dlg = wx.MessageDialog(self.mainWin, "Do you really want to quit the app?", "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        return result

    def confirmInterrupt(self):
        dlg = wx.MessageDialog(self.mainWin, "Do you really want to interrupt degaussing?", "Confirm", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        return result

    def showAdvTextLine(self, state):
        if state:
            self.advWin.coilP.text.Show()
            self.advWin.coilP.panel.Layout()
        else:
            self.advWin.coilP.text.Hide()
            self.advWin.coilP.panel.Layout()

    def showCustomFileAlert(self):
        wx.MessageBox("No file specified", "Error", wx.OK)

    def showRunningAlert(self):
        wx.MessageBox("Degaussing in progress", "Error", wx.OK)
