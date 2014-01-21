import wx
import collections
import mainWindow
import advWindow

class initLayout(wx.Frame):

    def __init__(self):
        self.createMainWindow()
        

    def __initMenu__(self):
        self.menubar = wx.MenuBar()
        filem = wx.Menu()
        editm = wx.Menu()
        helpm = wx.Menu()

        self.menubar.Append(filem, '&File')
        self.menubar.Append(editm, '&Edit')
        self.menubar.Append(helpm, '&Help')
        self.SetMenuBar(self.menubar)

    def createMainWindow(self):
        self.mainwin = mainWindow.mainWindow(self)
        self.mainwin.Show()

    def createAdvWindow(self, coils):
        self.advwin = advWindow.advWindow(self.mainwin, coils)
            

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = initLayout()
    frame.mainwin.Show()
    app.MainLoop()
