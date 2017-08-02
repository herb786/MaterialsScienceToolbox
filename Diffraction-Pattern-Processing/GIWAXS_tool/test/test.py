#!/usr/bin/env python

import unittest
import wx
import sys, os
import numpy as np
from numpy.random import random
import matplotlib.pyplot as plt

cwd = os.getcwd()
upFolder = os.path.dirname(cwd)
sys.path.append(upFolder)
from MockObject import MockToolBar
from src.AppParameters import AppParameters as par
from src.AppMainWindow import AppMainWindow
from src.EventHandle import EventHandle
from src.ImageCorrector import *
from src.Integrator import *
from src.Comparator import *
from src.PlotterUI import *
from src.ProcessedDataBuilder import *


class TestAppMainWindow(unittest.TestCase):
    def setUp(self):
        self.app = wx.App()
        self.appMainWindow = AppMainWindow(None,-1,'test', par)
        self.EventHandle = EventHandle(self.appMainWindow, par)
              
    def tearDown(self):
        self.appMainWindow = None
     
            
    def testWidgetObject(self):
        self.assertIsInstance(self.appMainWindow.appMenuBar,wx._core.MenuBar, "It is not a Menu Bar")
        self.assertIsInstance(self.appMainWindow.appFileMenu,wx._core.Menu, "It is not a Menu")
        self.assertIsInstance(self.appMainWindow.appToolBar,wx._core.ToolBar, "It is not a Tool Bar")
        self.assertIsInstance(self.appMainWindow.lowerLimitColorMapSlider,wx._core.Slider, "It is not a slider")
        self.assertIsInstance(self.appMainWindow.upperLimitColorMapSlider,wx._core.Slider, "It is not a slider")
        
      
    def testOpenFileMethod(self):
        self.assertNotEqual(par.folderName,'')
        self.assertEqual(par.myFiles,[])
        self.assertEqual(par.imageContainer,{})
        self.appMainWindow.horizontalPixelOnDetectorEdt.SetValue('800')
        self.appMainWindow.verticalPixelOnDetectorEdt.SetValue('800')
        # Double click on the image and select a working area around the click location
        print self.EventHandle.onOpen(wx.EVT_TOOL)
        self.assertNotEqual(par.myFiles,[])
        self.assertNotEqual(par.imageContainer,{})
        self.assertFalse(self.appMainWindow.verticalPixelOnDetectorEdt.IsEnabled(), "It is enabled")
        self.assertFalse(self.appMainWindow.horizontalPixelOnDetectorEdt.IsEnabled(), "It is enabled")
        
        
    def testToggleButton(self):
        self.appMainWindow.plotQzQxyBtn.SetValue(True)
        self.EventHandle.onToggleClick(wx.EVT_BUTTON)
        self.assertEqual(self.appMainWindow.plotQzQxyBtn.GetBackgroundColour(),wx.Colour(218, 57, 57, 255))
        self.appMainWindow.plotQxzQxyBtn.SetValue(True)
        self.EventHandle.onToggleClick(wx.EVT_BUTTON)
        self.assertEqual(self.appMainWindow.plotQxzQxyBtn.GetBackgroundColour(),wx.Colour(218, 57, 57, 255))


