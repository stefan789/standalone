import wx

class advCoilPanel(wx.Panel):
    def __init__(self, parent):
        self.panel = wx.Panel(parent)

        # topsizer contains bagSizer, bagsizer the other widgets
        topSizer = wx.BoxSizer(wx.VERTICAL)

        outerbagsizer = wx.GridBagSizer(hgap = 5, vgap = 5)

        coilbbox = wx.StaticBox(self.panel, label="Choose coil configuration")
        coilbox = wx.StaticBoxSizer(coilbbox, wx.VERTICAL)
        
        bagSizer = wx.GridBagSizer(hgap = 5, vgap = 10)

        self.rb1 = wx.RadioButton(self.panel, style = wx.RB_GROUP)
        self.rb2 = wx.RadioButton(self.panel)
        self.rb3 = wx.RadioButton(self.panel)
        self.rb4 = wx.RadioButton(self.panel)
        self.rb5 = wx.RadioButton(self.panel)

        self.labelrb1 = wx.StaticText(self.panel, label = "Inner coils")
        self.labelrb2 = wx.StaticText(self.panel, label = "Middle coils")
        self.labelrb3 = wx.StaticText(self.panel, label = "Outer coils")
        self.labelrb4 = wx.StaticText(self.panel, label = "All coils")
        self.labelrb5 = wx.StaticText(self.panel, label = "Custom coil file")
        self.text = wx.TextCtrl(self.panel)

        bagSizer.Add((340,-1), pos = (0,1))

        bagSizer.Add(self.rb1, pos = (1,0))
        bagSizer.Add(self.rb2, pos = (2,0))
        bagSizer.Add(self.rb3, pos = (3,0))
        bagSizer.Add(self.rb4, pos = (4,0))
        bagSizer.Add(self.rb5, pos = (5,0))


        bagSizer.Add(self.labelrb1, pos = (1,1), flag = wx.ALIGN_CENTER_VERTICAL)
        bagSizer.Add(self.labelrb2, pos = (2,1), flag = wx.ALIGN_CENTER_VERTICAL)
        bagSizer.Add(self.labelrb3, pos = (3,1), flag = wx.ALIGN_CENTER_VERTICAL)
        bagSizer.Add(self.labelrb4, pos = (4,1), flag = wx.ALIGN_CENTER_VERTICAL)
        bagSizer.Add(self.labelrb5, pos = (5,1), flag = wx.ALIGN_CENTER_VERTICAL)
        bagSizer.Add(self.text, pos = (6,1), flag =
                wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        bagSizer.Add((-1,1), pos = (7,1))

        coilbox.Add(bagSizer, wx.EXPAND)

        outerbagsizer.Add((-1, 5), pos = (0,0))
        outerbagsizer.Add(coilbox, pos = (1,0), flag = wx.EXPAND)
        outerbagsizer.Add((-1, 5), pos = (2,0))
        topSizer.Add(outerbagsizer, wx.EXPAND)
        self.panel.SetSizer(topSizer)

        self.text.Hide()


        
