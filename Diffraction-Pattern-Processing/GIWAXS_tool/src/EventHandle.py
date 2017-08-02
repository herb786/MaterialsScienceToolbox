#!/usr/bin/env python

import wx
from AppParameters import AppParameters as par
from ImageLoader import imageLoader
from ImageCorrector import *
from Integrator import *
from Comparator import *
from PlotterUI import *
from ProcessedDataBuilder import *

class EventHandle():

    def __init__(self, appMainWindow, par):
        self.appMainWindow = appMainWindow
        self.par = par
        
        
    def onQuit(self, event):
        self.appMainWindow.Close()
        
        
    def onOpen(self, event):
        dialog = wx.FileDialog(self.appMainWindow,"Choose a file", self.par.folderName, '',"TIFF files (*.tif;*.tiff)|*.tif;*.tiff",wx.FD_MULTIPLE)
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetFilenames()
            #print self.appMainWindow.filename
            if filename[0].endswith('.tiff'):
                self.par.myFiles = [a.replace('.tiff','') for a in filename]
            if filename[0].endswith('.tif'):
                self.par.myFiles = [a.replace('.tif','') for a in filename]
            self.appMainWindow.verticalPixelOnDetectorEdt.Enable()
            self.appMainWindow.horizontalPixelOnDetectorEdt.Enable()
            imageLoader(self.appMainWindow, self.par, filename)
            
            
    def focusOnIncidentAlpha(self, event):
        self.appMainWindow.incidentAlphaEdt.SetFocus()
        self.appMainWindow.incidentAlphaEdt.SetSelection(-1,-1)
    
    
    def focusOnSampleToDetectorDistance(self, event):
        self.appMainWindow.sampleToDetectorDistanceEdt.SetFocus()
        self.appMainWindow.sampleToDetectorDistanceEdt.SetSelection(-1,-1)
            
            
    def focusOnRunButton(self, event):
        self.appMainWindow.plotQzQxyBtn.SetValue(True)
        self.appMainWindow.plotQzQxyBtn.SetBackgroundColour('#DA3939')
        self.appMainWindow.plotQzQxyBtn.SetForegroundColour('white')
        self.appMainWindow.runBtn.SetFocus()
        
        
    def onToggleClick(self,event):
    
        if self.appMainWindow.plotQzQxyBtn.GetValue():
            self.appMainWindow.plotQzQxyBtn.SetBackgroundColour('#DA3939')
            self.appMainWindow.plotQzQxyBtn.SetForegroundColour('white')
        else:
            self.appMainWindow.plotQzQxyBtn.SetBackgroundColour((240, 240, 240, 255))
            self.appMainWindow.plotQzQxyBtn.SetForegroundColour('black')
            
        if self.appMainWindow.plotQxzQxyBtn.GetValue():
            self.appMainWindow.plotQxzQxyBtn.SetBackgroundColour('#DA3939')
            self.appMainWindow.plotQxzQxyBtn.SetForegroundColour('white')
        else:
            self.appMainWindow.plotQxzQxyBtn.SetBackgroundColour((240, 240, 240, 255))
            self.appMainWindow.plotQxzQxyBtn.SetForegroundColour('black')
            
    
    def onRunButtonClick(self, event):
        a = self.appMainWindow.plotQzQxyBtn.GetValue()
        b = self.appMainWindow.plotQxzQxyBtn.GetValue()
        if ((a and not b) or (not a and b)):
            imageCorrector(self.appMainWindow, self.par)
            
    
    def onIntegrateButtonClick(self, event):
        integrationRoutine(self.appMainWindow, self.par)
    
    
    def onCompareButtonClick(self, event):
        comparatorRoutine(self.appMainWindow, self.par)
        
        
    def onPlotAgainButtonClick(self, event):
        plotAgainRoutine(self.appMainWindow, self.par)

        
    def onChangeUpperLimitColorMapSlider(self, event):
        changeLimitColorMapSlider(self.appMainWindow, self.par, True)

        
    def onChangeLowerLimitColorMapSlider(self, event):
        changeLimitColorMapSlider(self.appMainWindow, self.par, False)

        
    def OnSave(self,event):

        saveFileDialog = wx.FileDialog(self.parent, 
            "Save DAT file", "", 
            defaultFile=self.par.myFiles[0],
            wildcard="DAT files (*.dat)|*.dat",
            style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT )
            
        if saveFileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed idea...
        #print saveFileDialog.GetDirectory()
        #There is file output for each button. Filename is created from the orginal one and the integration
        folderpath = saveFileDialog.GetDirectory()
        
        integrateOverQxzKeepQxyBtn = self.appMainWindow.integrateOverQxzKeepQxyBtn.GetValue()
        integrateOverQzKeepQxyBtn = self.appMainWindow.integrateOverQzKeepQxyBtn.GetValue()
        integrateOverQxyKeepQzBtn = self.appMainWindow.integrateOverQxyKeepQzBtn.GetValue()
        integrateOverQxyKeepQxzBtn = self.appMainWindow.integrateOverQxyKeepQxzBtn.GetValue()
        
        if (integrateOverQxzKeepQxyBtn):
            saveIntegrationData(self.par, 1, folderpath)
        
        if (integrateOverQzKeepQxyBtn):
            saveIntegrationData(self.par, 2, folderpath)
            
        if (integrateOverQxyKeepQzBtn):
            saveIntegrationData(self.par, 3, folderpath)
            
        if (integrateOverQxyKeepQxzBtn):
            saveIntegrationData(self.par, 4, folderpath)
        
            
            
    