class TestImageCorrectorModule(unittest.TestCase):
    
    def setUp(self):
        self.app = wx.App()
        self.appMainWindow = AppMainWindow(None,-1,'test', par)
        self.singleImage = np.random.random((20,20))
        self.regularXAxis = np.linspace(0., 1., 20)
        self.regularYAxis = np.linspace(0., 1., 20)
        self.stopX = np.array([0,5,5,10,10,15,15,19])
        self.stopY = np.array([10,19,0,10])        
        
              
    def tearDown(self):
        self.appMainWindow = None
        
    def testGetRegularAndInitialAxis(self):
        wavevector = 5
        pixelDensity = 172.
        incidentAngle = 0.5
        sampleToDetectorDistance = 1200
        xDirectBeam = 100
        yDirectBeam = 100 
        dimensionXY = (200, 200)
        initialXYAxis, initialXZAxis, initialZAxis, regularXYAxis, regularXZAxis, regularZAxis, stopX, stopY = \
            getRegularAndInitialAxis(wavevector, incidentAngle, pixelDensity, sampleToDetectorDistance, xDirectBeam, yDirectBeam, dimensionXY)
        self.assertIsInstance(initialXYAxis,np.ndarray)
        self.assertEqual(initialXYAxis.shape[0], 200*200)
        self.assertIsInstance(initialXZAxis,np.ndarray)
        self.assertEqual(initialXZAxis.shape[0], 200*200)
        self.assertIsInstance(initialZAxis,np.ndarray)
        self.assertEqual(initialZAxis.shape[0], 200*200)
        self.assertIsInstance(regularXYAxis,np.ndarray)
        self.assertEqual(regularXYAxis.shape[0], 200)
        self.assertIsInstance(regularXZAxis,np.ndarray)
        self.assertEqual(regularXZAxis.shape[0], 100)
        self.assertIsInstance(regularZAxis,np.ndarray)
        self.assertEqual(regularZAxis.shape[0], 100)
        self.assertIsInstance(stopX,np.ndarray)
        self.assertEqual(stopX.shape[0], 8)
        self.assertIsInstance(stopY,np.ndarray)
        self.assertEqual(stopY.shape[0], 4)
        
    def testCreateEigthPatches(self):
        imageBundle = {}
        imageBundle[1] = np.random.random((100,100))
        initialXGrid = np.ravel(2*np.random.random((100,100)))    
        regularXAxis = np.linspace(-10, 10, 100)
        initialZGrid = np.ravel(3*np.random.random((100,100)))
        regularZAxis = np.linspace(-10, 10, 100)
        stopX = np.array([0,25,25,50,50,75,75,99])
        stopY = np.array([50,99,0,50])
        imagePatch, gridPatch = createEigthPatches(imageBundle, initialXGrid, regularXAxis, initialZGrid, regularZAxis, stopX, stopY)        
        self.assertIsInstance(imagePatch, dict)
        self.assertNotEqual(imagePatch['80000'].shape, 100)
        self.assertIsInstance(gridPatch, dict)
        self.assertNotEqual(gridPatch['80000'].shape, 100)
        
    def testInterpolationOnRegularGrid(self):
        imagePatch = {}
        gridPatch = {}      
        srcA = np.ravel(np.transpose(np.array([[0.23,0.34],[0.23,0.34],[0.23,0.34],[0.23,0.34],[0.23,0.34]])))
        srcB = np.ravel(np.transpose(np.array([[0.64,0.84],[0.64,0.84],[0.64,0.84],[0.64,0.84],[0.64,0.84]])))
        gridPatch['10000'] = np.array([[0.13,0.24]*5, srcA])
        gridPatch['20000'] = np.array([[0.34,0.44]*5, srcA])
        gridPatch['30000'] = np.array([[0.53,0.64]*5, srcA])
        gridPatch['40000'] = np.array([[0.87,0.94]*5, srcA])
        gridPatch['50000'] = np.array([[0.13,0.24]*5, srcB])
        gridPatch['60000'] = np.array([[0.34,0.44]*5, srcB])
        gridPatch['70000'] = np.array([[0.53,0.64]*5, srcB])
        gridPatch['80000'] = np.array([[0.87,0.94]*5, srcB])
        imagePatch['10000'] = random(10)
        imagePatch['20000'] = random(10)
        imagePatch['30000'] = random(10)
        imagePatch['40000'] = random(10)
        imagePatch['50000'] = random(10)
        imagePatch['60000'] = random(10)
        imagePatch['70000'] = random(10)
        imagePatch['80000'] = random(10)
        interpolationOnRegularGrid(gridPatch, imagePatch, self.regularXAxis, self.regularYAxis, self.stopX, self.stopY, 1)
        
    def testPreparePlot(self):
        regularXAxis = np.linspace(0., 1., 20)
        regularYAxis = np.linspace(0., 1., 20)
        stopX = np.array([0,5,5,10,10,15,15,19])
        stopY = np.array([10,19,0,10])
        preparePlot(self.appMainWindow, par, self.regularXAxis, self.regularYAxis, self.stopX, self.stopY, self.singleImage, False)
        plt.show()
        
    def testSaveImageAndData(self):
        par.myFiles = ['test']
        plt.imshow(self.singleImage)
        saveImageAndData(par, 0, self.singleImage, '_myImage')
    
      
