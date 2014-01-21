import wx
import advDegaPanel
import advCoilPanel

class advWindow(wx.Frame):
    def __init__(self, parent, coils):
        wx.Frame.__init__(self, parent, wx.ID_ANY, "Advanced Settings", size =(400,300))
        self.SetSizeHints(400,330,800,600)
        panel = wx.Panel(self, wx.ID_ANY)

        topSizer = wx.BoxSizer(wx.VERTICAL)
        
        nb = wx.Notebook(panel)
        self.degaP = advDegaPanel.advDegaPanel(nb, coils)
        nb.AddPage(self.degaP.panel, "Parameters  ")
        self.coilP = advCoilPanel.advCoilPanel(nb)
        nb.AddPage(self.coilP.panel, "Coils  ")

        topSizer.Add(nb, flag = wx.EXPAND|wx.ALL, border = 5)

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
    import json
    import collections
    app = wx.PySimpleApp()
    with open("coils.dict", "r") as f:
        coils = json.loads(f.read(), object_pairs_hook=collections.OrderedDict)

    frame = advWindow(None, coils)
    frame.Show()
    app.MainLoop()

