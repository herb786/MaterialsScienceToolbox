"""This version 
* Changes in the limits of the vertical axis. Starting at zero now.
* Add tiff output.
* Remove lock button
* Remove lines to get metadata
* Change filenames of the outputs
* Allow modification of borderline, and thick labels
* Results in nanometers
* Format the colorbar
"""
import ctypes
import wx
import wx.lib.buttons as btn
import os.path
from scipy.interpolate import griddata
import numpy as np
import scipy as sci
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcol
from matplotlib.ticker import MaxNLocator
#import matplotlib.axes as mpax
import matplotlib.widgets as widgets
import matplotlib as mpl
from PIL import Image
import json
#import matplotlib.legend as mpleg

#from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as mycanvas

class app_wx(wx.Frame):
    def __init__(self,parent,id,title):
        #wx.Frame.__init__(self,parent,id,title,style = wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER)
        wx.Frame.__init__(self,parent,id,title)
        #self.child = ChildFrame(self)
        
        #My Menubar
        self.appmenubar = wx.MenuBar()
        self.appfilemenu = wx.Menu()
        self.appopenmenu = self.appfilemenu.Append(wx.ID_OPEN,'&Open')
        self.appquitmenu = self.appfilemenu.Append(wx.ID_EXIT,'&Quit')
        self.appmenubar.Append(self.appfilemenu,'&File')
        
        #My Toolbar
        self.toolbar = self.CreateToolBar()
        openico = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN,wx.ART_TOOLBAR,(32,32))
        self.opentool = self.toolbar.AddSimpleTool(-1,openico,'Open')
        quitico = wx.ArtProvider.GetBitmap(wx.ART_DELETE,wx.ART_TOOLBAR,(32,32))
        self.quittool = self.toolbar.AddSimpleTool(-1,quitico,'Quit')
        saveico = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE,wx.ART_TOOLBAR,(32,32))
        self.savetool = self.toolbar.AddSimpleTool(-1,saveico,'Save')

        #My Labels
        self.lempty = wx.StaticText(self,-1,label=u'')
        self.lwlength = wx.StaticText(self,-1,label=u'Wavelength')
        self.lwlength.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lalfai = wx.StaticText(self,-1,label=u'Incidence Angle')
        self.lalfai.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lsddet = wx.StaticText(self,-1,label=u'SDD')
        self.lsddet.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lpvdb = wx.StaticText(self,-1,label=u'Hor')
        self.lpvdb.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lphdb = wx.StaticText(self,-1,label=u'Ver')
        self.lphdb.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lcrop = wx.StaticText(self,-1,label=u'Size')
        self.lcrop.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lcmpmax = wx.StaticText(self,-1,label=u'Max')
        self.lcmpmax.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lcmpmin = wx.StaticText(self,-1,label=u'Min')
        self.lcmpmin.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lxmin = wx.StaticText(self,-1,label=u'X-axis Min')
        self.lxmin.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lymin = wx.StaticText(self,-1,label=u'Y-axis Min')
        self.lymin.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lxmax = wx.StaticText(self,-1,label=u'X-axis Max')
        self.lxmax.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lymax = wx.StaticText(self,-1,label=u'Y-axis Max')
        self.lymax.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lborder = wx.StaticText(self,-1,label=u'Borderline')
        self.lborder.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lticksz = wx.StaticText(self,-1,label=u'Font size')
        self.lticksz.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lticklg = wx.StaticText(self,-1,label=u'Tick length')
        self.lticklg.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.ltickwd = wx.StaticText(self,-1,label=u'Tick width')
        self.ltickwd.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lpixel = wx.StaticText(self,-1,label=u'Pixel')
        self.lpixel.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.llimq1 = wx.StaticText(self,-1,label=u'q_inf')
        self.llimq1.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.llimq2 = wx.StaticText(self,-1,label=u'q_sup')
        self.llimq2.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        #My buttons
        self.button = wx.Button(self,-1,label='RUN',size=(100,50))
        self.button.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.buttonplot = wx.Button(self,-1,label='Plot',size=(100,50))
        self.buttonplot.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.btnQZ = wx.ToggleButton(self,-1,label='QZ(I vs. QXY)')
        self.btnQXYZ = wx.ToggleButton(self,-1,label='QXY(I vs. QXZ)')
        self.btnQXZ = wx.ToggleButton(self,-1,label='QXZ(I vs. QXY)')
        self.btnQXY = wx.ToggleButton(self,-1,label='QXY(I vs. QZ)')
        self.btnPlotXY = btn.GenToggleButton(self,-1,label='I(QZ,QXY)')
        self.btnPlotXYZ = btn.GenToggleButton(self,-1,label='I(QXZ,QXY)')
        self.btnScale = wx.ToggleButton(self,-1,label='Log Scale')
        self.btnCompare = wx.Button(self,-1,label='Compare',size=(100,50))
        self.btnCompare.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.btnReplot = wx.Button(self,-1,label='Replot',size=(100,50))
        self.btnReplot.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        #My Sliders(The current frequency is 100 -the fifth position in the args-)
        self.SlideCMLow = wx.Slider(self,-1,0,0,100, style=wx.SL_VERTICAL, size=(-1,250))
        #self.SlideCMLow.SetTickFreq(10, 1)
        self.SlideCMUpp = wx.Slider(self,-1,100,0,100, style=wx.SL_VERTICAL, size=(-1,250))
        #self.SlideCMUpp.SetTickFreq(10, 1)
        
        #My Inputs
        self.wlength = wx.TextCtrl(self,-1,value=u'0.138')
        self.wlength.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.alfai = wx.TextCtrl(self,-1,value=u'0.3')
        self.alfai.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.sddet = wx.TextCtrl(self,-1,value=u'0.1')
        self.sddet.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.labelpvdb = wx.TextCtrl(self,-1,value=u'NONE')
        self.labelpvdb.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.labelphdb = wx.TextCtrl(self,-1,value=u'NONE')
        self.labelphdb.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.pixel = wx.TextCtrl(self,-1,value=u'172')
        self.pixel.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.limq1 = wx.TextCtrl(self,-1,value=u'0.0')
        self.limq1.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.limq2 = wx.TextCtrl(self,-1,value=u'0.0')
        self.limq2.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        #My Plot Inputs
        self.xmin = wx.TextCtrl(self,-1,value=wx.EmptyString)
        self.xmin.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.xmax = wx.TextCtrl(self,-1,value=wx.EmptyString)
        self.xmax.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.ymin = wx.TextCtrl(self,-1,value=wx.EmptyString)
        self.ymin.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.ymax = wx.TextCtrl(self,-1,value=wx.EmptyString)
        self.ymax.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.border = wx.TextCtrl(self,-1,value='2')
        self.border.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.ticksz = wx.TextCtrl(self,-1,value='12')
        self.ticksz.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.ticklg = wx.TextCtrl(self,-1,value='6')
        self.ticklg.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.tickwd = wx.TextCtrl(self,-1,value='2')
        self.tickwd.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))

        
        #My Text Output
        self.labelC = wx.StaticText(self,-1,label=u'WAIT ORDERS',size=wx.Size(350,50),style=wx.ST_NO_AUTORESIZE)
        self.labelC.SetBackgroundColour(wx.BLUE)
        self.labelC.SetForegroundColour(wx.WHITE)
        self.labelC.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.labelcrop = wx.StaticText(self,-1,label=u'HxV')
        self.labelcrop.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.cmpmax = wx.StaticText(self,-1,label=u'None')
        self.cmpmax.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.cmpmin = wx.StaticText(self,-1,label=u'None')
        self.cmpmin.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        #My Design
        self.SetMenuBar(self.appmenubar)
        self.toolbar.Realize()
        
        self.parameters = wx.StaticBox(self,-1,'Parameters')
        self.parameters.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        parboxsizer =  wx.StaticBoxSizer(self.parameters, wx.VERTICAL)
        sizer = wx.GridBagSizer(hgap=10,vgap=10)
        sizer.Add(self.lempty,(0,5),(1,2),wx.EXPAND)
        sizer.Add(self.lwlength,(0,1),(1,2),wx.EXPAND)
        sizer.Add(self.wlength,(0,3),(1,2),wx.EXPAND)
        sizer.Add(self.lalfai,(1,1),(1,2),wx.EXPAND)
        sizer.Add(self.alfai,(1,3),(1,2),wx.EXPAND)
        sizer.Add(self.lsddet,(2,1),(1,2),wx.EXPAND)
        sizer.Add(self.sddet,(2,3),(1,2),wx.EXPAND)
        parboxsizer.Add(sizer,-1, flag=wx.EXPAND|wx.ALL, border=10)
        
        self.dbeams = wx.StaticBox(self,-1,'Direct Beam')
        self.dbeams.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        dbeamssizer =  wx.StaticBoxSizer(self.dbeams, wx.VERTICAL)
        sizerdb = wx.GridBagSizer(hgap=10,vgap=10)
        sizerdb.Add(self.lpvdb,(0,1),(1,1),wx.EXPAND)
        sizerdb.Add(self.labelphdb,(0,2),(1,1),wx.EXPAND)
        sizerdb.Add(self.lphdb,(0,3),(1,1),wx.EXPAND)
        sizerdb.Add(self.labelpvdb,(0,4),(1,1),wx.EXPAND)
        dbeamssizer.Add(sizerdb,-1, flag=wx.EXPAND|wx.ALL, border=10)
        
        self.crops = wx.StaticBox(self,-1,'Selection')
        self.crops.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        cropssizer =  wx.StaticBoxSizer(self.crops, wx.VERTICAL)
        sizercrop = wx.GridBagSizer(hgap=10,vgap=10)
        sizercrop.Add(self.lcrop,(0,1),(1,1),wx.EXPAND)
        sizercrop.Add(self.labelcrop,(0,2),(1,1),wx.EXPAND)
        sizercrop.Add(self.lpixel,(0,5),(1,1),wx.EXPAND)
        sizercrop.Add(self.pixel,(0,6),(1,1),wx.EXPAND)
        cropssizer.Add(sizercrop,-1, flag=wx.EXPAND|wx.ALL, border=10)
        
        self.figures = wx.StaticBox(self,-1,'Figure')
        self.figures.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        figuressizer =  wx.StaticBoxSizer(self.figures, wx.VERTICAL)
        sizerfigures = wx.GridBagSizer(hgap=10,vgap=10)
        sizerfigures.Add(dbeamssizer,(0,0),(3,8),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=5)
        sizerfigures.Add(cropssizer,(3,0),(3,8),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=5)
        figuressizer.Add(sizerfigures,-1, flag=wx.EXPAND|wx.ALL, border=10)
        
        self.integration = wx.StaticBox(self,-1,'Integration')
        self.integration.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        intsizer =  wx.StaticBoxSizer(self.integration, wx.VERTICAL)
        sizerints = wx.GridBagSizer(hgap=10,vgap=10)
        sizerints.Add(self.btnQXY,(0,0),(1,1),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=5)
        sizerints.Add(self.btnQXYZ,(1,0),(1,1),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=5)
        sizerints.Add(self.btnQXZ,(2,0),(1,1),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=5)
        sizerints.Add(self.btnQZ,(3,0),(1,1),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=5)
        sizerints.Add(self.buttonplot,(2,1),(2,1))
        sizerints.Add(self.btnCompare,(0,1),(2,1))
        sizerints.Add(self.llimq1,(0,2),(1,1))
        sizerints.Add(self.limq1,(1,2),(1,1))
        sizerints.Add(self.llimq2,(2,2),(1,1))
        sizerints.Add(self.limq2,(3,2),(1,1))
        intsizer.Add(sizerints,-1, flag=wx.EXPAND|wx.ALL, border=10)
        
        self.slidebox = wx.StaticBox(self,-1,label="")
        slideboxsizer =  wx.StaticBoxSizer(self.slidebox, wx.VERTICAL)
        sizerslidebox = wx.GridBagSizer(hgap=2,vgap=2)
        sizerslidebox.Add(self.lcmpmax,(0,0),(1,2),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=2)
        sizerslidebox.Add(self.SlideCMUpp,(1,0),(4,2),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=2)
        sizerslidebox.Add(self.cmpmax,(5,0),(1,2),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=2)
        sizerslidebox.Add(self.lcmpmin,(0,2),(1,2),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=2)
        sizerslidebox.Add(self.SlideCMLow,(1,2),(4,2),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=2)
        sizerslidebox.Add(self.cmpmin,(5,2),(1,2),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=2)
        sizerslidebox.Add(self.btnScale,(6,0),(1,4),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=2)
        slideboxsizer.Add(sizerslidebox,-1, flag=wx.EXPAND|wx.ALL, border=1)
        
        self.cmapp = wx.StaticBox(self,-1,'Plot')
        self.cmapp.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        mappsizer =  wx.StaticBoxSizer(self.cmapp, wx.VERTICAL)
        sizermapp = wx.GridBagSizer(hgap=10,vgap=10)
        sizermapp.Add(slideboxsizer,(0,0),(9,1),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=5)
        sizermapp.Add(self.lxmin,(0,2),(1,1),wx.EXPAND)
        sizermapp.Add(self.xmin,(0,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=10)
        sizermapp.Add(self.lxmax,(1,2),(1,1),wx.EXPAND)
        sizermapp.Add(self.xmax,(1,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=10)
        sizermapp.Add(self.lymin,(2,2),(1,1),wx.EXPAND)
        sizermapp.Add(self.ymin,(2,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=10)
        sizermapp.Add(self.lymax,(3,2),(1,1),wx.EXPAND)
        sizermapp.Add(self.ymax,(3,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=10)
        sizermapp.Add(self.lticksz,(4,2),(1,1),wx.EXPAND)
        sizermapp.Add(self.ticksz,(4,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=10)
        sizermapp.Add(self.ltickwd,(5,2),(1,1),wx.EXPAND)
        sizermapp.Add(self.tickwd,(5,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=10)
        sizermapp.Add(self.lticklg,(6,2),(1,1),wx.EXPAND)
        sizermapp.Add(self.ticklg,(6,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=10)
        sizermapp.Add(self.lborder,(7,2),(1,1),wx.EXPAND)
        sizermapp.Add(self.border,(7,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=10)
        sizermapp.Add(self.btnReplot,(8,3),(1,1),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=10)
        mappsizer.Add(sizermapp,-1, flag=wx.EXPAND|wx.ALL, border=5)
        
        
        root = wx.GridBagSizer(2,2)
        root.Add(parboxsizer,(0,0),(2,6),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=20)
        root.Add(self.labelC,(2,0),(2,6),flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=20)
        root.Add(figuressizer,(4,0),(3,6),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=20)
        root.Add(self.btnPlotXYZ,(7,0),(2,2),flag=wx.ALL|wx.EXPAND, border=20)
        root.Add(self.btnPlotXY,(7,2),(2,2),flag=wx.ALL|wx.EXPAND, border=20)
        root.Add(self.button,(7,4),(2,2),flag=wx.ALL|wx.EXPAND, border=20)
        root.Add(mappsizer,(0,6),(5,5),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=20)
        root.Add(intsizer,(5,6),(4,5),flag=wx.BOTTOM|wx.RIGHT|wx.LEFT|wx.EXPAND, border=20)
        self.SetSizerAndFit(root)
        
        #My Events
        init = np.random.random((10,10))#data to intialize a figure window
        self.events = EventH(self)
        self.myfiles = []#container for the filenames
        self.imgfileout = ''#name of the first plot 
        self.dirname = ''#directory path of the output
        self.workmx = {}#container with data image as 3D arrays
        self.pvdb = []#direct beam y-coordinate
        self.phdb = []#direct beam x-coordinate
        self.infx = []#x-coordinate of the origin for the crop rectangle
        self.infy = []#y-coordinate of the origin for the crop rectangle
        self.largueur = []#width of the crop rectangle
        self.longueur = []#height of the crop rectangle
        self.plotmxypp = {}#new 3D array of data image
        self.plotmxyzpp = {}#new 3D array of data image
        self.axisqxy = []#values of the new axis
        self.axisqz = []#values of the new axis
        self.axisqxz = []#values of the new axis
        self.cmlow = []#minimum value of the colormap from the slidebar
        self.cmupp = []#maximum value of the colormap from the slidebar
        self.cmmax = []#current maximum value of the colormap for all the plots
        self.cmmin = []#current minimum value of the colormap for all the plots
        self.xxmin = []#minimum value for the qxy coordinate
        self.yymin = []#minimum value for the qz(qxz) coordinate
        self.xxmax = []#maximum value for the qxy coordinate
        self.yymax = []#maximum value for the qz(qxz) coordinate
        self.fonty = 12#fontsize value plot labels
        self.bordy = 2#thickness of the plot border
        self.tickw = 2#width of the tick
        self.tickl = 6#length of the tick
        self.Graphos = plt.figure()#handler for the plot
        #self.GraphoPP = mpimg.AxesImage(self)
        self.GraphoPP = plt.imshow(init)#initialize a plot
        self.GraphosAx = self.Graphos.add_subplot()#handler for the axis
        self.GraphoCBar = plt.colorbar(self.GraphoPP)#handler for the colormap
        self.qsup = []#upper limit for the integration
        self.qinf = []#lower limit for the integration
        self.Bind(wx.EVT_MENU,self.events.OnOpen,self.appopenmenu)
        self.Bind(wx.EVT_MENU,self.events.OnQuit,self.appquitmenu)
        self.Bind(wx.EVT_TOOL,self.events.OnQuit,self.quittool)
        self.Bind(wx.EVT_TOOL,self.events.OnOpen,self.opentool)
        self.Bind(wx.EVT_TOOL,self.events.OnSave,self.savetool)
        self.button.Bind(wx.EVT_BUTTON,self.events.OnButtonClick)
        self.buttonplot.Bind(wx.EVT_BUTTON,self.events.PlotButtonClick)
        self.btnCompare.Bind(wx.EVT_BUTTON,self.events.BtnCompareClick)
        self.btnReplot.Bind(wx.EVT_BUTTON,self.events.BtnReplotClick)
        self.Bind(wx.EVT_SCROLL_THUMBRELEASE,self.events.MapMaxDraw,self.SlideCMUpp)
        self.Bind(wx.EVT_SCROLL_THUMBRELEASE,self.events.MapMinDraw,self.SlideCMLow)
        self.Bind(wx.EVT_TEXT_ENTER,self.events.NextA,self.wlength)
        self.Bind(wx.EVT_TEXT_ENTER,self.events.NextB,self.alfai)
        self.Bind(wx.EVT_TEXT_ENTER,self.events.NextC,self.sddet)
        self.btnPlotXY.Bind(wx.EVT_BUTTON, self.events.OnToggleClick)
        self.btnPlotXYZ.Bind(wx.EVT_BUTTON, self.events.OnToggleClick)
        
class EventH():
    def __init__(self,parent):
        self.parent = parent
        
    def OnOpen(self,event):
        dialog = wx.FileDialog(self.parent,"Choose a file",self.parent.dirname, '',"TIFF files (*.tif;*.tiff)|*.tif;*.tiff",wx.FD_MULTIPLE)
        if dialog.ShowModal() == wx.ID_OK:
            self.parent.filename = dialog.GetFilenames()
            #print self.parent.filename
            if self.parent.filename[0].endswith('.tiff'):
                self.parent.myfiles = [a.replace('.tiff','') for a in self.parent.filename]
            if self.parent.filename[0].endswith('.tif'):
                self.parent.myfiles = [a.replace('.tif','') for a in self.parent.filename]
            self.parent.labelpvdb.Enable()
            self.parent.labelphdb.Enable()
            Loading(self.parent,self.parent.filename)
    
    def OnSave(self,event):
        #print self.parent.myfiles[0]
        saveFileDialog = wx.FileDialog(self.parent, "Save DAT file", "", defaultFile=self.parent.myfiles[0],wildcard="DAT files (*.dat)|*.dat",style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
        if saveFileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed idea...
        #print saveFileDialog.GetDirectory()
        #There is file output for each button. Filename is created from the orginal one and the integration
        btnQXZ = self.parent.btnQXZ.GetValue()
        btnQZ = self.parent.btnQZ.GetValue()
        btnQXY = self.parent.btnQXY.GetValue()
        btnQXYZ = self.parent.btnQXYZ.GetValue()
        dim3 = self.parent.workmx.shape[2]
        for l in range (0,dim3):
            if btnQZ == True:
                path = os.path.join(saveFileDialog.GetDirectory(), self.parent.myfiles[l]+'_qxy.dat')
                output = open(path, 'w')
                theaxisx = self.parent.axisqxy
                theaxisy = np.sum(self.parent.plotmxypp[l+1],axis=0)
            if btnQXZ == True:
                output = os.path.join(saveFileDialog.GetDirectory(), self.parent.myfiles[l]+'_qxyz.dat')
                theaxisx = self.parent.axisqxy
                theaxisy = np.sum(self.parent.plotmxyzpp[l+1],axis=0)
            if btnQXY == True:
                output = os.path.join(saveFileDialog.GetDirectory(), self.parent.myfiles[l]+'_qz.dat')
                theaxisx = self.parent.axisqz
                theaxisy = np.sum(self.parent.plotmxypp[l+1],axis=1)               
            if btnQXYZ == True:
                output = os.path.join(saveFileDialog.GetDirectory(), self.parent.myfiles[l]+'_qxz.dat')
                theaxisx = self.parent.axisqxz
                theaxisy = np.sum(self.parent.plotmxyzpp[l+1],axis=1)
            theaxisx = theaxisx.reshape((len(theaxisx),1))
            theaxisy = theaxisy.reshape((len(theaxisx),1))
            xout = np.hstack([theaxisx,theaxisy])
            #print xout, theaxisx.shape
            np.savetxt(output,xout, fmt=['%4.5f', '%4.5f'])    
            
    def OnQuit(self,event):
        self.parent.Close()
    
    def NextA(self,event):
        self.parent.alfai.SetFocus()
        self.parent.alfai.SetSelection(-1,-1)
    
    def NextB(self,event):
        self.parent.sddet.SetFocus()
        self.parent.sddet.SetSelection(-1,-1)
            
    def NextC(self,event):
        self.parent.btnPlotXY.SetValue(True)
        self.parent.btnPlotXY.SetBackgroundColour('#DA3939')
        self.parent.btnPlotXY.SetForegroundColour('white')
        self.parent.button.SetFocus()

    def OnToggleClick(self,event):
        if self.parent.btnPlotXY.GetValue():
            self.parent.btnPlotXY.SetBackgroundColour('#DA3939')
            self.parent.btnPlotXY.SetForegroundColour('white')
        else:
            self.parent.btnPlotXY.SetBackgroundColour((240, 240, 240, 255))
            self.parent.btnPlotXY.SetForegroundColour('black')
        if self.parent.btnPlotXYZ.GetValue():
            self.parent.btnPlotXYZ.SetBackgroundColour('#DA3939')
            self.parent.btnPlotXYZ.SetForegroundColour('white')
        else:
            self.parent.btnPlotXYZ.SetBackgroundColour((240, 240, 240, 255))
            self.parent.btnPlotXYZ.SetForegroundColour('black')
            
    def OnButtonClick(self,event):
        a = self.parent.btnPlotXY.GetValue()
        b = self.parent.btnPlotXYZ.GetValue()
        if ((a and not b) or (not a and b)):
            Correction(self.parent)
        
    def PlotButtonClick(self,event):
        Integration(self.parent)
    
    def BtnCompareClick(self,event):
        Comparison(self.parent)

    def BtnReplotClick(self,event):
        self.parent.fonty = float(self.parent.ticksz.GetValue())
        self.parent.bordy = float(self.parent.border.GetValue())
        self.parent.tickw = float(self.parent.tickwd.GetValue())
        self.parent.tickl = float(self.parent.ticklg.GetValue())
        self.parent.xxmin = float(self.parent.xmin.GetValue())
        self.parent.yymin = float(self.parent.ymin.GetValue())
        self.parent.xxmax = float(self.parent.xmax.GetValue())
        self.parent.yymax = float(self.parent.ymax.GetValue())
        self.parent.GraphosAx.set_ylim([self.parent.yymin,self.parent.yymax])
        self.parent.GraphosAx.set_xlim([self.parent.xxmin,self.parent.xxmax])
        self.parent.GraphosAx.xaxis.set_major_locator(MaxNLocator(nbins=6))#tick numbers at the x-axis
        self.parent.GraphosAx.yaxis.set_major_locator(MaxNLocator(nbins=4))#tick numbers at the y-axis
        for axis in ['top','bottom','left','right']:
            self.parent.GraphosAx.spines[axis].set_linewidth(self.parent.bordy)
        mpl.rcParams['axes.linewidth'] = self.parent.bordy
        self.parent.GraphoCBar.ax.tick_params(labelsize=self.parent.fonty,length=self.parent.tickl,width=self.parent.tickw)
        self.parent.GraphosAx.get_xaxis().set_tick_params(labelsize=self.parent.fonty,length=self.parent.tickl,width=self.parent.tickw)
        self.parent.GraphosAx.get_yaxis().set_tick_params(labelsize=self.parent.fonty,length=self.parent.tickl,width=self.parent.tickw)
        plt.tight_layout()
        self.parent.GraphoCBar.draw_all()
        plt.savefig(self.parent.imgfileout)
        plt.draw()
        
    def MapMaxDraw(self,event):
        val = self.parent.SlideCMUpp.GetValue()
        lim1 = self.parent.cmlow
        lim2 = self.parent.cmupp
        if self.parent.btnScale.GetValue() == True:
            realv = lim1 + val*(lim2-lim1)/100
            self.parent.cmmax = realv
            self.parent.cmpmax.SetLabel('{:4.0f}'.format(np.power(10,realv)))
            self.parent.GraphoPP.set_clim(vmax=realv)
        else:
            realv = np.power(10,lim1)+val*(np.power(10,lim2)-np.power(10,lim1))/100
            self.parent.cmpmax.SetLabel('{:4.0f}'.format(realv))
            self.parent.cmmax = np.log10(realv)
            self.parent.GraphoPP.set_clim(vmax=np.log10(realv))
        self.parent.GraphoCBar.draw_all()
        plt.savefig(self.parent.imgfileout)
        plt.draw()
        
    def MapMinDraw(self,event):
        val = self.parent.SlideCMLow.GetValue()
        lim1 = self.parent.cmlow
        lim2 = self.parent.cmupp
        if self.parent.btnScale.GetValue() == True:
            realv = lim1 + val*(lim2-lim1)/100
            self.parent.cmmin = realv
            self.parent.cmpmin.SetLabel('{:4.0f}'.format(np.power(10,realv)))
            self.parent.GraphoPP.set_clim(vmin=realv)
        else:
            realv = np.power(10,lim1)+val*(np.power(10,lim2)-np.power(10,lim1))/100
            self.parent.cmpmin.SetLabel('{:4.0f}'.format(realv))
            self.parent.cmmin = np.log10(realv)
            self.parent.GraphoPP.set_clim(vmin=np.log10(realv))
        self.parent.GraphoCBar.draw_all()
        plt.savefig(self.parent.imgfileout)
        plt.draw()
        #self.parent.Graphos.canvas.draw()
            
#===========================================================================
def Loading(parent,imagefile):
    nfile = len(imagefile)
    #new = []
    mapp = {}
    for file in range (0,nfile):
        filekey = 1+file
        if file == 0:
            plt.close()
            imag = plt.imread(imagefile[file])
            ima=imag.astype(float)
            if np.ndim(ima)>2:#For images with more than one channel(e.g. RGBA tiff)
                ima =  np.sum(ima,axis=2)
            def doubleclick(event):
                if event.dblclick:
                    #print event.xdata, event.ydata
                    parent.pvdb = event.ydata.astype(int)
                    parent.phdb = event.xdata.astype(int)
                    parent.labelpvdb.SetValue(str(parent.pvdb))
                    parent.labelphdb.SetValue(str(parent.phdb))
                    parent.labelC.SetLabel('Select an Area')
            def onselect(eclick, erelease):
                parent.infx = np.minimum(erelease.xdata,eclick.xdata)
                parent.infy = np.minimum(erelease.ydata,eclick.ydata)
                parent.longueur = np.absolute(erelease.ydata - eclick.ydata)
                parent.largueur = np.absolute(erelease.xdata - eclick.xdata)
                if parent.longueur > 10:
                    parent.labelC.SetLabel('Close the figure\nbefore press run')
                    parent.wlength.SetFocus()
                    parent.wlength.SetSelection(-1,-1)
                fig.canvas.draw()
            fig = plt.figure()
            ax = fig.add_subplot(111)
            # Select pixel for the direct beam
            plt.imshow(ima, interpolation='none', cmap = cm.jet, norm=mcol.LogNorm())
            parent.labelC.SetLabel('Double Click for\nDirect Beam Coordinates')
            fig.canvas.mpl_connect('button_press_event', doubleclick)
            # Select region to work
            selector = widgets.RectangleSelector(ax, onselect, drawtype='box', rectprops = dict(facecolor='yellow', edgecolor = 'black', alpha=0.5, fill=True))
            plt.show()
            a,b,c,d = np.array([parent.infx, parent.infy, parent.largueur, parent.longueur], dtype=np.int32)
            #print a,b,c,d
            parent.pvdb = np.int32(float(parent.labelpvdb.GetValue()))
            parent.phdb = np.int32(float(parent.labelphdb.GetValue()))
            parent.labelpvdb.Disable()
            parent.labelphdb.Disable()
            new = np.zeros((d,c))
            for i in range (0,d):
                for j in range (0,c):
                    new[i,j] = ima[b+i,a+j]
            #Assign new direct beam coordinates respect to the crop rectangle
            parent.pvdb=parent.pvdb-b
            parent.phdb=parent.phdb-a
            mapp[filekey]= new[ ::-1,:]
            #Write out the new direct beam coordinates on screen
            parent.labelpvdb.SetValue(str(parent.pvdb))
            parent.labelphdb.SetValue(str(parent.phdb))
            dim1 = new.shape[0]
            dim2 = new.shape[1]
            #Write out the dimension of the crop rectangle
            parent.labelcrop.SetLabel(str(dim2)+'x'+str(dim1))
            #Write out the limits of the current colormap
            parent.cmpmax.SetLabel('{:4.0f}'.format(np.amax(mapp[1])))
            parent.cmpmin.SetLabel('{:4.0f}'.format(np.amin(mapp[1])))
            del ima, imag
        else:
            plt.close()
            parent.labelC.SetLabel('Reading file '+str(file+1))
            imag = plt.imread(imagefile[file])
            ima=imag.astype(float)
            if np.ndim(ima)>2:
                ima =  np.sum(ima,axis=2)
            for i in range (0,d):
                    for j in range (0,c):
                        new[i,j] = ima[b+i,a+j]
            mapp[filekey]= new[ ::-1,:]
            del ima, imag
    #Allocate data in array
    parent.workmx = mapp
    parent.labelC.SetLabel('Enter parameters\nClick on RUN')
    #Flush memory
    del mapp, new


def Correction(parent):
    lbda=float(parent.wlength.GetValue())
    tltd=float(parent.alfai.GetValue())
    dtorm=float(parent.sddet.GetValue())
    dpixel=float(parent.pixel.GetValue())
    mapp = parent.workmx
    dim1 = mapp[1].shape[0]
    dim2 = mapp[1].shape[1]
    dim3 = len(mapp)
    q=2*np.pi/lbda
    vdb=dim1-parent.pvdb
    tlt=tltd*np.pi/180
    hdb=parent.phdb
    dtor=dtorm*1e6/dpixel
    parent.labelC.SetLabel('Be patient\nLarge Images - Each one at least 3 min')
    #print dim1, dim2, dim3
    '''
    RECIPROCAL SPACE
    #dimensions of a frame
    '''
    ppy,ppx = np.mgrid[0:dim1,0:dim2]
    # polar angle in radians
    px=ppx.astype(float)
    py=ppy.astype(float)
    af=np.arctan((ppy-vdb)/np.sqrt(dtor**2+(ppx-hdb)*(ppx-hdb)))
    # azimuth angle in radians
    z2f=np.arctan((ppx-hdb)/dtor)
    # exit angle
    af2=af-tlt*np.cos(z2f)
    #af2=asin(cos(z2f).*sin(af-tlt));
    qx = q*(np.cos(af2)*np.cos(z2f)-np.cos(tlt))
    qy = q*(np.cos(af2)*np.sin(z2f))
    qxy = np.zeros([dim1,dim2])
    qxz = np.zeros([dim1,dim2])
    qz = q*(np.sin(af2)+np.sin(tlt))
    for i in range (0,dim1):
        for j in range (0,dim2):
            if qy[i,j] >= 0:
                qxy[i,j] = np.sqrt(qx[i,j]**2+qy[i,j]**2)
                if qz[i,j] >= 0:
                    qxz[i,j] = np.sqrt(qx[i,j]**2+qz[i,j]**2)
                else:
                    qxz[i,j] = -np.sqrt(qx[i,j]**2+qz[i,j]**2)
            else:
                qxy[i,j] = -np.sqrt(qx[i,j]**2+qy[i,j]**2)
                if qz[i,j] >= 0:
                    qxz[i,j] = np.sqrt(qx[i,j]**2+qz[i,j]**2)  
                else:
                    qxz[i,j] = -np.sqrt(qx[i,j]**2+qz[i,j]**2)          
    vqxy = np.ravel(qxy)
    vqxz = np.ravel(qxz)
    vqz = np.ravel(qz)
    del ppx, ppy, px, py, af, z2f, af2, qx, qy,qxy,qxz
    #New Coordinates
    qxyp = np.linspace(min(vqxy), max(vqxy),dim2)
    qxzp = np.linspace(0, max(vqxz),dim1-vdb)
    qzp = np.linspace(0, max(vqz),dim1-vdb)
    #New Center due to delocalization
    for i in range (0,dim2-1):
        if (qxyp[i+1]>=0) and (qxyp[i]<0):
            hcng=i+1
    mlx,mrx,mby,mty = hcng/2,(dim2+hcng)/2,vdb/2,(dim1+vdb)/2
    xs1,xs2,xs3,xs4 = mlx,hdb-mlx,mrx-hdb,dim2-mrx
    ys1,ys2 = dim1-mty, mty-vdb
    #Divide the image in 16 regions
    ly = np.array([mty-vdb,dim1-vdb-1,0,mty-vdb])
    lx = np.array([0,mlx,mlx,hcng,hcng,mrx,mrx,dim2-1])
    #print ly, lx
    #Clipping data cloud
    val={}
    ptxy={}
    ptxyz={}
    
    if parent.btnPlotXY.GetValue() == True:
        for l in range (0,dim3):
            values = np.ravel(mapp[l+1])
            # Tolerance for the points
            t=20
            # Data cloud for each region
            index = []
            for i in range (0,dim1*dim2):
                if (vqxy[i]<qxyp[lx[0]]) or (vqxy[i]>qxyp[lx[1]+t]) or (vqz[i]<qzp[ly[0]-t]) or (vqz[i]>qzp[ly[1]]):
                    index.append(i)
            val[str(10000+l)]=np.delete(values,index)
            ptxy[str(10000+l)]=np.array([np.delete(vqxy,index),np.delete(vqz,index)])
            index = []
            for i in range (0,dim1*dim2):
                if (vqxy[i]<qxyp[lx[2]-t]) or (vqxy[i]>qxyp[lx[3]]) or (vqz[i]<qzp[ly[0]-t]) or (vqz[i]>qzp[ly[1]]):
                    index.append(i)
            val[str(20000+l)]=np.delete(values,index)
            ptxy[str(20000+l)]=np.array([np.delete(vqxy,index),np.delete(vqz,index)])
            index = []
            for i in range (0,dim1*dim2):
                if (vqxy[i]<qxyp[lx[4]]) or (vqxy[i]>qxyp[lx[5]+t]) or (vqz[i]<qzp[ly[0]-t]) or (vqz[i]>qzp[ly[1]]):
                    index.append(i)
            val[str(30000+l)]=np.delete(values,index)
            ptxy[str(30000+l)]=np.array([np.delete(vqxy,index),np.delete(vqz,index)])
            index = []
            for i in range (0,dim1*dim2):
                if (vqxy[i]<qxyp[lx[6]-t]) or (vqxy[i]>qxyp[lx[7]]) or (vqz[i]<qzp[ly[0]-t]) or (vqz[i]>qzp[ly[1]]):
                    index.append(i)
            val[str(40000+l)]=np.delete(values,index)
            ptxy[str(40000+l)]=np.array([np.delete(vqxy,index),np.delete(vqz,index)])
            # Data cloud for each region
            index = []
            for i in range (0,dim1*dim2):
                if (vqxy[i]<qxyp[lx[0]]) or (vqxy[i]>qxyp[lx[1]+t]) or (vqz[i]<qzp[ly[2]]) or (vqz[i]>qzp[ly[3]+t]):
                    index.append(i)
            val[str(50000+l)]=np.delete(values,index)
            ptxy[str(50000+l)]=np.array([np.delete(vqxy,index),np.delete(vqz,index)])
            index = []
            for i in range (0,dim1*dim2):
                if (vqxy[i]<qxyp[lx[2]-t]) or (vqxy[i]>qxyp[lx[3]]) or (vqz[i]<qzp[ly[2]]) or (vqz[i]>qzp[ly[3]+t]):
                    index.append(i)
            val[str(60000+l)]=np.delete(values,index)
            ptxy[str(60000+l)]=np.array([np.delete(vqxy,index),np.delete(vqz,index)])
            index = []
            for i in range (0,dim1*dim2):
                if (vqxy[i]<qxyp[lx[4]]) or (vqxy[i]>qxyp[lx[5]+t]) or (vqz[i]<qzp[ly[2]]) or (vqz[i]>qzp[ly[3]+t]):
                    index.append(i)
            val[str(70000+l)]=np.delete(values,index)
            ptxy[str(70000+l)]=np.array([np.delete(vqxy,index),np.delete(vqz,index)])
            index = []
            for i in range (0,dim1*dim2):
                if (vqxy[i]<qxyp[lx[6]-t]) or (vqxy[i]>qxyp[lx[7]]) or (vqz[i]<qzp[ly[2]]) or (vqz[i]>qzp[ly[3]+t]):
                    index.append(i)
            val[str(80000+l)]=np.delete(values,index)
            ptxy[str(80000+l)]=np.array([np.delete(vqxy,index),np.delete(vqz,index)])
            
    if parent.btnPlotXYZ.GetValue() == True:
        for l in range (0,dim3):
            values = np.ravel(mapp[l+1])
            # Tolerance for the points
            t=20
            # Data cloud for each region
            index = []
            for i in range (0,dim1*dim2):
                if (vqxy[i]<qxyp[lx[0]]) or (vqxy[i]>qxyp[lx[1]]) or (vqxz[i]<qxzp[ly[0]]) or (vqxz[i]>qxzp[ly[1]]):
                    index.append(i)
            val[str(10000+l)]=np.delete(values,index)
            ptxyz[str(10000+l)]=np.array([np.delete(vqxy,index),np.delete(vqxz,index)])
            index = []
            for i in range (0,dim1*dim2):
                if (vqxy[i]<qxyp[lx[2]]) or (vqxy[i]>qxyp[lx[3]]) or (vqxz[i]<qxzp[ly[0]]) or (vqxz[i]>qxzp[ly[1]]):
                    index.append(i)
            val[str(20000+l)]=np.delete(values,index)
            ptxyz[str(20000+l)]=np.array([np.delete(vqxy,index),np.delete(vqxz,index)])
            index = []
            for i in range (0,dim1*dim2):
                if (vqxy[i]<qxyp[lx[4]]) or (vqxy[i]>qxyp[lx[5]]) or (vqxz[i]<qxzp[ly[0]]) or (vqxz[i]>qxzp[ly[1]]):
                    index.append(i)
            val[str(30000+l)]=np.delete(values,index)
            ptxyz[str(30000+l)]=np.array([np.delete(vqxy,index),np.delete(vqxz,index)])
            index = []
            for i in range (0,dim1*dim2):
                if (vqxy[i]<qxyp[lx[6]]) or (vqxy[i]>qxyp[lx[7]]) or (vqxz[i]<qxzp[ly[0]]) or (vqxz[i]>qxzp[ly[1]]):
                    index.append(i)
            val[str(40000+l)]=np.delete(values,index)
            ptxyz[str(40000+l)]=np.array([np.delete(vqxy,index),np.delete(vqxz,index)])
            # Data cloud for each region
            index = []
            for i in range (0,dim1*dim2):
                if (vqxy[i]<qxyp[lx[0]]) or (vqxy[i]>qxyp[lx[1]]) or (vqxz[i]<qxzp[ly[2]]) or (vqxz[i]>qxzp[ly[3]]):
                    index.append(i)
            val[str(50000+l)]=np.delete(values,index)
            ptxyz[str(50000+l)]=np.array([np.delete(vqxy,index),np.delete(vqxz,index)])
            index = []
            for i in range (0,dim1*dim2):
                if (vqxy[i]<qxyp[lx[2]]) or (vqxy[i]>qxyp[lx[3]]) or (vqxz[i]<qxzp[ly[2]]) or (vqxz[i]>qxzp[ly[3]]):
                    index.append(i)
            val[str(60000+l)]=np.delete(values,index)
            ptxyz[str(60000+l)]=np.array([np.delete(vqxy,index),np.delete(vqxz,index)])
            index = []
            for i in range (0,dim1*dim2):
                if (vqxy[i]<qxyp[lx[4]]) or (vqxy[i]>qxyp[lx[5]]) or (vqxz[i]<qxzp[ly[2]]) or (vqxz[i]>qxzp[ly[3]]):
                    index.append(i)
            val[str(70000+l)]=np.delete(values,index)
            ptxyz[str(70000+l)]=np.array([np.delete(vqxy,index),np.delete(vqxz,index)])
            index = []
            for i in range (0,dim1*dim2):
                if (vqxy[i]<qxyp[lx[6]]) or (vqxy[i]>qxyp[lx[7]]) or (vqxz[i]<qxzp[ly[2]]) or (vqxz[i]>qxzp[ly[3]]):
                    index.append(i)
            val[str(80000+l)]=np.delete(values,index)
            ptxyz[str(80000+l)]=np.array([np.delete(vqxy,index),np.delete(vqxz,index)])        
                        
    # Mapping with the new coordinates
    if parent.btnPlotXY.GetValue() == True:
        dqxyp={}
        dqzp={}
        gx={}
        gy={}
        mx={}
        parent.axisqz = qzp[ly[2]:ly[1]]
        for l in range (0,dim3):
            for r in range (0,4):
                key1,key2 = str(10000*(r+1)+l),str(10000*(r+5)+l)
                dqxyp[key1] = qxyp[lx[2*r]:lx[2*r+1]]
                dqxyp[key2] = qxyp[lx[2*r]:lx[2*r+1]]
                dqzp[key1] = qzp[ly[0]:ly[1]]
                dqzp[key2] = qzp[ly[2]:ly[3]]
                gx[key1], gy[key1] = np.meshgrid(dqxyp[key1], dqzp[key1])
                gx[key2], gy[key2] = np.meshgrid(dqxyp[key2], dqzp[key2])
                mx[key1] = griddata(ptxy[key1].T, val[key1], (gx[key1], gy[key1]), method='linear')
                mx[key2] = griddata(ptxy[key2].T, val[key2], (gx[key2], gy[key2]), method='linear')
            #print mx['40000']
            g11,g12,g13,g14 = mx[str(10000+l)],mx[str(20000+l)],mx[str(30000+l)],mx[str(40000+l)]
            g21,g22,g23,g24 = mx[str(50000+l)],mx[str(60000+l)],mx[str(70000+l)],mx[str(80000+l)]
            sub_g1 = np.concatenate((g11,g12,g13,g14), axis=1)
            sub_g2 = np.concatenate((g21,g22,g23,g24), axis=1)
            grid = np.concatenate((sub_g2,sub_g1), axis=0)
            overall = np.nan_to_num(grid)
            parent.plotmxypp[l+1] = overall
              
    if parent.btnPlotXYZ.GetValue() == True:    
        dqxyp={}
        dqxzp={}
        gx={}
        gy={}
        mx={}
        parent.axisqxz = qxzp[ly[2]:ly[1]]
        for l in range (0,dim3):
            for r in range (0,4):
                key1,key2 = str(10000*(r+1)+l),str(10000*(r+5)+l)
                dqxyp[key1] = qxyp[lx[2*r]:lx[2*r+1]]
                dqxyp[key2] = qxyp[lx[2*r]:lx[2*r+1]]
                dqxzp[key1] = qxzp[ly[0]:ly[1]]
                dqxzp[key2] = qxzp[ly[2]:ly[3]]
                gx[key1], gy[key1] = np.meshgrid(dqxyp[key1], dqxzp[key1])
                gx[key2], gy[key2] = np.meshgrid(dqxyp[key2], dqxzp[key2])
                mx[key1] = griddata(ptxyz[key1].T, val[key1], (gx[key1], gy[key1]), method='linear')
                mx[key2] = griddata(ptxyz[key2].T, val[key2], (gx[key2], gy[key2]), method='linear')
            #print mx['40000']
            g11,g12,g13,g14 = mx[str(10000+l)],mx[str(20000+l)],mx[str(30000+l)],mx[str(40000+l)]
            g21,g22,g23,g24 = mx[str(50000+l)],mx[str(60000+l)],mx[str(70000+l)],mx[str(80000+l)]
            sub_g1 = np.concatenate((g11,g12,g13,g14), axis=1)
            sub_g2 = np.concatenate((g21,g22,g23,g24), axis=1)
            grid = np.concatenate((sub_g2,sub_g1), axis=0)
            overall = np.nan_to_num(grid)
            parent.plotmxyzpp[1+l] = overall
            
    #======================================================================================            
    # Make the plot
    parent.axisqxy = qxyp[lx[0]:lx[7]]
    if parent.btnPlotXY.GetValue() == True:
        parent.xmin.SetValue('{:4.4f}'.format(min(qxyp)))
        parent.xmax.SetValue('{:4.4f}'.format(max(qxyp)))
        parent.ymin.SetValue('{:4.4f}'.format(min(qzp)))
        parent.ymax.SetValue('{:4.4f}'.format(max(qzp)))
        parent.xxmin = float(parent.xmin.GetValue())
        parent.yymin = float(parent.ymin.GetValue())
        parent.xxmax = float(parent.xmax.GetValue())
        parent.yymax = float(parent.ymax.GetValue())
        info = dict(qxy_min = min(qxyp), qxy_max = max(qxyp), qz_min = min(qzp), qz_max = max(qzp))
        info = json.dumps(info)
        for l in range (0,dim3):
            if l==0:
                plt.close()
                parent.Graphos = plt.figure(num=None, figsize=(8,8), dpi=120)
                parent.GraphosAx = parent.Graphos.add_subplot(111)
                mini = np.amin(parent.plotmxypp[l+1])
                mx_plot = np.log10(parent.plotmxypp[l+1]-mini+1)
                np.savetxt(parent.myfiles[l]+"_qxy.dat", parent.plotmxypp[l+1].astype('float32')) 
                parent.cmlow = np.amin(mx_plot)
                parent.cmupp = np.amax(mx_plot)
                parent.cmmin = parent.cmlow
                parent.cmmax = parent.cmupp
                parent.GraphoPP = plt.imshow(np.flipud(mx_plot),extent=[min(qxyp),max(qxyp),min(qzp),max(qzp)])
                plt.xlabel('$q_{xy}$ [nm$^{-1}$]',fontsize=22)
                plt.ylabel('$q_{z}$ [nm$^{-1}$]',fontsize=22)
                divider = make_axes_locatable(plt.gca())
                cax = divider.append_axes("right", "5%", pad="3%")
                parent.GraphoCBar = plt.colorbar(parent.GraphoPP, cax=cax)
                for axis in ['top','bottom','left','right']:
                    parent.GraphosAx.spines[axis].set_linewidth(parent.bordy)
                parent.GraphoCBar.outline.set_linewidth(parent.bordy)
                parent.GraphoCBar.ax.tick_params(labelsize=parent.fonty,length=parent.tickl,width=parent.tickw)
                parent.GraphosAx.get_xaxis().set_tick_params(labelsize=parent.fonty,length=parent.tickl,width=parent.tickw)
                parent.GraphosAx.get_yaxis().set_tick_params(labelsize=parent.fonty,length=parent.tickl,width=parent.tickw)
                plt.tight_layout()
                parent.imgfileout = parent.myfiles[l]+"_qxy.png"
                plt.savefig(parent.imgfileout)
                plt.show()
            else:
                plt.close()
                parent.Graphos = plt.figure(num=None, figsize=(8,8), dpi=120)
                parent.GraphosAx = parent.Graphos.add_subplot(111)
                mini = np.amin(parent.plotmxypp[l+1])
                mx_plot = np.log10(parent.plotmxypp[l+1]-mini+1)
                parent.GraphoPP = plt.imshow(np.flipud(mx_plot),extent=[min(qxyp),max(qxyp),min(qzp),max(qzp)])
                plt.xlabel('$q_{xy}$ [nm$^{-1}$]',fontsize=22)
                plt.ylabel('$q_{z}$ [nm$^{-1}$]',fontsize=22)
                parent.GraphosAx.set_ylim([parent.yymin,parent.yymax])
                parent.GraphosAx.set_xlim([parent.xxmin,parent.xxmax])
                parent.GraphosAx.xaxis.set_major_locator(MaxNLocator(nbins=6))
                parent.GraphosAx.yaxis.set_major_locator(MaxNLocator(nbins=4))
                parent.GraphoPP.set_clim(vmin=parent.cmmin, vmax=parent.cmmax)
                divider = make_axes_locatable(plt.gca())
                cax = divider.append_axes("right", "5%", pad="3%")
                parent.GraphoCBar = plt.colorbar(parent.GraphoPP, cax=cax)
                for axis in ['top','bottom','left','right']:
                    parent.GraphosAx.spines[axis].set_linewidth(parent.bordy)
                parent.GraphoCBar.outline.set_linewidth(parent.bordy)
                parent.GraphoCBar.ax.tick_params(labelsize=parent.fonty,length=parent.tickl,width=parent.tickw)
                parent.GraphosAx.get_xaxis().set_tick_params(labelsize=parent.fonty,length=parent.tickl,width=parent.tickw)
                parent.GraphosAx.get_yaxis().set_tick_params(labelsize=parent.fonty,length=parent.tickl,width=parent.tickw)
                plt.tight_layout()
                parent.GraphoCBar.draw_all()
                plt.savefig(parent.myfiles[l]+"_qxy.png")
                np.savetxt(parent.myfiles[l]+"_qxy.dat", parent.plotmxypp[l+1].astype('float32'))
    if parent.btnPlotXYZ.GetValue() == True:
        parent.xmin.SetValue('{:4.4f}'.format(min(qxyp)))
        parent.xmax.SetValue('{:4.4f}'.format(max(qxyp)))
        parent.ymin.SetValue('{:4.4f}'.format(min(qxzp)))
        parent.ymax.SetValue('{:4.4f}'.format(max(qxzp)))
        parent.xxmin = float(parent.xmin.GetValue())
        parent.yymin = float(parent.ymin.GetValue())
        parent.xxmax = float(parent.xmax.GetValue())
        parent.yymax = float(parent.ymax.GetValue())
        info = dict(qxy_min = min(qxyp), qxy_max = max(qxyp), qxz_min = min(qxzp), qxz_max = max(qxzp))
        info = json.dumps(info)
        for l in range (0,dim3):
            if l==0:
                plt.close()
                parent.Graphos = plt.figure(num=None, figsize=(8,8), dpi=120)
                parent.GraphosAx = parent.Graphos.add_subplot(111)
                mini = np.amin(parent.plotmxyzpp[1+l])
                mx_plot = np.log10(parent.plotmxyzpp[1+l]-mini+1)
                np.savetxt(parent.myfiles[l]+"_qxz.dat", parent.plotmxyzpp[l+1].astype('float32'))
                parent.cmlow = np.amin(mx_plot)
                parent.cmupp = np.amax(mx_plot)
                parent.cmmin = parent.cmlow
                parent.cmmax = parent.cmupp
                parent.GraphoPP = plt.imshow(np.flipud(mx_plot),extent=[min(qxyp),max(qxyp),min(qxzp),max(qxzp)])
                plt.xlabel('$q_{xy}$ [nm$^{-1}$]',fontsize=22)
                plt.ylabel('$q_{xz}$ [nm$^{-1}$]',fontsize=22)
                divider = make_axes_locatable(plt.gca())
                cax = divider.append_axes("right", "5%", pad="3%")
                parent.GraphoCBar = plt.colorbar(parent.GraphoPP, cax=cax)
                for axis in ['top','bottom','left','right']:
                    parent.GraphosAx.spines[axis].set_linewidth(parent.bordy)
                parent.GraphoCBar.outline.set_linewidth(parent.bordy)
                parent.GraphoCBar.ax.tick_params(labelsize=parent.fonty,length=parent.tickl,width=parent.tickw)
                parent.GraphosAx.get_xaxis().set_tick_params(labelsize=parent.fonty,length=parent.tickl,width=parent.tickw)
                parent.GraphosAx.get_yaxis().set_tick_params(labelsize=parent.fonty,length=parent.tickl,width=parent.tickw)
                plt.tight_layout()
                parent.imgfileout = parent.myfiles[l]+"_qxz.png"
                plt.savefig(parent.imgfileout)
                plt.show()
            else:
                plt.close()
                parent.Graphos = plt.figure(num=None, figsize=(8,8), dpi=120)
                parent.GraphosAx = parent.Graphos.add_subplot(111)
                mini = np.amin(parent.plotmxyzpp[1+l])
                mx_plot = np.log10(parent.plotmxyzpp[1+l]-mini+1)
                parent.GraphoPP = plt.imshow(np.flipud(mx_plot),extent=[min(qxyp),max(qxyp),min(qzp),max(qzp)])
                plt.xlabel('$q_{xy}$ [nm$^{-1}$]',fontsize=22)
                plt.ylabel('$q_{xz}$ [nm$^{-1}$]',fontsize=22)
                parent.GraphosAx.set_ylim([parent.yymin,parent.yymax])
                parent.GraphosAx.set_xlim([parent.xxmin,parent.xxmax])
                parent.GraphosAx.xaxis.set_major_locator(MaxNLocator(nbins=6))
                parent.GraphosAx.yaxis.set_major_locator(MaxNLocator(nbins=4))
                parent.GraphoPP.set_clim(vmin=parent.cmmin, vmax=parent.cmmax)
                divider = make_axes_locatable(plt.gca())
                cax = divider.append_axes("right", "5%", pad="3%")
                parent.GraphoCBar = plt.colorbar(parent.GraphoPP, cax=cax)
                for axis in ['top','bottom','left','right']:
                    parent.GraphosAx.spines[axis].set_linewidth(parent.bordy)
                parent.GraphoCBar.outline.set_linewidth(parent.bordy)
                parent.GraphoCBar.ax.tick_params(labelsize=parent.fonty,length=parent.tickl,width=parent.tickw)
                parent.GraphosAx.get_xaxis().set_tick_params(labelsize=parent.fonty,length=parent.tickl,width=parent.tickw)
                parent.GraphosAx.get_yaxis().set_tick_params(labelsize=parent.fonty,length=parent.tickl,width=parent.tickw)
                plt.tight_layout()
                parent.GraphoCBar.draw_all()
                plt.savefig(parent.myfiles[l]+"_qxz.png")
                np.savetxt(parent.myfiles[l]+"_qxz.dat", parent.plotmxyzpp[l+1].astype('float32'))                

def Integration(parent):
    plt.close()
    dim3 = len(parent.workmx)
    btnQXZ = parent.btnQXZ.GetValue()
    btnQZ = parent.btnQZ.GetValue()
    btnQXY = parent.btnQXY.GetValue()
    btnQXYZ = parent.btnQXYZ.GetValue()
    parent.qinf = float(parent.limq1.GetValue())
    parent.qsup = float(parent.limq2.GetValue())
    if btnQZ == True:
        if parent.qinf != 0 and parent.qsup != 0: 
            i1,i2=0,0
            while parent.qinf >= parent.axisqz[i1]:
                a,i1=i1,i1+1
            while parent.qsup >= parent.axisqz[i2]:
                b,i2=i2,i2+1
            intqxy = np.sum(parent.plotmxypp[1][a:b,:],axis=0)
        else:
            intqxy = np.sum(parent.plotmxypp[1],axis=0)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.semilogy(parent.axisqxy, intqxy, 'r.-')
        plt.xlabel(r'$q_{xy}$',fontsize=22)
        plt.ylabel(r'$Intensity[u.a.]$',fontsize=22)
    if btnQXZ == True:
        if parent.qinf != 0 and parent.qsup != 0: 
            i1,i2=0,0
            while parent.qinf >= parent.axisqxz[i1]:
                a,i1=i1,i1+1
            while parent.qsup >= parent.axisqxz[i2]:
                b,i2=i2,i2+1
            intqxy = np.sum(parent.plotmxyzpp[1][a:b,:],axis=0)
        else:
            intqxy = np.sum(parent.plotmxyzpp[1],axis=0)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.semilogy(parent.axisqxy, intqxy, 'b.-')
        plt.xlabel(r'$q_{xy}$',fontsize=22)
        plt.ylabel(r'$Intensity[u.a.]$',fontsize=22)
    if btnQXY == True:
        if parent.qinf != 0 and parent.qsup != 0: 
            i1,i2=0,0
            while parent.qinf >= parent.axisqxy[i1]:
                a,i1=i1,i1+1
            while parent.qsup >= parent.axisqxy[i2]:
                b,i2=i2,i2+1
            intqz = np.sum(parent.plotmxypp[1][:,a:b],axis=1)
        else:
            intqz = np.sum(parent.plotmxypp[1],axis=1)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.semilogy(parent.axisqz, intqz, 'r.-')
        plt.xlabel(r'$q_z$',fontsize=22)
        plt.ylabel(r'$Intensity[u.a.]$',fontsize=22)
    if btnQXYZ == True:
        if parent.qinf != 0 and parent.qsup != 0: 
            i1,i2=0,0
            while parent.qinf >= parent.axisqxy[i1]:
                a,i1=i1,i1+1
            while parent.qsup >= parent.axisqxy[i2]:
                b,i2=i2,i2+1
            intqz = np.sum(parent.plotmxyzpp[1][:,a:b],axis=1)
        else:
            intqz = np.sum(parent.plotmxyzpp[1],axis=1)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.semilogy(parent.axisqxz, intqz, 'b.-')
        plt.xlabel(r'$q_{xz}$',fontsize=22)
        plt.ylabel(r'$Intensity[u.a.]$',fontsize=22)
    plt.show()
    

def Comparison(parent):
    dim3 = parent.workmx.shape[2]
    btnQXZ = parent.btnQXZ.GetValue()
    btnQZ = parent.btnQZ.GetValue()
    btnQXY = parent.btnQXY.GetValue()
    btnQXYZ = parent.btnQXYZ.GetValue()
    if (btnQZ and btnQXZ):
            y1 = np.sum(parent.plotmxypp[1],axis=0)
            y2 = np.sum(parent.plotmxyzpp[1],axis=0)
            fig = plt.figure()
            ax = fig.add_subplot(111)
            p1, = plt.semilogy(parent.axisqxy, y1, 'r.-')
            p2, = plt.semilogy(parent.axisqxy, y2, 'b.-')
            plt.xlabel(r'$q_{xy}$',fontsize=22)
            plt.ylabel(r'$Intensity[u.a.]$',fontsize=22)
            plt.legend([p1, p2], ["$q_{z}$", "$q_{xz}$"])
            plt.setp(plt.gca().get_legend().get_texts(), fontsize='18') 
    if (btnQXY and btnQXYZ):
            y1 = np.sum(parent.plotmxypp[1],axis=1)
            y2 = np.sum(parent.plotmxyzpp[1],axis=1)
            fig = plt.figure()
            ax = fig.add_subplot(111)
            p1, = plt.semilogy(parent.axisqz, y1, 'r.-')
            p2, = plt.semilogy(parent.axisqxz, y2, 'b.-')
            plt.xlabel(r'$q_{z},q_{xz}$',fontsize=22)
            plt.ylabel(r'$Intensity[u.a.]$',fontsize=22)
            plt.legend([p1, p2], ["$q_{z}$", "$q_{xz}$"])
            plt.setp(plt.gca().get_legend().get_texts(), fontsize='18') 
    plt.show()
    
   
def Main():
    vmp = mpl.__version__
    vnp = np.__version__
    vsc = sci.__version__
    if vmp=='1.4.2':
        app = wx.App()
        frame = app_wx(None,-1,'GIWAXS-Correction-Tool')
        frame.Show()
        app.MainLoop()
    else:
        mess = "Matplolib vers. < "+"1.4.2\nYour version is "+vmp+"\nNumpy v. "+vnp+"\nScipy v. "+vsc
        ctypes.windll.user32.MessageBoxA(0, mess, "Update python", 1)
    
if __name__ == "__main__":
    Main()
