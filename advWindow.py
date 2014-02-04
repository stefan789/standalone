import wx
import advDegaPanel
import advCoilPanel

class advWindow(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, wx.ID_ANY, "Advanced Settings", size =(400,300))
        self.SetSizeHints(400,350,800,600)
        panel = wx.Panel(self, wx.ID_ANY)

        topSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.nb = wx.Notebook(panel)
        self.coilP = advCoilPanel.advCoilPanel(self.nb)
        self.nb.AddPage(self.coilP.panel, "Coils  ")
        self.degaP = advDegaPanel.advDegaPanel(self.nb)
        self.nb.AddPage(self.degaP.panel, "Parameters  ")

        topSizer.Add(self.nb, flag = wx.EXPAND|wx.ALL, border = 5)

        # create buttons and put them buttonsizer, add buttonsizer to topsizer
        self.resetbutton = wx.Button(panel, label = "Reset", size = (100,30))
        self.okbutton = wx.Button(panel, label = "Ok", size = (100,30))
        self.cancelbutton = wx.Button(panel, label = "Cancel", size = (100,30))
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

        buttonSizer.Add(self.resetbutton, flag = wx.ALL, border = 5)
        buttonSizer.Add(self.okbutton, flag = wx.ALL, border = 5)
        buttonSizer.Add(self.cancelbutton, flag = wx.ALL, border = 5)
        topSizer.Add(buttonSizer, flag = wx.ALIGN_RIGHT)

        panel.SetSizer(topSizer)
        self.Centre()
        self.Layout()

if __name__ == '__main__':
    app = wx.App()
    frame = advWindow(None)
    frame.Show()
    app.MainLoop()

