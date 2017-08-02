#!/usr/bin/env python

import wx
import sys, os
from src.EventHandle import EventHandle

class MockToolBar(wx.Frame):

    def __init__(self, parent, id, title, par):
        wx.Frame.__init__(self, parent, id, title)
        self.par = par

        self.appMenuBar = wx.MenuBar()
        self.appFileMenu = wx.Menu()
        self.appOpenMenu = self.appFileMenu.Append(wx.ID_OPEN,'&Open')
        self.appQuitMenu = self.appFileMenu.Append(wx.ID_EXIT,'&Quit')
        self.appMenuBar.Append(self.appFileMenu,'&File')
        
        self.appToolBar = self.CreateToolBar()
        icon = wx.ArtProvider.GetBitmap(wx.ART_TIP,wx.ART_TOOLBAR,(32,32))
        self.appOpenTool = self.appToolBar.AddSimpleTool(-1,icon,'Open')
        self.appQuitTool = self.appToolBar.AddSimpleTool(-1,icon,'Quit')
        self.appSaveTool = self.appToolBar.AddSimpleTool(-1,icon,'Save')
        
        self.SetMenuBar(self.appMenuBar)
        self.appToolBar.Realize()
        
        self.eventHandle = EventHandle(self, self.par)
        self.Bind(wx.EVT_MENU, self.eventHandle.onQuit, self.appQuitMenu)
        self.Bind(wx.EVT_TOOL, self.eventHandle.onQuit, self.appQuitTool)
        self.Bind(wx.EVT_MENU, self.eventHandle.onOpen, self.appOpenMenu)
        self.Bind(wx.EVT_TOOL, self.eventHandle.onOpen, self.appOpenTool)
        
    def OnCloseWindow(self, event):
        app.keepGoing = False
        self.Destroy()