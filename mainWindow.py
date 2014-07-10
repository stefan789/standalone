import wx

class mainWindow(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, None, wx.ID_ANY, 'Degaussing Tool', pos=(0,0),
                size=(800,600))

#        self.__initMenu__()

        self.panel = wx.Panel(self, wx.ID_ANY)
#        self.advwin = advWindow.advWindow(self)

        topSizer = wx.BoxSizer(wx.VERTICAL)
        # outerbag sizer for 2 columns 'Control' and 'Progress'
        outerbagSizer = wx.GridBagSizer(hgap = 5, vgap = 5)
        controlbbox = wx.StaticBox(self.panel, label = 'Control')
        controlbox = wx.StaticBoxSizer(controlbbox, wx.VERTICAL)
        progressbbox = wx.StaticBox(self.panel, label = 'Progress')
        progressbox = wx.StaticBoxSizer(progressbbox, wx.VERTICAL)

        # two GridBagSizers for control and progess with two spacers in (0,0)
        controlbag = wx.GridBagSizer(hgap = 5, vgap = 5)
        progressbag = wx.GridBagSizer(hgap = 5, vgap = 5)
        controlbag.Add((380,100), pos = (0,0), flag = wx.EXPAND)
        progressbag.Add((380,165), pos = (0,0), flag = wx.EXPAND)

        # create start button and add them to controlbag
        startbuttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.startbtn = wx.Button(self.panel, label = 'Start', size = (200,123))
        startbuttonSizer.Add((-1,-1), wx.ALIGN_LEFT|wx.EXPAND)
        startbuttonSizer.Add(self.startbtn)
        startbuttonSizer.Add((-1,-1), wx.ALIGN_RIGHT|wx.EXPAND)
        controlbag.Add(startbuttonSizer, pos = (1,0), flag = wx.EXPAND)
        controlbag.AddGrowableRow(1,0)

        controlbag.Add((-1,40), pos = (2,0), flag = wx.EXPAND)

        # create abort button and add them to controlbag
        abortbuttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.abortbtn = wx.Button(self.panel, label = 'Abort', size = (200,123))
        abortbuttonSizer.Add((-1,-1), wx.ALIGN_LEFT|wx.EXPAND)
        abortbuttonSizer.Add(self.abortbtn,flag = wx.EXPAND)
        abortbuttonSizer.Add((-1,-1), wx.ALIGN_RIGHT|wx.EXPAND)
        controlbag.Add(abortbuttonSizer, pos = (3,0), flag = wx.EXPAND)
        controlbag.AddGrowableRow(3)
        controlbag.Add((-1,35), pos = (4,0))

        # number of runs
        runNrSizer = wx.BoxSizer(wx.HORIZONTAL)
        runLabel = wx.StaticText(self.panel, label = "Nr of runs")
        self.runNrCtrl = wx.SpinCtrl(self.panel, value = '1', size=(60,-1), min=1, max=5)
        runNrSizer.Add((-1,-1), wx.ALIGN_LEFT|wx.EXPAND)
        runNrSizer.Add(runLabel, flag=wx.ALIGN_CENTER)
        runNrSizer.Add((30,-1))
        runNrSizer.Add(self.runNrCtrl, flag=wx.ALIGN_CENTER)
        runNrSizer.Add((-1,-1), wx.ALIGN_RIGHT|wx.EXPAND)
        controlbag.Add(runNrSizer, pos=(5,0), flag = wx.ALIGN_LEFT|wx.EXPAND)
        controlbag.Add((-1,37), pos=(6,0))

        # create advanced settings button and add to advbuttonsizer then add to controlbag
        advbuttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.advbtn = wx.Button(self.panel, label = "advanced settings", size = (200,30))
        advbuttonSizer.Add((-1,-1), wx.EXPAND)
        advbuttonSizer.Add(self.advbtn, wx.ALIGN_LEFT)
        advbuttonSizer.Add((-1,-1), wx.EXPAND)
        controlbag.Add(advbuttonSizer, pos=(7,0), flag = wx.ALIGN_LEFT|wx.EXPAND)

        
        # create overall progress bar and add to progressbag
        self.overalllabel = wx.StaticText(self.panel, wx.ID_ANY, "Progress", size=(-1,-1), style=wx.ALIGN_BOTTOM)
        progressbag.Add((-1,45), pos = (1,0))
        progressbag.Add(self.overalllabel, pos = (2,0), flag = wx.ALIGN_LEFT|wx.EXPAND)
        progressbag.AddGrowableRow(1)
        self.overallbar = wx.Gauge(self.panel, range = 100, size = (-1,30))
        progressbag.Add(self.overallbar, pos = (3,0), flag = wx.EXPAND)

        # spacer in between progress bars
        progressbag.Add((-1,-1), pos = (4,0), flag = wx.EXPAND)
        # create overall progress bar and add to progressbag
        progressbag.Add((-1,-1), pos = (5,0), flag = wx.ALIGN_LEFT)
        progressbag.AddGrowableRow(4)
        progressbag.Add((-1,-1), pos = (6,0), flag = wx.EXPAND)
        progressbag.Add((-1,-1), pos = (7,0))
        progressbag.Add((-1,108), pos = (8,0))

        self.statusLabel = wx.StaticText(self.panel, wx.ID_ANY, "Status")
        progressbag.Add(self.statusLabel, pos = (9,0))
        self.status = wx.TextCtrl(self.panel,5, "", wx.Point(20,20),
                wx.Size(380,90),
                wx.TE_MULTILINE | wx.TE_READONLY)
        progressbag.Add(self.status, pos = (10,0))
        self.saveStatus = wx.CheckBox(self.panel, label = "Save status to log file")
        self.saveStatus.SetValue(False)
        progressbag.Add(self.saveStatus, pos = (11,0))


        # add them to their boxes
        controlbox.Add(controlbag, wx.EXPAND)
        progressbox.Add(progressbag, wx.EXPAND)
        
        # add boxes to outerbag
        outerbagSizer.Add(controlbox, pos = (0,0), flag=wx.ALIGN_TOP, border = 5)
        outerbagSizer.Add(progressbox, pos = (0,1), flag=wx.ALIGN_TOP, border = 5)

        # add outerbag to top
        topSizer.Add(outerbagSizer, wx.EXPAND)
        self.panel.SetSizer(topSizer)
        #self.SetSizeHints(800, 600, 800, 600)

        self.Centre()

if __name__ == '__main__':
    app = wx.App()
    frame = mainWindow(None)
    frame.Show()
    app.MainLoop()