class TestPlotAnalysis(unittest.TestCase):

    def setUp(self):
        self.singleImage1 = np.random.random((20,20))
        self.singleImage2 = np.random.random((20,20))        
        self.regularAxis = np.linspace(0., 20., 20)       
                    
    def tearDown(self):
        self.appMainWindow = None
        
    def testPlotIntegration(self):
        par.imageQxyQz[1] = self.singleImage1
        par.imageQxyQxz[1] = self.singleImage2    
        par.axisQxy = self.regularAxis 
        par.axisQxz = self.regularAxis
        par.axisQz = self.regularAxis
        par.lowerBoundIntegration = 5.
        par.upperBoundIntegration = 10.       
        integrationNumber = 4
        plotIntegration(par, integrationNumber)
        
    def testPrepareGraphPair(self):
        par.imageQxyQz[1] = self.singleImage1
        par.imageQxyQxz[1] = self.singleImage2   
        par.axisQxy = self.regularAxis 
        par.axisQxz = self.regularAxis
        par.axisQz = self.regularAxis
        labelXAxis = r'$q_{xy}$'
        prepareGraphPair(par.imageQxyQz[1], par.imageQxyQxz[1], par.axisQxy, par.axisQxy, labelXAxis)
        plt.show()
        

class TestEventRoutine(unittest.TestCase):

    def setUp(self):
        self.singleImage1 = np.random.random((20,20))
        self.singleImage2 = np.random.random((20,20))
        self.singleImage3 = np.random.random((20,20))
        self.regularAxis = np.linspace(0., 20., 20)       
                    
    def tearDown(self):
        self.appMainWindow = None
        
    def testSaveIntegrationData(self):
        par.myFiles = ['file1', 'file2', 'file3']
        par.imageContainer = { 1:self.singleImage1, 2:self.singleImage2, 3:self.singleImage3 }
        par.imageQxyQz = { 1:self.singleImage1, 2:self.singleImage2, 3:self.singleImage3 }
        par.imageQxyQxz = { 1:self.singleImage1, 2:self.singleImage2, 3:self.singleImage3 }  
        par.axisQxy = self.regularAxis 
        par.axisQxz = self.regularAxis
        par.axisQz = self.regularAxis
        folderpath = os.getcwd()
        saveIntegrationData(par, 2, folderpath)
        
             
def suite():
    suite = unittest.TestSuite()
    # suite.addTest(TestAppMainWindow('testWidgetObject'))
    # suite.addTest(TestAppMainWindow('testToggleButton'))
    # suite.addTest(TestImageCorrectorModule('testGetRegularAndInitialAxis'))
    # suite.addTest(TestImageCorrectorModule('testCreateEigthPatches'))
    # suite.addTest(TestImageCorrectorModule('testInterpolationOnRegularGrid'))
    # suite.addTest(TestImageCorrectorModule('testPreparePlot'))
    # suite.addTest(TestImageCorrectorModule('testSaveImageAndData'))
    # suite.addTest(TestPlotAnalysis('testPlotIntegration'))
    # suite.addTest(TestPlotAnalysis('testPrepareGraphPair'))
    suite.addTest(TestEventRoutine('testSaveIntegrationData'))
    return suite
        

if __name__ == '__main__':
    # unittest.main()
    runner = unittest.TextTestRunner(stream=sys.stdout)
    testSuite = suite()
    runner.run(testSuite)
    
