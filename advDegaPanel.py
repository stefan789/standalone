import wx
import collections

class advDegaPanel(wx.Panel):
    def __init__(self, parent):
        self.panel = wx.Panel(parent)

        # topsizer contains bagSizer, bagsizer the other widgets
        topSizer = wx.BoxSizer(wx.VERTICAL)
        bagSizer = wx.GridBagSizer(hgap = 5, vgap = 5)

        # device section 
        labelDev = wx.StaticText(self.panel, -1, "Device")
        deviceList = ["Dev0", "Dev1", "Dev2"]
        self.inputDev = wx.ComboBox(self.panel, -1, "", wx.DefaultPosition, (200,-1), deviceList, wx.CB_DROPDOWN)
        bagSizer.Add((-1,10), pos = (0,0))
        bagSizer.Add(labelDev, pos = (1,0), flag = wx.ALIGN_CENTER_VERTICAL, border = 5)
        bagSizer.Add(self.inputDev, pos = (1,1), flag = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, border = 5)

        # offset section
        labelOffset = wx.StaticText(self.panel, -1, "Offset")
        self.textOffset = wx.TextCtrl(self.panel)

        bagSizer.Add(labelOffset, pos = (2,0), flag = wx.ALIGN_CENTER_VERTICAL, border = 5)
        bagSizer.Add(self.textOffset, pos = (2,1), flag = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, border = 5)


        bagSizer.Add(wx.StaticLine(self.panel, -1, (25,-1), (-1,-1)), pos = (3,0), span=(1,2), flag = wx.EXPAND|wx.ALL, border = 10)

        # Coil selector
        labelCoil = wx.StaticText(self.panel, -1, "Coil")
        self.coilselector = wx.ComboBox(self.panel, -1, "", wx.DefaultPosition,
                (200,-1), "", wx.CB_READONLY)

        bagSizer.Add(labelCoil, pos = (4,0), flag = wx.ALIGN_CENTER_VERTICAL, border = 5)
        bagSizer.Add(self.coilselector, pos = (4,1), flag = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, border = 5)

        # amplitude
        labelAmp = wx.StaticText(self.panel, -1, "Amplitude")
        self.textAmp = wx.TextCtrl(self.panel)

        bagSizer.Add(labelAmp, pos = (5,0), flag = wx.ALIGN_CENTER_VERTICAL, border = 5)
        bagSizer.Add(self.textAmp, pos = (5,1), flag = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, border = 5)
        
        # frequency
        labelFreq = wx.StaticText(self.panel, -1, "Frequency")
        self.textFreq = wx.TextCtrl(self.panel)

        bagSizer.Add(labelFreq, pos = (6,0), flag = wx.ALIGN_CENTER_VERTICAL, border = 5)
        bagSizer.Add(self.textFreq, pos = (6,1), flag = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, border = 5)

        # duration
        labelDur = wx.StaticText(self.panel, -1, "Duration")
        self.textDur = wx.TextCtrl(self.panel)

        bagSizer.Add(labelDur, pos = (7,0), flag = wx.ALIGN_CENTER_VERTICAL, border = 5)
        bagSizer.Add(self.textDur, pos = (7,1), flag = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, border = 5)

        # keeptime
        labelKeep = wx.StaticText(self.panel, -1, "Keeptime")
        self.textKeep = wx.TextCtrl(self.panel)

        bagSizer.Add(labelKeep, pos = (8,0), flag = wx.ALIGN_CENTER_VERTICAL, border = 5)
        bagSizer.Add(self.textKeep, pos = (8,1), flag = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, border = 5)

        #add everything to topsizer and set it as panel sizer
        topSizer.Add(bagSizer, flag = wx.EXPAND|wx.ALL, border = 5)
        self.panel.SetSizer(topSizer)
