import wx
import initLayout
import control

app = wx.PySimpleApp()
frame = initLayout.initLayout()
controller = control.control(frame)
app.MainLoop()
