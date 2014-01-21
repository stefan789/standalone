import wx

class advCoilPanel(wx.Panel):
    def __init__(self, parent):
        self.panel = wx.Panel(parent)
        t = wx.StaticText(self.panel, -1, "Text in Panel 1")
