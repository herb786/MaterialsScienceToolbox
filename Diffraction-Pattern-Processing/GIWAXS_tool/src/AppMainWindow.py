#!/usr/bin/env python

import wx
import wx.lib.buttons as btn
from EventHandle import EventHandle

class AppMainWindow(wx.Frame):
    def __init__(self, parent, id, title, par):
        #wx.Frame.__init__(self,parent,id,title,style = wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER)
        wx.Frame.__init__(self,parent,id,title)
        #self.child = ChildFrame(self)
        self.par = par
        
        
        #My Menubar
        self.appMenuBar = wx.MenuBar()
        self.appFileMenu = wx.Menu()
        self.appOpenMenu = self.appFileMenu.Append(wx.ID_OPEN,'&Open')
        self.appQuitMenu = self.appFileMenu.Append(wx.ID_EXIT,'&Quit')
        self.appMenuBar.Append(self.appFileMenu,'&File')
        
        
        #My Toolbar
        self.appToolBar = self.CreateToolBar()
        
        openIcon = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN,wx.ART_TOOLBAR,(32,32))
        self.appOpenTool = self.appToolBar.AddSimpleTool(-1,openIcon,'Open')
        
        quitIcon = wx.ArtProvider.GetBitmap(wx.ART_DELETE,wx.ART_TOOLBAR,(32,32))
        self.appQuitTool = self.appToolBar.AddSimpleTool(-1,quitIcon,'Quit')
        
        saveIcon = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE,wx.ART_TOOLBAR,(32,32))
        self.appSaveTool = self.appToolBar.AddSimpleTool(-1,saveIcon,'Save')

        
        #My Labels
        self.emptyTxt = wx.StaticText(self,-1,label=u'')
        
        self.wavelengthTxt = wx.StaticText(self,-1,label=u'Wavelength')
        self.wavelengthTxt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.incidentAlphaTxt = wx.StaticText(self,-1,label=u'Incidence Angle')
        self.incidentAlphaTxt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.sampleToDetectorDistanceTxt = wx.StaticText(self,-1,label=u'SDD')
        self.sampleToDetectorDistanceTxt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.verticalPixelOnDetectorTxt = wx.StaticText(self,-1,label=u'Hor')
        self.verticalPixelOnDetectorTxt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.horizontalPixelOnDetectorTxt = wx.StaticText(self,-1,label=u'Ver')
        self.horizontalPixelOnDetectorTxt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.cropSizeTxt = wx.StaticText(self,-1,label=u'Size')
        self.cropSizeTxt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.upperLimitColorMapTxt = wx.StaticText(self,-1,label=u'Max')
        self.upperLimitColorMapTxt.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.lowerLimitColorMapTxt = wx.StaticText(self,-1,label=u'Min')
        self.lowerLimitColorMapTxt.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.lowerLimitXAxisTxt = wx.StaticText(self,-1,label=u'X-axis Min')
        self.lowerLimitXAxisTxt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.lowerLimitYAxisTxt = wx.StaticText(self,-1,label=u'Y-axis Min')
        self.lowerLimitYAxisTxt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.upperLimitXAxisTxt = wx.StaticText(self,-1,label=u'X-axis Max')
        self.upperLimitXAxisTxt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.upperLimitYAxisTxt = wx.StaticText(self,-1,label=u'Y-axis Max')
        self.upperLimitYAxisTxt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.borderThicknessTxt = wx.StaticText(self,-1,label=u'Borderline')
        self.borderThicknessTxt.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.tickFontSizeTxt = wx.StaticText(self,-1,label=u'Font size')
        self.tickFontSizeTxt.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.tickLengthTxt = wx.StaticText(self,-1,label=u'Tick length')
        self.tickLengthTxt.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.tickWidthTxt = wx.StaticText(self,-1,label=u'Tick width')
        self.tickWidthTxt.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.densityPixelTxt = wx.StaticText(self,-1,label=u'Pixel')
        self.densityPixelTxt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.lowerLimitQAxisTxt = wx.StaticText(self,-1,label=u'q_inf')
        self.lowerLimitQAxisTxt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.upperLimitQAxisTxt = wx.StaticText(self,-1,label=u'q_sup')
        self.upperLimitQAxisTxt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        
        #My buttons
        self.runBtn = wx.Button(self,-1,label='RUN',size=(100,50))
        self.runBtn.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.integrateBtn = wx.Button(self,-1,label='Plot',size=(100,50))
        self.integrateBtn.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.integrateOverQzKeepQxyBtn = wx.ToggleButton(self,-1,label='QZ(I vs. QXY)')
        self.integrateOverQxyKeepQxzBtn = wx.ToggleButton(self,-1,label='QXY(I vs. QXZ)')
        self.integrateOverQxzKeepQxyBtn = wx.ToggleButton(self,-1,label='QXZ(I vs. QXY)')
        self.integrateOverQxyKeepQzBtn = wx.ToggleButton(self,-1,label='QXY(I vs. QZ)')
        
        self.plotQzQxyBtn = btn.GenToggleButton(self,-1,label='I(QZ,QXY)')
        self.plotQxzQxyBtn = btn.GenToggleButton(self,-1,label='I(QXZ,QXY)')
        
        self.logScaleBtn = wx.ToggleButton(self,-1,label='Log Scale')
        
        self.compareBtn = wx.Button(self,-1,label='Compare',size=(100,50))
        self.compareBtn.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.plotAgainBtn = wx.Button(self,-1,label='Replot',size=(100,50))
        self.plotAgainBtn.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        #My Sliders(The current frequency is 100 -the fifth position in the args-)
        self.lowerLimitColorMapSlider = wx.Slider(self,-1,0,0,100, style=wx.SL_VERTICAL, size=(-1,250))
        #self.SlideCMLow.SetTickFreq(10, 1)
        self.upperLimitColorMapSlider = wx.Slider(self,-1,100,0,100, style=wx.SL_VERTICAL, size=(-1,250))
        #self.SlideCMUpp.SetTickFreq(10, 1)
        
        
        #My Inputs
        self.wavelengthEdt = wx.TextCtrl(self,-1,value=u'0.138')
        self.wavelengthEdt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        self.incidentAlphaEdt = wx.TextCtrl(self,-1,value=u'0.3')
        self.incidentAlphaEdt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        self.sampleToDetectorDistanceEdt = wx.TextCtrl(self,-1,value=u'0.1')
        self.sampleToDetectorDistanceEdt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        self.verticalPixelOnDetectorEdt = wx.TextCtrl(self,-1,value=u'NONE')
        self.verticalPixelOnDetectorEdt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        self.horizontalPixelOnDetectorEdt = wx.TextCtrl(self,-1,value=u'NONE')
        self.horizontalPixelOnDetectorEdt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        self.densityPixelEdt = wx.TextCtrl(self,-1,value=u'172')
        self.densityPixelEdt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        self.upperLimitQAxisEdt = wx.TextCtrl(self,-1,value=u'0.0')
        self.upperLimitQAxisEdt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.lowerLimitQAxisEdt = wx.TextCtrl(self,-1,value=u'0.0')
        self.lowerLimitQAxisEdt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        
        #My Plot Inputs
        self.lowerLimitXAxisEdt = wx.TextCtrl(self,-1,value=wx.EmptyString)
        self.lowerLimitXAxisEdt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        self.upperLimitXAxisEdt = wx.TextCtrl(self,-1,value=wx.EmptyString)
        self.upperLimitXAxisEdt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        self.lowerLimitYAxisEdt = wx.TextCtrl(self,-1,value=wx.EmptyString)
        self.lowerLimitYAxisEdt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        self.upperLimitYAxisEdt = wx.TextCtrl(self,-1,value=wx.EmptyString)
        self.upperLimitYAxisEdt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        self.borderThicknessEdt = wx.TextCtrl(self,-1,value='2')
        self.borderThicknessEdt.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        self.tickFontSizeEdt = wx.TextCtrl(self,-1,value='12')
        self.tickFontSizeEdt.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        self.tickLengthEdt = wx.TextCtrl(self,-1,value='6')
        self.tickLengthEdt.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        self.tickWidthEdt = wx.TextCtrl(self,-1,value='2')
        self.tickWidthEdt.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        
        #My Text Output
        self.statusMessageTxt = wx.StaticText(self,-1,label=u'WAIT ORDERS',size=wx.Size(350,50),style=wx.ST_NO_AUTORESIZE)
        self.statusMessageTxt.SetBackgroundColour(wx.BLUE)
        self.statusMessageTxt.SetForegroundColour(wx.WHITE)
        self.statusMessageTxt.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.cropSizeEdt = wx.StaticText(self,-1,label=u'HxV')
        self.cropSizeEdt.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        self.upperLimitColorMapSliderTxt = wx.StaticText(self,-1,label=u'None')
        self.upperLimitColorMapSliderTxt.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.lowerLimitColorMapSliderTxt = wx.StaticText(self,-1,label=u'None')
        self.lowerLimitColorMapSliderTxt.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        
        #My Design
        self.SetMenuBar(self.appMenuBar)
        self.appToolBar.Realize()
        
        # Parameter Box
        self.parametersBox = wx.StaticBox(self,-1,'Parameters')
        self.parametersBox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        parametersBoxSizer =  wx.StaticBoxSizer(self.parametersBox, wx.VERTICAL)
        
        parametersGridSizer = wx.GridBagSizer(hgap=10,vgap=10)
        parametersGridSizer.Add(self.emptyTxt,(0,5),(1,2),wx.EXPAND)
        parametersGridSizer.Add(self.wavelengthTxt,(0,1),(1,2),wx.EXPAND)
        parametersGridSizer.Add(self.wavelengthEdt,(0,3),(1,2),wx.EXPAND)
        parametersGridSizer.Add(self.incidentAlphaTxt,(1,1),(1,2),wx.EXPAND)
        parametersGridSizer.Add(self.incidentAlphaEdt,(1,3),(1,2),wx.EXPAND)
        parametersGridSizer.Add(self.sampleToDetectorDistanceTxt,(2,1),(1,2),wx.EXPAND)
        parametersGridSizer.Add(self.sampleToDetectorDistanceEdt,(2,3),(1,2),wx.EXPAND)
        parametersBoxSizer.Add(parametersGridSizer,-1, flag=wx.EXPAND|wx.ALL, border=10)
        
        
        # Direct Beam Box
        self.directBeamBox = wx.StaticBox(self,-1,'Direct Beam')
        self.directBeamBox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        directBeamBoxSizer =  wx.StaticBoxSizer(self.directBeamBox, wx.VERTICAL)
        
        directBeamGridSizer = wx.GridBagSizer(hgap=10,vgap=10)
        directBeamGridSizer.Add(self.verticalPixelOnDetectorTxt,(0,1),(1,1),wx.EXPAND)
        directBeamGridSizer.Add(self.verticalPixelOnDetectorEdt,(0,2),(1,1),wx.EXPAND)
        directBeamGridSizer.Add(self.horizontalPixelOnDetectorTxt,(0,3),(1,1),wx.EXPAND)
        directBeamGridSizer.Add(self.horizontalPixelOnDetectorEdt,(0,4),(1,1),wx.EXPAND)
        directBeamBoxSizer.Add(directBeamGridSizer,-1, flag=wx.EXPAND|wx.ALL, border=10)
        
        
        # Crop Region Box
        self.cropRegionBox = wx.StaticBox(self,-1,'Selection')
        self.cropRegionBox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        cropRegionBoxSizer =  wx.StaticBoxSizer(self.cropRegionBox, wx.VERTICAL)
        
        cropRegionBoxGridSizer = wx.GridBagSizer(hgap=10,vgap=10)
        cropRegionBoxGridSizer.Add(self.cropSizeTxt,(0,1),(1,1),wx.EXPAND)
        cropRegionBoxGridSizer.Add(self.cropSizeEdt,(0,2),(1,1),wx.EXPAND)
        cropRegionBoxGridSizer.Add(self.densityPixelTxt,(0,5),(1,1),wx.EXPAND)
        cropRegionBoxGridSizer.Add(self.densityPixelEdt,(0,6),(1,1),wx.EXPAND)
        cropRegionBoxSizer.Add(cropRegionBoxGridSizer,-1, flag=wx.EXPAND|wx.ALL, border=10)
        
        
        # Figure Box
        self.figureBox = wx.StaticBox(self,-1,'Figure')
        self.figureBox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        figureBoxSizer =  wx.StaticBoxSizer(self.figureBox, wx.VERTICAL)
        
        figureBoxGridSizer = wx.GridBagSizer(hgap=10,vgap=10)
        figureBoxGridSizer.Add(directBeamBoxSizer,(0,0),(3,8),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=5)
        figureBoxGridSizer.Add(cropRegionBoxSizer,(3,0),(3,8),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=5)
        figureBoxSizer.Add(figureBoxGridSizer,-1, flag=wx.EXPAND|wx.ALL, border=10)
        
        
        # Integration Box
        self.integrationBox = wx.StaticBox(self,-1,'Integration')
        self.integrationBox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        integrationBoxSizer =  wx.StaticBoxSizer(self.integrationBox, wx.VERTICAL)
        
        integrationBoxGridSizer = wx.GridBagSizer(hgap=10,vgap=10)
        integrationBoxGridSizer.Add(self.integrateOverQxyKeepQzBtn,(0,0),(1,1),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=5)
        integrationBoxGridSizer.Add(self.integrateOverQxyKeepQxzBtn,(1,0),(1,1),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=5)
        integrationBoxGridSizer.Add(self.integrateOverQxzKeepQxyBtn,(2,0),(1,1),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=5)
        integrationBoxGridSizer.Add(self.integrateOverQzKeepQxyBtn,(3,0),(1,1),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=5)
        integrationBoxGridSizer.Add(self.integrateBtn,(2,1),(2,1))
        integrationBoxGridSizer.Add(self.compareBtn,(0,1),(2,1))
        integrationBoxGridSizer.Add(self.lowerLimitQAxisTxt,(0,2),(1,1))
        integrationBoxGridSizer.Add(self.lowerLimitQAxisEdt,(1,2),(1,1))
        integrationBoxGridSizer.Add(self.upperLimitQAxisTxt,(2,2),(1,1))
        integrationBoxGridSizer.Add(self.upperLimitQAxisEdt,(3,2),(1,1))
        integrationBoxSizer.Add(integrationBoxGridSizer,-1, flag=wx.EXPAND|wx.ALL, border=10)
        
        
        # ColorMap Slider
        self.sliderBox = wx.StaticBox(self,-1,label="")
        sliderBoxSizer =  wx.StaticBoxSizer(self.sliderBox, wx.VERTICAL)
        
        sliderBoxGridSizer = wx.GridBagSizer(hgap=2,vgap=2)
        sliderBoxGridSizer.Add(self.upperLimitColorMapTxt,(0,0),(1,2),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=2)
        sliderBoxGridSizer.Add(self.upperLimitColorMapSlider,(1,0),(4,2),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=2)
        sliderBoxGridSizer.Add(self.upperLimitColorMapSliderTxt,(5,0),(1,2),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=2)
        sliderBoxGridSizer.Add(self.lowerLimitColorMapTxt,(0,2),(1,2),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=2)
        sliderBoxGridSizer.Add(self.lowerLimitColorMapSlider,(1,2),(4,2),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=2)
        sliderBoxGridSizer.Add(self.lowerLimitColorMapSliderTxt,(5,2),(1,2),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=2)
        sliderBoxGridSizer.Add(self.logScaleBtn,(6,0),(1,4),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=2)
        sliderBoxSizer.Add(sliderBoxGridSizer,-1, flag=wx.EXPAND|wx.ALL, border=1)
        
        
        # Figure customization
        self.plotBox = wx.StaticBox(self,-1,'Plot')
        self.plotBox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        plotBoxSizer =  wx.StaticBoxSizer(self.plotBox, wx.VERTICAL)
        
        plotBoxGridSizer = wx.GridBagSizer(hgap=10,vgap=10)
        plotBoxGridSizer.Add(sliderBoxSizer,(0,0),(9,1),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=5)
        
        plotBoxGridSizer.Add(self.lowerLimitXAxisTxt,(0,2),(1,1),wx.EXPAND)
        plotBoxGridSizer.Add(self.lowerLimitXAxisEdt,(0,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=10)
        plotBoxGridSizer.Add(self.upperLimitXAxisTxt,(1,2),(1,1),wx.EXPAND)
        plotBoxGridSizer.Add(self.upperLimitXAxisEdt,(1,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=10)
        plotBoxGridSizer.Add(self.lowerLimitYAxisTxt,(2,2),(1,1),wx.EXPAND)
        plotBoxGridSizer.Add(self.lowerLimitYAxisEdt,(2,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=10)
        plotBoxGridSizer.Add(self.upperLimitYAxisTxt,(3,2),(1,1),wx.EXPAND)
        plotBoxGridSizer.Add(self.upperLimitYAxisEdt,(3,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=10)
        plotBoxGridSizer.Add(self.tickFontSizeTxt,(4,2),(1,1),wx.EXPAND)
        plotBoxGridSizer.Add(self.tickFontSizeEdt,(4,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=10)
        plotBoxGridSizer.Add(self.tickWidthTxt,(5,2),(1,1),wx.EXPAND)
        plotBoxGridSizer.Add(self.tickWidthEdt,(5,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=10)
        plotBoxGridSizer.Add(self.tickLengthTxt,(6,2),(1,1),wx.EXPAND)
        plotBoxGridSizer.Add(self.tickLengthEdt,(6,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=10)
        plotBoxGridSizer.Add(self.borderThicknessTxt,(7,2),(1,1),wx.EXPAND)
        plotBoxGridSizer.Add(self.borderThicknessEdt,(7,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=10)
        plotBoxGridSizer.Add(self.plotAgainBtn,(8,3),(1,1),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=10)
        plotBoxSizer.Add(plotBoxGridSizer,-1, flag=wx.EXPAND|wx.ALL, border=5)
        
        
        root = wx.GridBagSizer(2,2)
        root.Add(parametersBoxSizer,(0,0),(2,6),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=20)
        root.Add(self.statusMessageTxt,(2,0),(2,6),flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=20)
        root.Add(figureBoxSizer,(4,0),(3,6),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=20)
        root.Add(self.plotQxzQxyBtn,(7,0),(2,2),flag=wx.ALL|wx.EXPAND, border=20)
        root.Add(self.plotQzQxyBtn,(7,2),(2,2),flag=wx.ALL|wx.EXPAND, border=20)
        root.Add(self.runBtn,(7,4),(2,2),flag=wx.ALL|wx.EXPAND, border=20)
        root.Add(plotBoxSizer,(0,6),(5,5),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=20)
        root.Add(integrationBoxSizer,(5,6),(4,5),flag=wx.BOTTOM|wx.RIGHT|wx.LEFT|wx.EXPAND, border=20)
        self.SetSizerAndFit(root)
        
        
    def bindEvents(self):
    
        self.eventHandle = EventHandle(self, self.par)
        
        self.Bind(wx.EVT_MENU, self.eventHandle.onQuit, self.appQuitMenu)
        self.Bind(wx.EVT_TOOL, self.eventHandle.onQuit, self.appQuitTool)
        
        self.Bind(wx.EVT_MENU, self.eventHandle.onOpen, self.appOpenMenu)
        self.Bind(wx.EVT_TOOL, self.eventHandle.onOpen, self.appOpenTool)
        
        self.Bind(wx.EVT_TEXT_ENTER, self.eventHandle.focusOnIncidentAlpha, self.wavelengthEdt)
        self.Bind(wx.EVT_TEXT_ENTER, self.eventHandle.focusOnSampleToDetectorDistance, self.incidentAlphaEdt)
        self.Bind(wx.EVT_TEXT_ENTER, self.eventHandle.focusOnRunButton, self.sampleToDetectorDistanceEdt)
        
        self.plotQzQxyBtn.Bind(wx.EVT_BUTTON, self.eventHandle.onToggleClick)
        self.plotQxzQxyBtn.Bind(wx.EVT_BUTTON, self.eventHandle.onToggleClick)
        
        self.runBtn.Bind(wx.EVT_BUTTON, self.eventHandle.onRunButtonClick)
        self.integrateBtn.Bind(wx.EVT_BUTTON, self.eventHandle.onIntegrateButtonClick)
        self.compareBtn.Bind(wx.EVT_BUTTON, self.eventHandle.onCompareButtonClick)        
        self.plotAgainBtn.Bind(wx.EVT_BUTTON, self.eventHandle.onPlotAgainButtonClick)
        
        self.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.eventHandle.onChangeLowerLimitColorMapSlider, self.upperLimitColorMapSlider)
        self.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.eventHandle.onChangeUpperLimitColorMapSlider, self.lowerLimitColorMapSlider)
        
        self.Bind(wx.EVT_TOOL, self.eventHandle.OnSave, self.appSaveTool)
        