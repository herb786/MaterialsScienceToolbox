import ctypes
import wx
import wx.lib.buttons as btn
import wx.lib.agw.shapedbutton as agw
import os.path
from scipy.interpolate import griddata
import numpy as np
import scipy as sci
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcol
from matplotlib.ticker import MaxNLocator
from scipy.spatial import cKDTree as kdtree
import matplotlib.widgets as widgets
import matplotlib as mpl
from PIL import Image
import json
import logging
import wx.lib.inspection



#from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as mycanvas

class app_wx(wx.Frame):
    def __init__(self,parent,id,title):
        #wx.Frame.__init__(self,parent,id,title,style = wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER)
        wx.Frame.__init__(self,parent,id,title,pos=(0,0))
        appPan = wx.Panel(self)

        #My Menubar
        self.appmenubar = wx.MenuBar()
        self.appfilemenu = wx.Menu()
        self.appopenmenu = self.appfilemenu.Append(wx.ID_OPEN,'&Open')
        self.appquitmenu = self.appfilemenu.Append(wx.ID_EXIT,'&Quit')
        self.appmenubar.Append(self.appfilemenu,'&File')
        self.appoptions = wx.Menu()
        self.menparameters = self.appoptions.Append(wx.NewId(),'Para&meters')
        self.menintegration = self.appoptions.Append(wx.NewId(),'&Integration')
        self.mencustomize = self.appoptions.Append(wx.NewId(),'&Customize')
        self.appmenubar.Append(self.appoptions,'O&ptions')
        
        #My Toolbar
        self.toolbar = self.CreateToolBar()
        openico = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN,wx.ART_TOOLBAR,(32,32))
        self.opentool = self.toolbar.AddSimpleTool(-1,openico,'Open')
        quitico = wx.ArtProvider.GetBitmap(wx.ART_DELETE,wx.ART_TOOLBAR,(32,32))
        self.quittool = self.toolbar.AddSimpleTool(-1,quitico,'Quit')
        saveico = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE,wx.ART_TOOLBAR,(32,32))
        self.savetool = self.toolbar.AddSimpleTool(-1,saveico,'Save')
        
        #My buttons
        self.button = wx.BitmapButton(appPan,-1,bitmap=wx.Bitmap('icons//run.png'),size=(80,80))
        #self.button.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        #self.btnTransf1 = btn.GenToggleButton(appPan,-1,label='Angle',size=(80,80))
        #self.btnTransf2 = btn.GenToggleButton(appPan,-1,label='Qxz',size=(80,80))
        #self.btnTransf3 = btn.GenToggleButton(appPan,-1,label='Qx/z',size=(80,80))
        self.btnTransf1 = btn.GenBitmapToggleButton(appPan,-1,bitmap=wx.Bitmap('icons//ang.png'),size=(80,80))
        self.btnTransf2 = btn.GenBitmapToggleButton(appPan,-1,bitmap=wx.Bitmap('icons//qxz.png'),size=(80,80))
        self.btnTransf3 = btn.GenBitmapToggleButton(appPan,-1,bitmap=wx.Bitmap('icons//qxzz.png'),size=(80,80))
        self.btnInt1 = btn.GenBitmapToggleButton(appPan,-1,bitmap=wx.Bitmap('icons//sx.png'),size=(80,80))
        #self.btnInt1.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        #self.btnInt2 = agw.SBitmapToggleButton(appPan,-1,bitmap=wx.Bitmap('icons//sy.png'),size=(80,80))
        self.btnInt2 = btn.GenBitmapToggleButton(appPan,-1,bitmap=wx.Bitmap('icons//sy.png'),size=(80,80))
        #self.btnInt2.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        #My Design
        self.sline1 = wx.StaticLine(appPan,-1, size=(80,5),style=wx.LI_HORIZONTAL)
        self.sline2 = wx.StaticLine(appPan,-1, size=(80,5),style=wx.LI_HORIZONTAL)
        self.SetMenuBar(self.appmenubar)
        self.toolbar.Realize()
        topSizer = wx.BoxSizer(wx.VERTICAL)
        root = wx.GridBagSizer(1,1)
        root.Add(self.btnTransf1,(0,0),(1,1),flag=wx.ALL|wx.EXPAND, border=5)
        root.Add(self.btnTransf2,(1,0),(1,1),flag=wx.ALL|wx.EXPAND, border=5)
        root.Add(self.btnTransf3,(2,0),(1,1),flag=wx.ALL|wx.EXPAND, border=5)
        root.Add(self.sline1,(3,0),(1,1),flag=wx.ALL|wx.EXPAND, border=5)
        root.Add(self.btnInt1,(4,0),(1,1),flag=wx.ALL|wx.EXPAND, border=5)
        root.Add(self.btnInt2,(5,0),(1,1),flag=wx.ALL|wx.EXPAND, border=5)
        root.Add(self.sline2,(6,0),(1,1),flag=wx.ALL|wx.EXPAND, border=5)
        root.Add(self.button,(7,0),(1,1),flag=wx.ALL|wx.EXPAND, border=5)
        topSizer.Add(root,0,wx.CENTER)
        appPan.SetSizer(topSizer)
        topSizer.Fit(self)
        
        init = np.random.random((10,10))#data to intialize a figure window
        self.valAN = [0.616000]#Incidence Angle
        self.valSDD = [2884.00]#sample to detector distance
        self.valPIX = [1.22000]#pixel size
        self.valSPE = [192]#specular pixel
        self.idTransf = 1#Transformation Type
        self.events = EventH(self)
        self.myxml = ['none']#container for the xml files
        self.mytxt = ['none']#container for the text files
        self.imgfileout = ''#name of the first plot 
        self.dirname = ''#directory path of the output
        self.workmx = {}#container with data image as 3D arrays
        self.intdata = {}#container for integration
        self.pvdb = []#direct beam y-coordinate
        self.phdb = []#direct beam x-coordinate
        self.infx = []#x-coordinate of the origin for the crop rectangle
        self.infy = []#y-coordinate of the origin for the crop rectangle
        self.largueur = []#width of the crop rectangle
        self.longueur = []#height of the crop rectangle
        self.plotmxz = {}#new 3D array of data image
        self.plotmxzz = {}#new 3D array of data image
        self.plotmif = {}#new 3D array of data image
        self.axisxx = []#values of the integration axis
        self.axisyy = []#values of the integration axis
        self.axisxw = []#values of the axis for mapping
        self.axisyw = []#values of the axis for mapping
        self.origl = []#min value for the intensity
        self.origu = []#max value for the intensity
        self.cmlow = []#minimum value of the colormap from the slidebar
        self.cmupp = []#maximum value of the colormap from the slidebar
        self.cmmax = []#current maximum value of the colormap for all the plots
        self.cmmin = []#current minimum value of the colormap for all the plots
        self.xxmin = []#minimum value for the qxy coordinate
        self.yymin = []#minimum value for the qz(qxz) coordinate
        self.xxmax = []#maximum value for the qxy coordinate
        self.yymax = []#maximum value for the qz(qxz) coordinate
        self.fontly = 22#fontsize value plot labels
        self.fonty = 12#fontsize value plot labels
        self.bordy = 2#thickness of the plot border
        self.tickw = 2#width of the tick
        self.tickl = 6#length of the tick
        self.cy2 = 0.#upper limit for the integration
        self.cy1 = 0.#lower limit for the integration
        self.cx2 = 0.#upper limit for the integration
        self.cx1 = 0.#lower limit for the integration
        self.y2 = 0.#upper limit for the integration
        self.y1 = 0.#lower limit for the integration
        self.x2 = 0.#upper limit for the integration
        self.x1 = 0.#lower limit for the integration
        self.aratio = 1#aspect ratio
        self.gami = 1.#gamma factor
        self.Graphos = plt.figure()#handler for the plot
        #self.GraphoPP = mpimg.AxesImage(self)
        self.GraphoPP = plt.imshow(init)#initialize a plot
        self.GraphosAx = self.Graphos.add_subplot()#handler for the axis
        self.GraphoCBar = plt.colorbar(self.GraphoPP)#handler for the colormap
        self.vtolm = 200#tolerance of the mask
        self.ztonan = False#Replace zeros with NaN values
        
        #My Colormap
        #self.ctof = {'red':(( 0.000, 1.000, 1.000),( 0.143, 0.000, 0.000),( 0.286, 1.000, 1.000),( 0.429, 1.000, 1.000),( 0.571, 0.000, 0.000),( 0.714, 1.000, 1.000),( 0.857, 0.000, 0.000),( 1.000, 1.000, 1.000)),
        #'green':(( 0.000, 1.000, 1.000),( 0.143, 0.000, 0.000),( 0.286, 1.000, 1.000),( 0.429, 0.000, 0.000),( 0.571, 1.000, 1.000),( 0.714, 0.000, 0.000),( 0.857, 1.000, 1.000),( 1.000, 1.000, 1.000)),
        #'blue':(( 0.000, 1.000, 1.000),( 0.143, 1.000, 1.000),( 0.286, 0.000, 0.000),( 0.429, 0.000, 0.000),( 0.571, 1.000, 1.000),( 0.714, 1.000, 1.000),( 0.857, 0.000, 0.000),( 1.000, 1.000, 1.000))}
        
        #The jet Colormap
        #self.ctof = {'blue': ((0.0, 0.5, 0.5), (0.11, 1, 1), (0.34, 1, 1), (0.65, 0, 0), (1, 0, 0)), 'green': ((0.0, 0, 0), (0.125, 0, 0), (0.375, 1, 1), (0.64, 1, 1), (0.91, 0, 0), (1, 0, 0)), 'red': ((0.0, 0, 0), (0.35, 0, 0), (0.66, 1, 1), (0.89, 1, 1), (1, 0.5, 0.5))}
        
        #Especial jet
        self.ctof = {'red':(( 0.000, 0.973, 0.973),( 0.016, 0.647, 0.647),( 0.032, 0.325, 0.325),( 0.048, 0.000, 0.000),( 0.063, 0.000, 0.000),( 0.079, 0.000, 0.000),( 0.095, 0.000, 0.000),( 0.111, 0.000, 0.000),( 0.127, 0.000, 0.000),( 0.143, 0.000, 0.000),( 0.159, 0.000, 0.000),( 0.175, 0.000, 0.000),( 0.190, 0.000, 0.000),( 0.206, 0.000, 0.000),( 0.222, 0.000, 0.000),( 0.238, 0.000, 0.000),( 0.254, 0.000, 0.000),( 0.270, 0.000, 0.000),( 0.286, 0.000, 0.000),( 0.302, 0.000, 0.000),( 0.317, 0.000, 0.000),( 0.333, 0.000, 0.000),( 0.349, 0.000, 0.000),( 0.365, 0.000, 0.000),( 0.381, 0.063, 0.063),( 0.397, 0.125, 0.125),( 0.413, 0.188, 0.188),( 0.429, 0.251, 0.251),( 0.444, 0.314, 0.314),( 0.460, 0.376, 0.376),( 0.476, 0.439, 0.439),( 0.492, 0.502, 0.502),( 0.508, 0.561, 0.561),( 0.524, 0.624, 0.624),( 0.540, 0.686, 0.686),( 0.556, 0.749, 0.749),( 0.571, 0.812, 0.812),( 0.587, 0.875, 0.875),( 0.603, 0.937, 0.937),( 0.619, 1.000, 1.000),( 0.635, 1.000, 1.000),( 0.651, 1.000, 1.000),( 0.667, 1.000, 1.000),( 0.683, 1.000, 1.000),( 0.698, 1.000, 1.000),( 0.714, 1.000, 1.000),( 0.730, 1.000, 1.000),( 0.746, 1.000, 1.000),( 0.762, 1.000, 1.000),( 0.778, 1.000, 1.000),( 0.794, 1.000, 1.000),( 0.810, 1.000, 1.000),( 0.825, 1.000, 1.000),( 0.841, 1.000, 1.000),( 0.857, 1.000, 1.000),( 0.873, 1.000, 1.000),( 0.889, 0.937, 0.937),( 0.905, 0.875, 0.875),( 0.921, 0.812, 0.812),( 0.937, 0.749, 0.749),( 0.952, 0.686, 0.686),( 0.968, 0.624, 0.624),( 0.984, 0.561, 0.561),( 1.000, 0.502, 0.502)),
        'green':(( 0.000, 0.973, 0.973),( 0.016, 0.647, 0.647),( 0.032, 0.325, 0.325),( 0.048, 0.000, 0.000),( 0.063, 0.000, 0.000),( 0.079, 0.000, 0.000),( 0.095, 0.000, 0.000),( 0.111, 0.000, 0.000),( 0.127, 0.063, 0.063),( 0.143, 0.125, 0.125),( 0.159, 0.188, 0.188),( 0.175, 0.251, 0.251),( 0.190, 0.314, 0.314),( 0.206, 0.376, 0.376),( 0.222, 0.439, 0.439),( 0.238, 0.502, 0.502),( 0.254, 0.561, 0.561),( 0.270, 0.624, 0.624),( 0.286, 0.686, 0.686),( 0.302, 0.749, 0.749),( 0.317, 0.812, 0.812),( 0.333, 0.875, 0.875),( 0.349, 0.937, 0.937),( 0.365, 1.000, 1.000),( 0.381, 1.000, 1.000),( 0.397, 1.000, 1.000),( 0.413, 1.000, 1.000),( 0.429, 1.000, 1.000),( 0.444, 1.000, 1.000),( 0.460, 1.000, 1.000),( 0.476, 1.000, 1.000),( 0.492, 1.000, 1.000),( 0.508, 1.000, 1.000),( 0.524, 1.000, 1.000),( 0.540, 1.000, 1.000),( 0.556, 1.000, 1.000),( 0.571, 1.000, 1.000),( 0.587, 1.000, 1.000),( 0.603, 1.000, 1.000),( 0.619, 1.000, 1.000),( 0.635, 0.937, 0.937),( 0.651, 0.875, 0.875),( 0.667, 0.812, 0.812),( 0.683, 0.749, 0.749),( 0.698, 0.686, 0.686),( 0.714, 0.624, 0.624),( 0.730, 0.561, 0.561),( 0.746, 0.502, 0.502),( 0.762, 0.439, 0.439),( 0.778, 0.376, 0.376),( 0.794, 0.314, 0.314),( 0.810, 0.251, 0.251),( 0.825, 0.188, 0.188),( 0.841, 0.125, 0.125),( 0.857, 0.063, 0.063),( 0.873, 0.000, 0.000),( 0.889, 0.000, 0.000),( 0.905, 0.000, 0.000),( 0.921, 0.000, 0.000),( 0.937, 0.000, 0.000),( 0.952, 0.000, 0.000),( 0.968, 0.000, 0.000),( 0.984, 0.000, 0.000),( 1.000, 0.000, 0.000)),
        'blue':(( 0.000, 0.973, 0.973),( 0.016, 0.835, 0.835),( 0.032, 0.698, 0.698),( 0.048, 0.561, 0.561),( 0.063, 0.671, 0.671),( 0.079, 0.780, 0.780),( 0.095, 0.890, 0.890),( 0.111, 1.000, 1.000),( 0.127, 1.000, 1.000),( 0.143, 1.000, 1.000),( 0.159, 1.000, 1.000),( 0.175, 1.000, 1.000),( 0.190, 1.000, 1.000),( 0.206, 1.000, 1.000),( 0.222, 1.000, 1.000),( 0.238, 1.000, 1.000),( 0.254, 1.000, 1.000),( 0.270, 1.000, 1.000),( 0.286, 1.000, 1.000),( 0.302, 1.000, 1.000),( 0.317, 1.000, 1.000),( 0.333, 1.000, 1.000),( 0.349, 1.000, 1.000),( 0.365, 1.000, 1.000),( 0.381, 0.937, 0.937),( 0.397, 0.875, 0.875),( 0.413, 0.812, 0.812),( 0.429, 0.749, 0.749),( 0.444, 0.686, 0.686),( 0.460, 0.624, 0.624),( 0.476, 0.561, 0.561),( 0.492, 0.502, 0.502),( 0.508, 0.439, 0.439),( 0.524, 0.376, 0.376),( 0.540, 0.314, 0.314),( 0.556, 0.251, 0.251),( 0.571, 0.188, 0.188),( 0.587, 0.125, 0.125),( 0.603, 0.063, 0.063),( 0.619, 0.000, 0.000),( 0.635, 0.000, 0.000),( 0.651, 0.000, 0.000),( 0.667, 0.000, 0.000),( 0.683, 0.000, 0.000),( 0.698, 0.000, 0.000),( 0.714, 0.000, 0.000),( 0.730, 0.000, 0.000),( 0.746, 0.000, 0.000),( 0.762, 0.000, 0.000),( 0.778, 0.000, 0.000),( 0.794, 0.000, 0.000),( 0.810, 0.000, 0.000),( 0.825, 0.000, 0.000),( 0.841, 0.000, 0.000),( 0.857, 0.000, 0.000),( 0.873, 0.000, 0.000),( 0.889, 0.000, 0.000),( 0.905, 0.000, 0.000),( 0.921, 0.000, 0.000),( 0.937, 0.000, 0.000),( 0.952, 0.000, 0.000),( 0.968, 0.000, 0.000),( 0.984, 0.000, 0.000),( 1.000, 0.000, 0.000),)}
        
        cm_tof = mcol.LinearSegmentedColormap('cm_tof', self.ctof)
        #plt.register_cmap(cmap=cm_tof)
        #map1= np.array([[1.,1.,1.],[0,1.,0],[1.,1.,0],[1.,0,0],[0,1.,1.],[1.,0,1.],[0,0,1.],[1.,1.,1.]])
        #self.cm1=mcol.ListedColormap(map1, name=u'from_list', N=None)
        
        #My Events
        self.Bind(wx.EVT_MENU,self.events.OnOpen,self.appopenmenu)
        self.Bind(wx.EVT_MENU,self.events.OnQuit,self.appquitmenu)
        self.Bind(wx.EVT_MENU,self.events.OnPara,self.menparameters)
        self.Bind(wx.EVT_MENU,self.events.OnInte,self.menintegration)
        self.Bind(wx.EVT_MENU,self.events.OnCust,self.mencustomize)
        self.Bind(wx.EVT_TOOL,self.events.OnQuit,self.quittool)
        self.Bind(wx.EVT_TOOL,self.events.OnOpen,self.opentool)
        self.Bind(wx.EVT_TOOL,self.events.OnSave,self.savetool)
        self.button.Bind(wx.EVT_BUTTON,self.events.OnButtonClick)
        self.btnTransf1.Bind(wx.EVT_BUTTON, self.events.OnToggleClick)
        self.btnTransf2.Bind(wx.EVT_BUTTON, self.events.OnToggleClick)
        self.btnTransf3.Bind(wx.EVT_BUTTON, self.events.OnToggleClick)
        self.btnInt1.Bind(wx.EVT_BUTTON, self.events.OnToggleClick)
        self.btnInt2.Bind(wx.EVT_BUTTON, self.events.OnToggleClick)
        
       
class frmParameters(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self,None,-1,title='Parameters',pos=(0,0))
        self.parent = parent
        parPan = wx.Panel(self)
        #My Labels
        self.langle = wx.StaticText(parPan,-1,label=u'Angle[deg]  ')
        self.langle.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lsdd = wx.StaticText(parPan,-1,label=u'SDD[mm]  ')
        self.lsdd.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lpixel = wx.StaticText(parPan,-1,label=u'Pixel Size[mm]  ')
        self.lpixel.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lspec = wx.StaticText(parPan,-1,label=u'Specular [pix] ')
        self.lspec.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        #My Inputs
        self.angle = wx.TextCtrl(parPan,-1)
        self.valAN = parent.valAN
        self.angle.SetValue(str(parent.valAN[0]))
        self.angle.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.sdd = wx.TextCtrl(parPan,-1)
        self.valSDD = parent.valSDD
        self.sdd.SetValue(str(parent.valSDD[0]))
        self.sdd.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.pixel = wx.TextCtrl(parPan,-1)
        self.valPIX = parent.valPIX
        self.pixel.SetValue(str(parent.valPIX[0]))
        self.pixel.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.spec = wx.TextCtrl(parPan,-1)
        self.valSPE = parent.valSPE
        self.spec.SetValue(str(parent.valSPE[0]))
        self.spec.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))

        
        #My Selection
        self.llimx1 = wx.StaticText(parPan,-1,label=u'x1')
        self.llimx1.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.llimx2 = wx.StaticText(parPan,-1,label=u'  x2')
        self.llimx2.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.llimy1 = wx.StaticText(parPan,-1,label=u'y1')
        self.llimy1.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.llimy2 = wx.StaticText(parPan,-1,label=u'  y2')
        self.llimy2.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.limx1 = wx.TextCtrl(parPan,-1,value=u'0.0')
        self.limx1.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.limx2 = wx.TextCtrl(parPan,-1,value=u'0.0')
        self.limx2.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.limy1 = wx.TextCtrl(parPan,-1,value=u'0.0')
        self.limy1.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.limy2 = wx.TextCtrl(parPan,-1,value=u'0.0')
        self.limy2.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.ltolm = wx.StaticText(parPan,-1,label=u'  Mask[0-900]')
        self.ltolm.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.tolm = wx.TextCtrl(parPan,-1,value=u'0.0')
        self.tolm.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.tolm.SetValue('{:4.4f}'.format(self.parent.vtolm))
        self.cbnan = wx.CheckBox(parPan, -1, 'Clear Noise', (10, 10))
        self.cbnan.SetValue(False)
        
        #Initialization
        self.limx1.SetValue('{:4.4f}'.format(self.parent.cx1))
        self.limx2.SetValue('{:4.4f}'.format(self.parent.cx2))
        self.limy1.SetValue('{:4.4f}'.format(180*self.parent.cy1/np.pi))
        self.limy2.SetValue('{:4.4f}'.format(180*self.parent.cy2/np.pi))
        
        #Design
        self.wavy = wx.StaticBox(parPan,-1,label='Angle')
        self.wavy.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        parboxsizer =  wx.StaticBoxSizer(self.wavy,wx.VERTICAL)
        parboxsizer.SetMinSize((100,160))
        sizer = wx.GridBagSizer(hgap=1,vgap=1)
        sizer.Add(self.langle,(0,0),(1,1),wx.EXPAND)
        sizer.Add(self.angle,(0,1),(1,1),wx.EXPAND)
        sizer.Add(self.lsdd,(1,0),(1,1),wx.EXPAND)
        sizer.Add(self.sdd,(1,1),(1,1),wx.EXPAND)
        sizer.Add(self.lpixel,(2,0),(1,1),wx.EXPAND)
        sizer.Add(self.pixel,(2,1),(1,1),wx.EXPAND)
        sizer.Add(self.lspec,(3,0),(1,1),wx.EXPAND)
        sizer.Add(self.spec,(3,1),(1,1),wx.EXPAND)
        parboxsizer.Add(sizer,-1,flag=wx.EXPAND|wx.ALL, border=10)

        self.crops = wx.StaticBox(parPan,-1,'Selection')
        self.crops.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        cropssizer =  wx.StaticBoxSizer(self.crops, wx.VERTICAL)
        cropssizer.SetMinSize((100,100))
        sizercrop = wx.GridBagSizer(1,1)
        sizercrop.Add(self.llimx1,(0,0),(1,1),wx.EXPAND)
        sizercrop.Add(self.limx1,(0,1),(1,1),wx.EXPAND)
        sizercrop.Add(self.llimx2,(0,2),(1,1),wx.EXPAND)
        sizercrop.Add(self.limx2,(0,3),(1,1),wx.EXPAND)
        sizercrop.Add(self.llimy1,(1,0),(1,1),wx.EXPAND)
        sizercrop.Add(self.limy1,(1,1),(1,1),wx.EXPAND)
        sizercrop.Add(self.llimy2,(1,2),(1,1),wx.EXPAND)
        sizercrop.Add(self.limy2,(1,3),(1,1),wx.EXPAND)
        cropssizer.Add(sizercrop,-1, flag=wx.EXPAND|wx.ALL, border=10)

        self.figures = wx.StaticBox(parPan,-1,'Figure')
        self.figures.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        figuressizer =  wx.StaticBoxSizer(self.figures, wx.VERTICAL)
        figuressizer.SetMinSize((100,200))
        sizerfigures = wx.GridBagSizer(1,1)
        sizerfigures.Add(cropssizer,(0,0),(1,3),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=5)
        sizerfigures.Add(self.ltolm,(1,0),(1,1),wx.EXPAND)
        sizerfigures.Add(self.tolm,(1,1),(1,1),wx.EXPAND)
        sizerfigures.Add(self.cbnan,(2,0),(1,1),wx.EXPAND)
        figuressizer.Add(sizerfigures,-1, flag=wx.EXPAND|wx.ALL, border=10)
        
        topSizer = wx.BoxSizer(wx.VERTICAL)
        root = wx.GridBagSizer(1,1)
        root.Add(parboxsizer,(0,0),(1,1),flag=wx.ALL|wx.EXPAND, border=5)
        root.Add(figuressizer,(1,0),(1,1),flag=wx.ALL|wx.EXPAND, border=5)
        topSizer.Add(root,0,wx.CENTER)
        parPan.SetSizer(topSizer)
        topSizer.Fit(self)
        
        self.Bind(wx.EVT_CLOSE, self.getPar)

    def getPar(self,event):
        f = np.pi/180.
        self.valAN[0] = self.angle.GetValue()
        self.valSPE[0] = self.spec.GetValue()
        self.valPIX[0] = self.pixel.GetValue()
        self.valSDD[0] = self.sdd.GetValue()
        self.parent.vtolm = float(self.tolm.GetValue())
        self.parent.cx1 = float(self.limx1.GetValue())
        self.parent.cx2 = float(self.limx2.GetValue())
        self.parent.cy1 = f*float(self.limy1.GetValue())
        self.parent.cy2 = f*float(self.limy2.GetValue())
        self.parent.ztonan = self.cbnan.GetValue()
        #self.parent.btnIntegration.SetLabel('hi')
        #print self.valWL[0]
        self.Destroy()
        
class frmIntegration(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self,None,-1,title='Integration',pos=(0,0))
        self.parent = parent
        intPan = wx.Panel(self)

        #My Labels
        self.llimx1 = wx.StaticText(intPan,-1,label=u'x1')
        self.llimx1.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.llimx2 = wx.StaticText(intPan,-1,label=u'x2')
        self.llimx2.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.llimy1 = wx.StaticText(intPan,-1,label=u'y1')
        self.llimy1.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.llimy2 = wx.StaticText(intPan,-1,label=u'y2')
        self.llimy2.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.limx1 = wx.TextCtrl(intPan,-1,value=u'0.0')
        self.limx1.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.limx2 = wx.TextCtrl(intPan,-1,value=u'0.0')
        self.limx2.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.limy1 = wx.TextCtrl(intPan,-1,value=u'0.0')
        self.limy1.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.limy2 = wx.TextCtrl(intPan,-1,value=u'0.0')
        self.limy2.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))        
        
        self.integration = wx.StaticBox(intPan,-1,'Integration')
        self.integration.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        intsizer =  wx.StaticBoxSizer(self.integration, wx.VERTICAL)
        intsizer.SetMinSize((50,180))
        sizerints = wx.GridBagSizer(5,5)
        sizerints.Add(self.llimx1,(0,0),(1,1),wx.EXPAND)
        sizerints.Add(self.limx1,(0,1),(1,1),wx.EXPAND)
        sizerints.Add(self.llimx2,(1,0),(1,1),wx.EXPAND)
        sizerints.Add(self.limx2,(1,1),(1,1),wx.EXPAND)
        sizerints.Add(self.llimy1,(2,0),(1,1),wx.EXPAND)
        sizerints.Add(self.limy1,(2,1),(1,1),wx.EXPAND)
        sizerints.Add(self.llimy2,(3,0),(1,1),wx.EXPAND)
        sizerints.Add(self.limy2,(3,1),(1,1),wx.EXPAND)
        intsizer.Add(sizerints,-1, flag=wx.EXPAND|wx.ALL, border=10)
        
        topSizer = wx.BoxSizer(wx.VERTICAL)
        root = wx.GridBagSizer(1,1)
        root.Add(intsizer,(0,0),(1,1),flag=wx.ALL|wx.EXPAND, border=5)
        topSizer.Add(root,0,wx.CENTER)
        intPan.SetSizer(topSizer)
        topSizer.Fit(self)
        
        self.Bind(wx.EVT_CLOSE, self.getPar)

    def getPar(self,event):
        self.parent.x1 = float(self.limx1.GetValue())
        self.parent.x2 = float(self.limx2.GetValue())
        self.parent.y1 = float(self.limy1.GetValue())
        self.parent.y2 = float(self.limy2.GetValue())
        self.Destroy()
       
class frmCustomize(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self,None,-1,title='Customize',pos=(0,0))
        self.parent = parent
        cusPan = wx.Panel(self)
        #My Labels
        self.lcmpmax = wx.StaticText(cusPan,-1,label=u'')
        self.lcmpmax.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lcmpmin = wx.StaticText(cusPan,-1,label=u'')
        self.lcmpmin.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lxmin = wx.StaticText(cusPan,-1,label=u'X-axis Min')
        self.lxmin.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lymin = wx.StaticText(cusPan,-1,label=u'Y-axis Min')
        self.lymin.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lxmax = wx.StaticText(cusPan,-1,label=u'X-axis Max')
        self.lxmax.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lymax = wx.StaticText(cusPan,-1,label=u'Y-axis Max')
        self.lymax.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lborder = wx.StaticText(cusPan,-1,label=u'Borderline')
        self.lborder.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lticksz = wx.StaticText(cusPan,-1,label=u'Font size')
        self.lticksz.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.llabelsz = wx.StaticText(cusPan,-1,label=u'Label size')
        self.llabelsz.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lticklg = wx.StaticText(cusPan,-1,label=u'Tick length')
        self.lticklg.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.ltickwd = wx.StaticText(cusPan,-1,label=u'Tick width')
        self.ltickwd.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lgam = wx.StaticText(cusPan,-1,label=u'Gamma')
        self.lgam.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.larat = wx.StaticText(cusPan,-1,label=u'Aspect')
        self.larat.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        #My Sliders(The current frequency is 100 -the fifth position in the args-)
        self.SlideCMLow = wx.Slider(cusPan,-1,0,0,100, style=wx.SL_VERTICAL, size=(-1,300))
        #self.SlideCMLow.SetTickFreq(10, 1)
        self.SlideCMUpp = wx.Slider(cusPan,-1,100,0,100, style=wx.SL_VERTICAL, size=(-1,300))
        #self.SlideCMUpp.SetTickFreq(10, 1)
        #My Plot Inputs
        self.xmin = wx.TextCtrl(cusPan,-1,value=wx.EmptyString)
        self.xmin.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.xmax = wx.TextCtrl(cusPan,-1,value=wx.EmptyString)
        self.xmax.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.ymin = wx.TextCtrl(cusPan,-1,value=wx.EmptyString)
        self.ymin.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.ymax = wx.TextCtrl(cusPan,-1,value=wx.EmptyString)
        self.ymax.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.border = wx.TextCtrl(cusPan,-1,value='2')
        self.border.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.ticksz = wx.TextCtrl(cusPan,-1,value='12')
        self.ticksz.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.labelsz = wx.TextCtrl(cusPan,-1,value='20')
        self.labelsz.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.ticklg = wx.TextCtrl(cusPan,-1,value='6')
        self.ticklg.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.tickwd = wx.TextCtrl(cusPan,-1,value='2')
        self.tickwd.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.gam = wx.TextCtrl(cusPan,-1,value=wx.EmptyString)
        self.gam.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.arat = wx.TextCtrl(cusPan,-1,value=wx.EmptyString)
        self.arat.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        #My Text Outputs
        self.cmpmax = wx.StaticText(cusPan,-1,label=u'None')
        self.cmpmax.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.cmpmin = wx.StaticText(cusPan,-1,label=u'None')
        self.cmpmin.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        #Initialization
        self.xmin.SetValue('{:4.4f}'.format(self.parent.xxmin))
        self.xmax.SetValue('{:4.4f}'.format(self.parent.xxmax))
        self.ymin.SetValue('{:4.4f}'.format(self.parent.yymin))
        self.ymax.SetValue('{:4.4f}'.format(self.parent.yymax))
        self.gam.SetValue(str(self.parent.gami))
        self.arat.SetValue(str(self.parent.aratio))
        self.lcmpmax.SetLabel('{:4.0f}'.format(self.parent.origu))
        self.lcmpmin.SetLabel('{:4.0f}'.format(self.parent.origl))
        
        #My Buttons
        self.btnScale = wx.ToggleButton(cusPan,-1,label='Log Scale')
        self.btnReplot = wx.Button(cusPan,-1,label='Replot',size=(100,30))
        self.btnReplot.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        #My Design
        self.slidebox = wx.StaticBox(cusPan,-1,label="")
        slideboxsizer =  wx.StaticBoxSizer(self.slidebox, wx.VERTICAL)
        slideboxsizer.SetMinSize((50,350))
        sizerslidebox = wx.GridBagSizer(hgap=2,vgap=2)
        sizerslidebox.Add(self.lcmpmax,(0,0),(1,2),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=2)
        sizerslidebox.Add(self.SlideCMUpp,(1,0),(4,2),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=2)
        sizerslidebox.Add(self.cmpmax,(5,0),(1,2),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=2)
        sizerslidebox.Add(self.lcmpmin,(0,2),(1,2),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=2)
        sizerslidebox.Add(self.SlideCMLow,(1,2),(4,2),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=2)
        sizerslidebox.Add(self.cmpmin,(5,2),(1,2),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=2)
        sizerslidebox.Add(self.btnScale,(6,0),(1,4),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=2)
        slideboxsizer.Add(sizerslidebox,-1, flag=wx.EXPAND|wx.ALL, border=2)

        self.cmapp = wx.StaticBox(cusPan,-1,'Plot')
        self.cmapp.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        mappsizer =  wx.StaticBoxSizer(self.cmapp, wx.VERTICAL)
        mappsizer.SetMinSize((100,350))
        sizermapp = wx.GridBagSizer(hgap=2,vgap=2)
        sizermapp.Add(slideboxsizer,(0,0),(12,1),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=2)
        sizermapp.Add(self.lxmin,(0,2),(1,1),wx.EXPAND)
        sizermapp.Add(self.xmin,(0,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=2)
        sizermapp.Add(self.lxmax,(1,2),(1,1),wx.EXPAND)
        sizermapp.Add(self.xmax,(1,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=2)
        sizermapp.Add(self.lymin,(2,2),(1,1),wx.EXPAND)
        sizermapp.Add(self.ymin,(2,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=2)
        sizermapp.Add(self.lymax,(3,2),(1,1),wx.EXPAND)
        sizermapp.Add(self.ymax,(3,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=2)
        sizermapp.Add(self.lticksz,(4,2),(1,1),wx.EXPAND)
        sizermapp.Add(self.ticksz,(4,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=2)
        sizermapp.Add(self.ltickwd,(5,2),(1,1),wx.EXPAND)
        sizermapp.Add(self.tickwd,(5,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=2)
        sizermapp.Add(self.lticklg,(6,2),(1,1),wx.EXPAND)
        sizermapp.Add(self.ticklg,(6,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=2)
        sizermapp.Add(self.lgam,(7,2),(1,1),wx.EXPAND)
        sizermapp.Add(self.gam,(7,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=2)
        sizermapp.Add(self.lborder,(8,2),(1,1),wx.EXPAND)
        sizermapp.Add(self.border,(8,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=2)
        sizermapp.Add(self.larat,(9,2),(1,1),wx.EXPAND)
        sizermapp.Add(self.arat,(9,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=2)
        sizermapp.Add(self.llabelsz,(10,2),(1,1),wx.EXPAND)
        sizermapp.Add(self.labelsz,(10,3),(1,1),flag=wx.RIGHT|wx.EXPAND, border=2)
        sizermapp.Add(self.btnReplot,(11,3),(1,1),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=2)
        mappsizer.Add(sizermapp,-1, flag=wx.EXPAND|wx.ALL, border=2)

        topSizer = wx.BoxSizer(wx.VERTICAL)
        root = wx.GridBagSizer(1,1)
        root.Add(mappsizer,(0,0),(1,1),flag=wx.ALL|wx.EXPAND, border=5)
        topSizer.Add(root,0,wx.CENTER)
        cusPan.SetSizer(topSizer)
        topSizer.Fit(self)
        
        self.btnReplot.Bind(wx.EVT_BUTTON,self.BtnReplotClick)
        self.Bind(wx.EVT_SCROLL_THUMBRELEASE,self.MapMaxDraw,self.SlideCMUpp)
        self.Bind(wx.EVT_SCROLL_THUMBRELEASE,self.MapMinDraw,self.SlideCMLow)
        
    def BtnReplotClick(self,event):
        self.parent.fonty = float(self.ticksz.GetValue())
        self.parent.bordy = float(self.border.GetValue())
        self.parent.tickw = float(self.tickwd.GetValue())
        self.parent.tickl = float(self.ticklg.GetValue())
        self.parent.xxmin = float(self.xmin.GetValue())
        self.parent.yymin = float(self.ymin.GetValue())
        self.parent.xxmax = float(self.xmax.GetValue())
        self.parent.yymax = float(self.ymax.GetValue())
        self.parent.aratio = float(self.arat.GetValue())
        self.parent.fontly = float(self.labelsz.GetValue())
        self.parent.GraphosAx.set_ylim([self.parent.yymin,self.parent.yymax])
        self.parent.GraphosAx.set_xlim([self.parent.xxmin,self.parent.xxmax])
        self.parent.GraphosAx.xaxis.set_major_locator(MaxNLocator(nbins=6))#tick numbers at the x-axis
        if (self.parent.btnInt1.GetValue() == False) and (self.parent.btnInt2.GetValue() == False):
            self.parent.GraphosAx.yaxis.set_major_locator(MaxNLocator(nbins=6))#tick numbers at the y-axis
            gam = float(self.gam.GetValue())
            #tupi = cm.jet._segmentdata
            cmap = mcol.LinearSegmentedColormap('name',self.parent.ctof,gamma=gam)
            self.parent.GraphoPP.set_cmap(cmap)
        for axis in ['top','bottom','left','right']:
            self.parent.GraphosAx.spines[axis].set_linewidth(self.parent.bordy)
        mpl.rcParams['axes.linewidth'] = self.parent.bordy
        #mpl.rcParams['axes.labelsize'] = self.parent.fontly
        self.parent.GraphoCBar.ax.tick_params(labelsize=self.parent.fonty,length=self.parent.tickl,width=self.parent.tickw)
        self.parent.GraphosAx.get_xaxis().set_tick_params(labelsize=self.parent.fonty,length=self.parent.tickl,width=self.parent.tickw)
        self.parent.GraphosAx.get_yaxis().set_tick_params(labelsize=self.parent.fonty,length=self.parent.tickl,width=self.parent.tickw)
        self.parent.GraphosAx.get_yaxis().set_tick_params(which=u'minor',labelsize=self.parent.fonty,length=0.8*self.parent.tickl,width=self.parent.tickw)
        self.parent.GraphosAx.get_xaxis().set_tick_params(which=u'minor',labelsize=self.parent.fonty,length=0.8*self.parent.tickl,width=self.parent.tickw)
        plt.xlabel(self.parent.GraphosAx.get_xlabel(),fontsize=self.parent.fontly)
        plt.xlabel(self.parent.GraphosAx.get_ylabel(),fontsize=self.parent.fontly)
        self.parent.GraphosAx.get_axes().set_aspect(self.parent.aratio)
        plt.tight_layout()
        self.parent.GraphoCBar.draw_all()
        plt.savefig(self.parent.imgfileout)
        plt.draw()
 
    def MapMaxDraw(self,event):
        val = self.SlideCMUpp.GetValue()
        lim1 = self.parent.cmlow
        lim2 = self.parent.cmupp
        if self.btnScale.GetValue() == True:
            realv = lim1 + val*(lim2-lim1)/100
            self.parent.cmmax = realv
            self.cmpmax.SetLabel('{:4.0f}'.format(np.power(10,realv)))
            self.parent.GraphoPP.set_clim(vmax=realv)
        else:
            realv = np.power(10,lim1)+val*(np.power(10,lim2)-np.power(10,lim1))/100
            self.cmpmax.SetLabel('{:4.0f}'.format(realv))
            self.parent.cmmax = np.log10(realv)
            self.parent.GraphoPP.set_clim(vmax=np.log10(realv))
        self.parent.GraphoCBar.draw_all()
        plt.savefig(self.parent.imgfileout)
        plt.draw()
    
    def MapMinDraw(self,event):
        val = self.SlideCMLow.GetValue()
        lim1 = self.parent.cmlow
        lim2 = self.parent.cmupp
        if self.btnScale.GetValue() == True:
            realv = lim1 + val*(lim2-lim1)/100
            self.parent.cmmin = realv
            self.cmpmin.SetLabel('{:4.0f}'.format(np.power(10,realv)))
            self.parent.GraphoPP.set_clim(vmin=realv)
        else:
            realv = np.power(10,lim1)+val*(np.power(10,lim2)-np.power(10,lim1))/100
            self.cmpmin.SetLabel('{:4.0f}'.format(realv))
            self.cmmin = np.log10(realv)
            self.parent.GraphoPP.set_clim(vmin=np.log10(realv))
        self.parent.GraphoCBar.draw_all()
        plt.savefig(self.parent.imgfileout)
        plt.draw()
        #self.Graphos.canvas.draw()

class EventH():
    def __init__(self,parent):
        self.parent = parent
        
    def OnPara(self,event):
        self.parent.child = frmParameters(self.parent)
        self.parent.child.Show()
    
    def OnInte(self,event):
        self.parent.child = frmIntegration(self.parent)
        self.parent.child.Show()
        
    def OnCust(self,event):
        self.parent.child = frmCustomize(self.parent)
        self.parent.child.Show()
        
    def OnOpen(self,event):
        dialog = wx.FileDialog(self.parent,"Choose a file",self.parent.dirname, '',"TEXT files (*.txt;*.xml)|*.txt;*.xml",wx.FD_MULTIPLE)
        if dialog.ShowModal() == wx.ID_OK:
            self.parent.filename = dialog.GetFilenames()
            #print self.parent.filename
            for i in range (2):
                #print self.parent.filename[i]
                if self.parent.filename[i].endswith('.xml'):
                    self.parent.myxml[0] = self.parent.filename[i].replace('.xml','')
                    #print self.parent.filename[i].replace('.xml','')
                if self.parent.filename[i].endswith('.txt'):
                    #print self.parent.mytxt[0]
                    self.parent.mytxt[0] = self.parent.filename[i].replace('.txt','')
                    #print self.parent.filename[i].replace('.txt','')
            Loading(self.parent,self.parent.filename)
    
    def OnSave(self,event):
        #print self.parent.myfiles[0]
        saveFileDialog = wx.FileDialog(self.parent, "Save DAT file", "", defaultFile=self.parent.myfiles,wildcard="DAT files (*.dat)|*.dat",style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
        if saveFileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed idea...
        #print saveFileDialog.GetDirectory()
        #There is file output for each button. Filename is created from the orginal one and the integration
            
    def OnQuit(self,event):
        self.parent.Close()
    
    def OnButtonClick(self,event):
        a = self.parent.btnTransf1.GetValue()
        b = self.parent.btnTransf2.GetValue()
        b2 = self.parent.btnTransf3.GetValue()
        c = self.parent.btnInt1.GetValue()
        d = self.parent.btnInt2.GetValue()
        if a==True or b==True or b2==True:
            Mapping(self.parent)
        if c==True or d==True:
            Integration(self.parent)

    def OnToggleClick(self,event):
        if self.parent.btnTransf1.GetValue():
            self.parent.btnTransf1.SetBackgroundColour('#DA3939')
            self.parent.btnTransf1.SetForegroundColour('white')
        else:
            self.parent.btnTransf1.SetBackgroundColour((240, 240, 240, 255))
            self.parent.btnTransf1.SetForegroundColour('black')
        if self.parent.btnTransf2.GetValue():
            self.parent.btnTransf2.SetBackgroundColour('#DA3939')
            self.parent.btnTransf2.SetForegroundColour('white')
        else:
            self.parent.btnTransf2.SetBackgroundColour((240, 240, 240, 255))
            self.parent.btnTransf2.SetForegroundColour('black')
        if self.parent.btnTransf3.GetValue():
            self.parent.btnTransf3.SetBackgroundColour('#DA3939')
            self.parent.btnTransf3.SetForegroundColour('white')
        else:
            self.parent.btnTransf3.SetBackgroundColour((240, 240, 240, 255))
            self.parent.btnTransf3.SetForegroundColour('black')
        if self.parent.btnInt1.GetValue():
            self.parent.btnInt1.SetBackgroundColour('#DA3939')
            self.parent.btnInt1.SetForegroundColour('white')
        else:
            self.parent.btnInt1.SetBackgroundColour((240, 240, 240, 255))
            self.parent.btnInt1.SetForegroundColour('black')   
        if self.parent.btnInt2.GetValue():
            self.parent.btnInt2.SetBackgroundColour('#DA3939')
            self.parent.btnInt2.SetForegroundColour('white')
        else:
            self.parent.btnInt2.SetBackgroundColour((240, 240, 240, 255))
            self.parent.btnInt2.SetForegroundColour('black')   
           
#===========================================================================
def Loading(parent,imagefile):
    mapp = {}
    xcol = {}
    ycol = {}
    img=open(parent.myxml[0]+".xml",'r')
    xmlf=str(img.read())
    h0 = xmlf.find('<X_coord')
    h1 = xmlf[h0:].find('\n')
    h2 = xmlf.find('</X_coord>')
    val = xmlf[h0+h1:h2].split()
    col = np.array(val).astype('float')
    h0 = xmlf.find('<Y_coord')
    h1 = xmlf[h0:].find('\n')
    h2 = xmlf.find('</Y_coord>')
    val = xmlf[h0+h1:h2].split()
    row = np.array(val).astype('float')
    img=open(parent.mytxt[0]+".txt",'r')
    txtf=str(img.read())
    val = txtf.split()
    mat = np.array(val).astype('float')
    ima = mat.reshape(len(row),len(col))
    #imac = ima[ ::-1,:]
    #imac = np.rot90(ima)
    plt.close()
    fig = plt.figure(figsize=(8,4), dpi=120)
    ax = fig.add_subplot(111)
    plt.imshow(np.flipud(ima), interpolation='none', cmap = cm.jet, norm=mcol.LogNorm(), aspect=len(col)/(len(row)*1.))
    plt.show()
    mapp[1]= ima
    #Allocate data in array
    parent.workmx = mapp
    parent.workcl = col
    parent.workrw = row
    #Flush memory
    del mapp, ima   


def Mapping(parent):
    f = np.pi/180.#degree to radian
    tlt=f*float(parent.valAN[0])
    sdd=float(parent.valSDD[0])
    pix=float(parent.valPIX[0])
    spe=float(parent.valSPE[0])
    mapp = parent.workmx
    wlength = parent.workcl
    pixang = 2.*tlt*pix/(sdd*np.tan(2.*tlt))
    dim1, dim2 = parent.workmx[1].shape
    afp = tlt+(parent.workrw-dim1+spe+1)*pixang
    dim3 = len(mapp)
    wl, af2 = np.meshgrid(wlength,afp)
    #print pixang/f,afp/f
    qx = 2.*np.pi*(np.cos(af2)-np.cos(tlt))/wl
    qz = 2.*np.pi*(np.sin(af2)+np.sin(tlt))/wl
    qxz = np.zeros(qx.shape)
    for i in range (dim1):
        for j in range(dim2):
            if qz[i,j]!=0:
                qxz[i,j]= np.sign(qx[i,j])*np.absolute(qx[i,j]/qz[i,j])
            else:
                #qxz[i,j]=np.absolute(qx[i,j]/1e-14)
                qxz[i,j]=np.nan
    vaf = np.ravel(af2)
    vai = np.ravel(wl)
    vqx = np.ravel(qx)
    vqz = np.ravel(qz)
    vqxz = np.ravel(qxz)
    del tlt, af2
    #Clipping data cloud
    val={}
    ptaif={}
    ptqxz={}
    ptqxzz={}
    masks = {}
    if parent.btnTransf1.GetValue() == True:
        parent.axisyw = afp
        parent.axisxw = wlength
        parent.axisyy = afp
        parent.axisxx = wlength
        l=0
        if parent.ztonan:
            noise = 1#np.log10(np.amax(mapp[1]))/2
            mapp[1][mapp[1]<noise] = noise
        parent.plotmif[1+l] = mapp[1]
        parent.intdata = parent.plotmif

    if parent.btnTransf2.GetValue() == True:
        f = np.pi/180.#degree to radian
        tlt=f*float(parent.valAN[0])
        parent.idTransf = 2
        l=0
        trl = -1
        if parent.cy1 != 0 or parent.cy2 != 0: 
            i1,i2=0,0
            while parent.cy1 >= parent.axisyw[i1]:
                a,i1=i1+trl,i1+1
            while parent.cy2 >= parent.axisyw[i2]:
                b,i2=i2+trl,i2+1
            if parent.cx1 != 0 or parent.cx2 != 0: 
                i1,i2=0,0
                while parent.cx1 >= parent.axisxw[i1]:
                    c,i1=i1+trl,i1+1
                while parent.cx2 >= parent.axisxw[i2]:
                    d,i2=i2+trl,i2+1
            else:
                c, d = 0, len(parent.axisxw)
        else:
            a, b = 0, len(parent.axisyw)
            if parent.cx1 != 0 or parent.cx2 != 0: 
                i1,i2=0,0
                #c, d = 0, len(parent.axisxx)
                while parent.cx1 >= parent.axisxw[i1]:
                    c,i1=i1+trl,i1+1
                while parent.cx2 >= parent.axisxw[i2]:
                    d,i2=i2+trl,i2+1    
            else:
                c, d = 0, len(parent.axisxw)
        #print parent.axisxx 
        mapp[l+1]=parent.plotmif[1+l][a:b,c:d]
        dim1, dim2 = mapp[1+l].shape
        wl, af2 = np.meshgrid(parent.axisxw[c:d], parent.axisyw[a:b])    
        #print tlt
        qx = 2.*np.pi*(np.cos(af2)-np.cos(tlt))/wl
        qz = 2.*np.pi*(np.sin(af2)+np.sin(tlt))/wl
        vqx = np.ravel(qx)
        vqz = np.ravel(qz)
        ddx, ddy = 2000,2000#max(dim1, dim2), max(dim1, dim2)          
        qxp = np.linspace(min(vqx), max(vqx),ddx)
        qzp = np.linspace(min(vqz), max(vqz),ddy)
        #print dim1,dim2, ddx, ddy, len(qxp), len(vqx), dim1*dim2
        #Divide the image in 8 regions
        ly = np.array([ddy/2,ddy-1,0,ddy/2])
        lx = np.array([0,ddx/4,ddx/4,ddx/2,ddx/2,3*ddx/4,3*ddx/4,ddx-1])
        mask = 1000*np.ones(mapp[l+1].shape)
        mask[0:1,:] = 1
        mask[:,0:1] = 1
        mask[dim1-1:dim1,:] = 1
        mask[:,dim2-1:dim2] = 1
        values = np.ravel(mapp[l+1])
        maski = np.ravel(mask)
        # Tolerance for the points
        t=10
        # Data cloud for each region
        index = []
        for i in range (0,dim1*dim2):
            if (vqx[i]<qxp[lx[0]]) or (vqx[i]>qxp[lx[1]+t]) or (vqz[i]<qzp[ly[0]-t]) or (vqz[i]>qzp[ly[1]]):
                index.append(i)
        val[str(10000+l)]=np.delete(values,index)
        masks[str(10000+l)]=np.delete(maski,index)
        ptqxz[str(10000+l)]=np.array([np.delete(vqx,index),np.delete(vqz,index)])
        index = []
        for i in range (0,dim1*dim2):
            if (vqx[i]<qxp[lx[2]-t]) or (vqx[i]>qxp[lx[3]+t]) or (vqz[i]<qzp[ly[0]-t]) or (vqz[i]>qzp[ly[1]]):
                index.append(i)
        val[str(20000+l)]=np.delete(values,index)
        masks[str(20000+l)]=np.delete(maski,index)
        ptqxz[str(20000+l)]=np.array([np.delete(vqx,index),np.delete(vqz,index)])
        index = []
        for i in range (0,dim1*dim2):
            if (vqx[i]<qxp[lx[4]-t]) or (vqx[i]>qxp[lx[5]+t]) or (vqz[i]<qzp[ly[0]-t]) or (vqz[i]>qzp[ly[1]]):
                index.append(i)
        val[str(30000+l)]=np.delete(values,index)
        masks[str(30000+l)]=np.delete(maski,index)
        ptqxz[str(30000+l)]=np.array([np.delete(vqx,index),np.delete(vqz,index)])
        index = []
        for i in range (0,dim1*dim2):
            if (vqx[i]<qxp[lx[6]-t]) or (vqx[i]>qxp[lx[7]]) or (vqz[i]<qzp[ly[0]-t]) or (vqz[i]>qzp[ly[1]]):
                index.append(i)
        val[str(40000+l)]=np.delete(values,index)
        masks[str(40000+l)]=np.delete(maski,index)
        ptqxz[str(40000+l)]=np.array([np.delete(vqx,index),np.delete(vqz,index)])
        # Data cloud for each region
        index = []
        for i in range (0,dim1*dim2):
            if (vqx[i]<qxp[lx[0]]) or (vqx[i]>qxp[lx[1]+t]) or (vqz[i]<qzp[ly[2]]) or (vqz[i]>qzp[ly[3]+t]):
                index.append(i)
        val[str(50000+l)]=np.delete(values,index)
        masks[str(50000+l)]=np.delete(maski,index)
        ptqxz[str(50000+l)]=np.array([np.delete(vqx,index),np.delete(vqz,index)])
        index = []
        for i in range (0,dim1*dim2):
            if (vqx[i]<qxp[lx[2]-t]) or (vqx[i]>qxp[lx[3]+t]) or (vqz[i]<qzp[ly[2]]) or (vqz[i]>qzp[ly[3]+t]):
                index.append(i)
        val[str(60000+l)]=np.delete(values,index)
        masks[str(60000+l)]=np.delete(maski,index)
        ptqxz[str(60000+l)]=np.array([np.delete(vqx,index),np.delete(vqz,index)])
        index = []
        for i in range (0,dim1*dim2):
            if (vqx[i]<qxp[lx[4]-t]) or (vqx[i]>qxp[lx[5]+t]) or (vqz[i]<qzp[ly[2]]) or (vqz[i]>qzp[ly[3]+t]):
                index.append(i)
        val[str(70000+l)]=np.delete(values,index)
        masks[str(70000+l)]=np.delete(maski,index)
        ptqxz[str(70000+l)]=np.array([np.delete(vqx,index),np.delete(vqz,index)])
        index = []
        for i in range (0,dim1*dim2):
            if (vqx[i]<qxp[lx[6]-t]) or (vqx[i]>qxp[lx[7]]) or (vqz[i]<qzp[ly[2]]) or (vqz[i]>qzp[ly[3]+t]):
                index.append(i)
        val[str(80000+l)]=np.delete(values,index)
        masks[str(80000+l)]=np.delete(maski,index)
        ptqxz[str(80000+l)]=np.array([np.delete(vqx,index),np.delete(vqz,index)])
   
    if parent.btnTransf3.GetValue() == True:
        f = np.pi/180.#degree to radian
        tlt=f*float(parent.valAN[0])
        parent.idTransf = 3
        l=0
        trl= -1
        if parent.cy1 != 0 or parent.cy2 != 0: 
            i1,i2=0,0
            while parent.cy1 >= parent.axisyw[i1]:
                a,i1=i1+trl,i1+1
            while parent.cy2 >= parent.axisyw[i2]:
                b,i2=i2+trl,i2+1
            if parent.cx1 != 0 or parent.cx2 != 0: 
                i1,i2=0,0
                while parent.cx1 >= parent.axisxw[i1]:
                    c,i1=i1+trl,i1+1
                while parent.cx2 >= parent.axisxw[i2]:
                    d,i2=i2+trl,i2+1
            else:
                c, d = 0, len(parent.axisxw)
        else:
            a, b = 0, len(parent.axisyw)
            if parent.cx1 != 0 or parent.cx2 != 0: 
                i1,i2=0,0
                while parent.cx1 >= parent.axisxw[i1]:
                    c,i1=i1+trl,i1+1
                while parent.cx2 >= parent.axisxw[i2]:
                    d,i2=i2+trl,i2+1    
            else:
                c, d = 0, len(parent.axisxw)
        mapp[l+1]=parent.plotmif[1+l][a:b,c:d]
        dim1, dim2 = mapp[1+l].shape
        wl, af2 = np.meshgrid(parent.axisxw[c:d], parent.axisyw[a:b])    
        #print q
        qx = 2.*np.pi*(np.cos(af2)-np.cos(tlt))/wl
        qz = 2.*np.pi*(np.sin(af2)+np.sin(tlt))/wl
        qxz = np.zeros(qx.shape)
        for i in range (dim1):
            for j in range(dim2):
                if qz[i,j]!=0:
                    qxz[i,j]= qx[i,j]/qz[i,j]
                else:
                    #qxz[i,j]=np.absolute(qx[i,j]/1e-14)
                    qxz[i,j]=np.nan
        vqxz = np.ravel(qxz)
        vqz = np.ravel(qz)
        ddx, ddy = 2000,2000#max(dim1, dim2), max(dim1, dim2)          
        qxzp = np.linspace(min(vqxz), max(vqxz),ddx)
        qzp = np.linspace(min(vqz), max(vqz),ddy)
        #print dim1,dim2, ddx, ddy, len(qxp), len(vqx), dim1*dim2
        #Divide the image in 8 regions
        ly = np.array([ddy/2,ddy-1,0,ddy/2])
        lx = np.array([0,ddx/4,ddx/4,ddx/2,ddx/2,3*ddx/4,3*ddx/4,ddx-1])            
        mask = 1000*np.ones(mapp[l+1].shape)
        mask[0:1,:] = 1
        mask[:,0:1] = 1
        mask[dim1-1:dim1,:] = 1
        mask[:,dim2-1:dim2] = 1
        values = np.ravel(mapp[l+1])
        maski = np.ravel(mask)
        #for i in range (0,dim1*dim2):
            #if values[i] == 0 :
                #values[i] = np.nan
        # Tolerance for the points
        t=20
        # Data cloud for each region
        index = []
        for i in range (0,dim1*dim2):
            if (vqxz[i]<qxzp[lx[0]]) or (vqxz[i]>qxzp[lx[1]+t]) or (vqz[i]<qzp[ly[0]-t]) or (vqz[i]>qzp[ly[1]]):
                index.append(i)
        val[str(10000+l)]=np.delete(values,index)
        masks[str(10000+l)]=np.delete(maski,index)
        ptqxzz[str(10000+l)]=np.array([np.delete(vqxz,index),np.delete(vqz,index)])
        index = []
        for i in range (0,dim1*dim2):
            if (vqxz[i]<qxzp[lx[2]-t]) or (vqxz[i]>qxzp[lx[3]+t]) or (vqz[i]<qzp[ly[0]-t]) or (vqz[i]>qzp[ly[1]]):
                index.append(i)
        val[str(20000+l)]=np.delete(values,index)
        masks[str(20000+l)]=np.delete(maski,index)
        ptqxzz[str(20000+l)]=np.array([np.delete(vqxz,index),np.delete(vqz,index)])
        index = []
        for i in range (0,dim1*dim2):
            if (vqxz[i]<qxzp[lx[4]-t]) or (vqxz[i]>qxzp[lx[5]+t]) or (vqz[i]<qzp[ly[0]-t]) or (vqz[i]>qzp[ly[1]]):
                index.append(i)
        val[str(30000+l)]=np.delete(values,index)
        masks[str(30000+l)]=np.delete(maski,index)
        ptqxzz[str(30000+l)]=np.array([np.delete(vqxz,index),np.delete(vqz,index)])
        index = []
        for i in range (0,dim1*dim2):
            if (vqxz[i]<qxzp[lx[6]-t]) or (vqxz[i]>qxzp[lx[7]]) or (vqz[i]<qzp[ly[0]-t]) or (vqz[i]>qzp[ly[1]]):
                index.append(i)
        val[str(40000+l)]=np.delete(values,index)
        masks[str(40000+l)]=np.delete(maski,index)
        ptqxzz[str(40000+l)]=np.array([np.delete(vqxz,index),np.delete(vqz,index)])
        # Data cloud for each region
        index = []
        for i in range (0,dim1*dim2):
            if (vqxz[i]<qxzp[lx[0]]) or (vqxz[i]>qxzp[lx[1]+t]) or (vqz[i]<qzp[ly[2]]) or (vqz[i]>qzp[ly[3]+t]):
                index.append(i)
        val[str(50000+l)]=np.delete(values,index)
        masks[str(50000+l)]=np.delete(maski,index)
        ptqxzz[str(50000+l)]=np.array([np.delete(vqxz,index),np.delete(vqz,index)])
        index = []
        for i in range (0,dim1*dim2):
            if (vqxz[i]<qxzp[lx[2]-t]) or (vqxz[i]>qxzp[lx[3]+t]) or (vqz[i]<qzp[ly[2]]) or (vqz[i]>qzp[ly[3]+t]):
                index.append(i)
        val[str(60000+l)]=np.delete(values,index)
        masks[str(60000+l)]=np.delete(maski,index)
        ptqxzz[str(60000+l)]=np.array([np.delete(vqxz,index),np.delete(vqz,index)])
        index = []
        for i in range (0,dim1*dim2):
            if (vqxz[i]<qxzp[lx[4]-t]) or (vqxz[i]>qxzp[lx[5]+t]) or (vqz[i]<qzp[ly[2]]) or (vqz[i]>qzp[ly[3]+t]):
                index.append(i)
        val[str(70000+l)]=np.delete(values,index)
        masks[str(70000+l)]=np.delete(maski,index)
        ptqxzz[str(70000+l)]=np.array([np.delete(vqxz,index),np.delete(vqz,index)])
        index = []
        for i in range (0,dim1*dim2):
            if (vqxz[i]<qxzp[lx[6]-t]) or (vqxz[i]>qxzp[lx[7]]) or (vqz[i]<qzp[ly[2]]) or (vqz[i]>qzp[ly[3]+t]):
                index.append(i)
        val[str(80000+l)]=np.delete(values,index)
        masks[str(80000+l)]=np.delete(maski,index)
        ptqxzz[str(80000+l)]=np.array([np.delete(vqxz,index),np.delete(vqz,index)])
                        
    # Mapping with the new coordinates
    tolm=parent.vtolm#tolerance of the mask
    if parent.btnTransf2.GetValue() == True:
        dqxp={}
        dqzp={}
        gx={}
        gy={}
        mx={}
        parent.axisyy = qzp[ly[2]:ly[1]]
        l=0
        for r in range (0,4):
            #print r
            key1,key2 = str(10000*(r+1)+l),str(10000*(r+5)+l)
            dqxp[key1] = qxp[lx[2*r]:lx[2*r+1]]
            dqxp[key2] = qxp[lx[2*r]:lx[2*r+1]]
            dqzp[key1] = qzp[ly[0]:ly[1]]
            dqzp[key2] = qzp[ly[2]:ly[3]]
            gx[key1], gy[key1] = np.meshgrid(dqxp[key1], dqzp[key1])
            gx[key2], gy[key2] = np.meshgrid(dqxp[key2], dqzp[key2])
            #print val[key2].size, ptqxz[key2].size
            mx[key1] = np.nan*np.ones(gx[key1].shape)
            mx[key2] = np.nan*np.ones(gx[key2].shape)
            mask1 = np.nan*np.ones(gx[key1].shape)
            mask2 = np.nan*np.ones(gx[key2].shape)
            #print ptqxz[key1].shape, val[key1].shape, gx[key1].shape
            if val[key1].size != 0:
                mx[key1] = griddata(ptqxz[key1].T, val[key1], (gx[key1], gy[key1]), method='linear')
                mask1 = griddata(ptqxz[key1].T, masks[key1], (gx[key1], gy[key1]), method='linear')
                mask1 = np.nan_to_num(mask1)
                mx[key1][mask1<tolm] = np.nan
            if val[key2].size != 0:
                mx[key2] = griddata(ptqxz[key2].T, val[key2], (gx[key2], gy[key2]), method='linear')
                mask2 = griddata(ptqxz[key2].T, masks[key2], (gx[key2], gy[key2]), method='linear')
                mask2 = np.nan_to_num(mask2)
                mx[key2][mask2<tolm] = np.nan 
        #print mx['40000']
        g11,g12,g13,g14 = mx[str(10000+l)],mx[str(20000+l)],mx[str(30000+l)],mx[str(40000+l)]
        g21,g22,g23,g24 = mx[str(50000+l)],mx[str(60000+l)],mx[str(70000+l)],mx[str(80000+l)]
        sub_g1 = np.concatenate((g11,g12,g13,g14), axis=1)
        sub_g2 = np.concatenate((g21,g22,g23,g24), axis=1)
        grid = np.concatenate((sub_g2,sub_g1), axis=0)
        overall = np.nan_to_num(grid)
        parent.plotmxz[l+1] = overall
        parent.intdata = parent.plotmxz
 
    if parent.btnTransf3.GetValue() == True:    
        dxp={}
        dyp={}
        gx={}
        gy={}
        mx={}
        parent.axisyy = qzp[ly[2]:ly[1]]
        l=0
        for r in range (0,4):
            key1,key2 = str(10000*(r+1)+l),str(10000*(r+5)+l)
            dxp[key1] = qxzp[lx[2*r]:lx[2*r+1]]
            dxp[key2] = qxzp[lx[2*r]:lx[2*r+1]]
            dyp[key1] = qzp[ly[0]:ly[1]]
            dyp[key2] = qzp[ly[2]:ly[3]]
            gx[key1], gy[key1] = np.meshgrid(dxp[key1], dyp[key1])
            gx[key2], gy[key2] = np.meshgrid(dxp[key2], dyp[key2])
            mx[key1] = np.nan*np.ones(gx[key1].shape)
            mx[key2] = np.nan*np.ones(gx[key2].shape)
            mask1 = np.nan*np.ones(gx[key1].shape)
            mask2 = np.nan*np.ones(gx[key2].shape)
            if val[key1].size != 0:
                mx[key1] = griddata(ptqxzz[key1].T, val[key1], (gx[key1], gy[key1]), method='linear')
                mask1 = griddata(ptqxzz[key1].T, masks[key1], (gx[key1], gy[key1]), method='linear')
                mask1 = np.nan_to_num(mask1)
                mx[key1][mask1<tolm] = np.nan
            if val[key2].size != 0:
                mx[key2] = griddata(ptqxzz[key2].T, val[key2], (gx[key2], gy[key2]), method='linear')
                mask2 = griddata(ptqxzz[key2].T, masks[key2], (gx[key2], gy[key2]), method='linear')
                mask2 = np.nan_to_num(mask2)
                mx[key2][mask2<tolm] = np.nan
        #print mx['40000']
        g11,g12,g13,g14 = mx[str(10000+l)],mx[str(20000+l)],mx[str(30000+l)],mx[str(40000+l)]
        g21,g22,g23,g24 = mx[str(50000+l)],mx[str(60000+l)],mx[str(70000+l)],mx[str(80000+l)]
        sub_g1 = np.concatenate((g11,g12,g13,g14), axis=1)
        sub_g2 = np.concatenate((g21,g22,g23,g24), axis=1)
        grid = np.concatenate((sub_g2,sub_g1), axis=0)
        overall = np.nan_to_num(grid)
        parent.plotmxzz[1+l] = overall
        parent.intdata = parent.plotmxzz
            
    #======================================================================================            
    # Make the plot
    
    if parent.btnTransf2.GetValue() == True:
        parent.axisxx = qxp[lx[0]:lx[7]]
        intvx = np.absolute(qxp[1]-qxp[0])
        intvy = np.absolute(qzp[1]-qzp[0])
        parent.xxmin = ax = min(qxp)
        parent.yymin = ay = min(qzp)
        parent.xxmax = bx = max(qxp)
        parent.yymax = by = max(qzp)
        info = dict(qx_min = min(qxp), qx_max = max(qxp), qz_min = min(qzp), qz_max = max(qzp))
        info = json.dumps(info)
        gam = parent.gami
        rati = parent.aratio = np.absolute((qxp[1]-qxp[0])/(qzp[1]-qzp[0]))
        l=0
        parent.Graphos = plt.figure(num=None, figsize=(10,8), dpi=120)
        parent.GraphosAx = parent.Graphos.add_subplot(111)
        mini = np.amin(parent.plotmxz[l+1])
        mx_plot = np.log10(parent.plotmxz[l+1]-mini+1)
        parent.origu = np.amax(parent.plotmxz[l+1]-mini+1)
        parent.origl = np.amin(parent.plotmxz[l+1]-mini+1)
        mx1 = (2**16-1)*(parent.plotmxz[l+1] - np.min(np.min(parent.plotmxz[l+1])))/np.max(np.max(parent.plotmxz[l+1]))
        mx = np.flipud(mx1).astype('uint16')
        filename = parent.myxml[l]+"_qxz.tif"
        tifff(mx,filename,info)  
        parent.cmlow = np.amin(mx_plot)
        parent.cmupp = np.amax(mx_plot)
        parent.cmmin = parent.cmlow
        parent.cmmax = parent.cmupp
        #tupi = cm.jet._segmentdata
        cmap = mcol.LinearSegmentedColormap('name',parent.ctof,gamma=gam)
        #cmap = mcol.LinearSegmentedColormap('name',tupi,gamma=gam)
        parent.GraphoPP = plt.imshow(np.flipud(mx_plot),interpolation='none',cmap=cmap,extent=[ax,bx,ay,by],aspect=rati)
        plt.xlabel('$q_{x}$ [$\AA^{-1}$]',fontsize=parent.fontly)
        plt.ylabel('$q_{z}$ [$\AA^{-1}$]',fontsize=parent.fontly)
        parent.GraphoCBar = plt.colorbar(parent.GraphoPP, shrink=1,aspect=30)
        for axis in ['top','bottom','left','right']:
            parent.GraphosAx.spines[axis].set_linewidth(parent.bordy)
        parent.GraphoCBar.outline.set_linewidth(parent.bordy)
        parent.GraphoCBar.ax.tick_params(labelsize=parent.fonty,length=parent.tickl,width=parent.tickw)
        parent.GraphosAx.get_xaxis().set_tick_params(labelsize=parent.fonty,length=parent.tickl,width=parent.tickw)
        parent.GraphosAx.get_yaxis().set_tick_params(labelsize=parent.fonty,length=parent.tickl,width=parent.tickw)
        parent.GraphosAx.get_yaxis().set_tick_params(which=u'minor',labelsize=parent.fonty,length=0.8*parent.tickl,width=parent.tickw)
        parent.GraphosAx.get_xaxis().set_tick_params(which=u'minor',labelsize=parent.fonty,length=0.8*parent.tickl,width=parent.tickw)
        plt.tight_layout()
        parent.imgfileout = parent.myxml[l]+"_qxz.png"
        plt.savefig(parent.imgfileout)
        plt.show()
                    
    if parent.btnTransf1.GetValue() == True:
        f = 180/np.pi
        intvx = np.absolute(wlength[1]-wlength[0])
        intvy = np.absolute(afp[1]-afp[0])
        parent.xxmin = ax = min(wlength)
        parent.yymin = ay = f*min(afp)
        parent.xxmax = bx = max(wlength)+intvx
        parent.yymax = by = f*max(afp)+f*intvy
        info = dict(x_min = min(wlength), x_max = max(wlength), y_min = min(afp), y_max = max(afp))
        info = json.dumps(info)
        gam = parent.gami
        rati = parent.aratio = len(parent.axisxx)/(len(parent.axisyy)*1.)
        l=0#only one file *extend to many files!!!*
        parent.Graphos = plt.figure(num=None, figsize=(10,8), dpi=120)
        parent.GraphosAx = parent.Graphos.add_subplot(111)
        mini = np.amin(parent.plotmif[1+l])
        mx_plot = np.log10(parent.plotmif[1+l]-mini+1)
        parent.origu = np.amax(parent.plotmif[l+1]-mini+1)
        parent.origl = np.amin(parent.plotmif[l+1]-mini+1)
        #mx_plot = parent.plotmif[1+l]-mini+1
        mx1 = (2**16-1)*(parent.plotmif[l+1] - np.min(np.min(parent.plotmif[l+1])))/np.max(np.max(parent.plotmif[l+1]))
        mx = np.flipud(mx1).astype('uint16')
        filename = parent.myxml[l]+"_aif.tif"
        tifff(mx,filename,info)                
        parent.cmlow = np.amin(mx_plot)
        parent.cmupp = np.amax(mx_plot)
        parent.cmmin = parent.cmlow
        parent.cmmax = parent.cmupp
        #tupi = parent.cm1._segmentdata
        cmap = mcol.LinearSegmentedColormap('name',parent.ctof,gamma=gam)
        parent.GraphoPP = plt.imshow(np.flipud(mx_plot),cmap=cmap,extent=[ax,bx,ay,by],aspect=rati)
        plt.xlabel(r'$\lambda$ [$\AA$]',fontsize=parent.fontly)
        plt.ylabel(r'$\alpha_{f} $ [deg]',fontsize=parent.fontly)
        parent.GraphoCBar = plt.colorbar(parent.GraphoPP,shrink=1,aspect=30)
        for axis in ['top','bottom','left','right']:
            parent.GraphosAx.spines[axis].set_linewidth(parent.bordy)
        parent.GraphoCBar.outline.set_linewidth(parent.bordy)
        parent.GraphoCBar.ax.tick_params(labelsize=parent.fonty,length=parent.tickl,width=parent.tickw)
        parent.GraphosAx.get_xaxis().set_tick_params(which=u'major',labelsize=parent.fonty,length=parent.tickl,width=parent.tickw)
        parent.GraphosAx.get_yaxis().set_tick_params(which=u'major',labelsize=parent.fonty,length=parent.tickl,width=parent.tickw)
        parent.GraphosAx.get_yaxis().set_tick_params(which=u'minor',labelsize=parent.fonty,length=0.8*parent.tickl,width=parent.tickw)
        parent.GraphosAx.get_xaxis().set_tick_params(which=u'minor',labelsize=parent.fonty,length=0.8*parent.tickl,width=parent.tickw)
        plt.tight_layout()
        parent.imgfileout = parent.myxml[l]+"_aif.png"
        plt.savefig(parent.imgfileout)
        plt.show()
                
    if parent.btnTransf3.GetValue() == True:
        parent.axisxx = qxzp[lx[0]:lx[7]]
        intvx = np.absolute(qxzp[1]-qxzp[0])
        intvy = np.absolute(qzp[1]-qzp[0])
        parent.xxmin = ax = min(qxzp)
        parent.yymin = ay = min(qzp)
        parent.xxmax = bx = max(qxzp)
        parent.yymax = by = max(qzp)
        info = dict(qx_min = min(qxzp), qx_max = max(qxzp), qz_min = min(qzp), qz_max = max(qzp))
        info = json.dumps(info)
        gam = parent.gami
        rati = parent.aratio = intvx/intvy
        l=0
        parent.Graphos = plt.figure(num=None, figsize=(10,8), dpi=120)
        parent.GraphosAx = parent.Graphos.add_subplot(111)
        mini = np.amin(parent.plotmxzz[l+1])
        mx_plot = np.log10(parent.plotmxzz[l+1]-mini+1)
        parent.origu = np.amax(parent.plotmxzz[l+1]-mini+1)
        parent.origl = np.amin(parent.plotmxzz[l+1]-mini+1)
        mx1 = (2**16-1)*(parent.plotmxzz[l+1] - np.min(np.min(parent.plotmxzz[l+1])))/np.max(np.max(parent.plotmxzz[l+1]))
        mx = np.flipud(mx1).astype('uint16')
        filename = parent.myxml[l]+"_qxzz.tif"
        tifff(mx,filename,info)  
        parent.cmlow = np.amin(mx_plot)
        parent.cmupp = np.amax(mx_plot)
        parent.cmmin = parent.cmlow
        parent.cmmax = parent.cmupp
        #tupi = cm.spectral._segmentdata
        cmap = mcol.LinearSegmentedColormap('name',parent.ctof,gamma=gam)
        parent.GraphoPP = plt.imshow(np.flipud(mx_plot),cmap=cmap,extent=[ax,bx,ay,by],aspect=rati)
        plt.xlabel('$q_{x}/q_{z}$',fontsize=parent.fontly)
        plt.ylabel('$q_{z}$ [$\AA^{-1}$]',fontsize=parent.fontly)
        parent.GraphoCBar = plt.colorbar(parent.GraphoPP, shrink=1,aspect=30)
        for axis in ['top','bottom','left','right']:
            parent.GraphosAx.spines[axis].set_linewidth(parent.bordy)
        parent.GraphoCBar.outline.set_linewidth(parent.bordy)
        parent.GraphoCBar.ax.tick_params(labelsize=parent.fonty,length=parent.tickl,width=parent.tickw)
        parent.GraphosAx.get_xaxis().set_tick_params(labelsize=parent.fonty,length=parent.tickl,width=parent.tickw)
        parent.GraphosAx.get_yaxis().set_tick_params(labelsize=parent.fonty,length=parent.tickl,width=parent.tickw)
        parent.GraphosAx.get_yaxis().set_tick_params(which=u'minor',labelsize=parent.fonty,length=0.8*parent.tickl,width=parent.tickw)
        parent.GraphosAx.get_xaxis().set_tick_params(which=u'minor',labelsize=parent.fonty,length=0.8*parent.tickl,width=parent.tickw)
        plt.tight_layout()
        parent.imgfileout = parent.myxml[l]+"_qxzz.png"
        plt.savefig(parent.imgfileout)
        plt.show()
                
def Integration(parent):
    plt.close()
    btnSX = parent.btnInt1.GetValue()
    btnSY = parent.btnInt2.GetValue()
    if parent.idTransf == 1:
        labelx = r'$\alpha_{f}' r'[rad]$'
        labely = r'$\lambda$ [$\AA$]'
    if parent.idTransf == 2:
        labelx = '$q_{z}$ [$\AA^{-1}$]'
        labely = '$q_{x}$ [$\AA^{-1}$]'
    if parent.idTransf == 3:
        labelx = '$q_{z}$ [$\AA^{-1}$]'
        labely = '$q_{x}/q_{z}$'
    parent.Graphos = plt.figure(num=None, figsize=(6,6), dpi=120)
    parent.GraphosAx = parent.Graphos.add_subplot(111)
    if btnSX == True:
        if parent.y1 != 0 or parent.y2 != 0: 
            i1,i2=0,0
            #print parent.axisyy
            while parent.y1 >= parent.axisyy[i1]:
                a,i1=i1,i1+1
            while parent.y2 >= parent.axisyy[i2]:
                b,i2=i2,i2+1
            if parent.x1 != 0 or parent.x2 != 0: 
                i1,i2=0,0
                while parent.x1 >= parent.axisxx[i1]:
                    c,i1=i1,i1+1
                while parent.x2 >= parent.axisxx[i2]:
                    d,i2=i2,i2+1
            else:
                c, d = 0, len(parent.axisxx)-1
        else:
            a, b = 0, len(parent.axisyy)-1
            if parent.x1 != 0 or parent.x2 != 0: 
                i1,i2=0,0
                while parent.x1 >= parent.axisxx[i1]:
                    c,i1=i1,i1+1
                while parent.x2 >= parent.axisxx[i2]:
                    d,i2=i2,i2+1    
            else:
                c, d = 0, len(parent.axisxx)-1
        intqxy = np.sum(parent.intdata[1][a:b,c:d],axis=1)
        #print intqxy.shape, parent.intdata[1].shape,parent.axisyy.shape
        parent.GraphoPP = plt.semilogy(parent.axisyy[a:b], intqxy, 'r.-')
        plt.xlabel(labelx,fontsize=22) 
    if btnSY == True:
        if parent.y1 != 0 or parent.y2 != 0: 
            i1,i2=0,0
            while parent.y1 >= parent.axisyy[i1]:
                a,i1=i1,i1+1
            while parent.y2 >= parent.axisyy[i2]:
                b,i2=i2,i2+1
            if parent.x1 != 0 or parent.x2 != 0: 
                i1,i2=0,0
                while parent.x1 >= parent.axisxx[i1]:
                    c,i1=i1,i1+1
                while parent.x2 >= parent.axisxx[i2]:
                    d,i2=i2,i2+1
            else:
                c, d = 0, len(parent.axisxx)-1
        else:
            a, b = 0, len(parent.axisyy)-1
            if parent.x1 != 0 or parent.x2 != 0: 
                i1,i2=0,0
                while parent.x1 >= parent.axisxx[i1]:
                    c,i1=i1,i1+1
                while parent.x2 >= parent.axisxx[i2]:
                    d,i2=i2,i2+1    
            else:
                c, d = 0, len(parent.axisxx)-1
        intqxy = np.sum(parent.intdata[1][a:b,c:d],axis=0)
        #print intqxy.shape, parent.intdata[1].shape,parent.axisxx.shape
        parent.GraphoPP = plt.semilogy(parent.axisxx[c:d], intqxy, 'r.-')
        plt.xlabel(labely,fontsize=22)
    parent.GraphosAx.get_xaxis().set_tick_params(labelsize=parent.fonty,length=parent.tickl,width=parent.tickw)
    parent.GraphosAx.get_yaxis().set_tick_params(which=u'major',labelsize=parent.fonty,length=parent.tickl,width=parent.tickw)
    parent.GraphosAx.get_yaxis().set_tick_params(which=u'minor',labelsize=parent.fonty,length=0.8*parent.tickl,width=parent.tickw)
    plt.tight_layout()
    plt.show()                
 
def tifff(mx,fname,description):
    filename = fname.encode('ascii')
    output = open(filename,'wb')
    # Write the header
    head = chr(0x49)+chr(0x49)+chr(0x2a)+chr(0x00)
    thefile=head # Big endian & TIFF identifier
    dim0 = mx.shape[0]
    dim1 = mx.shape[1]
    offset = dim0*dim1*2 + 8
    a1=(offset & 0xff000000)/2**32
    a2=(offset & 0x00ff0000)/2**16
    a3=(offset & 0x0000ff00)/2**8
    a4=(offset & 0x000000ff)
    aa=chr(a4)+chr(a3)+chr(a2)+chr(a1)
    thefile=thefile+aa

    # Write the binary data
    for row in range (0,dim0):
        for col in range (0,dim1):
            value = mx[row,col]
            a3=(value & 0x0000ff00)/256
            a4=(value & 0x000000ff)
            aa=chr(a4)+chr(a3)
            thefile=thefile+aa

    # Number of directory entries:16
    aa=chr(0x10)+chr(0x00)
    thefile=thefile+aa

    # Width tag
    tag=chr(0x00)+chr(0x01)
    typs=chr(0x03)+chr(0x00)
    count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
    a1 = (dim1 & 0xff00)/256
    a2 = (dim1 & 0x00ff)
    val = chr(a2)+chr(a1)+chr(0x00)+chr(0x00)
    aa = tag+typs+count+val
    thefile=thefile+aa

    # Length tag
    tag=chr(0x01)+chr(0x01)
    typs=chr(0x03)+chr(0x00)
    count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
    a1 = (dim0 & 0xff00)/256
    a2 = (dim0 & 0x00ff)
    vall = chr(a2)+chr(a1)+chr(0x00)+chr(0x00)
    aa=tag+typs+count+vall
    thefile=thefile+aa

    # Bits per sample: 16bits
    tag=chr(0x02)+chr(0x01)
    typs=chr(0x03)+chr(0x00)
    count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
    val=chr(0x10)+chr(0x00)+chr(0x00)+chr(0x00)
    aa=tag+typs+count+val
    thefile=thefile+aa

    # Compresion: 1
    tag=chr(0x03)+chr(0x01)
    typs=chr(0x03)+chr(0x00)
    count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
    val=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
    aa=tag+typs+count+val
    thefile=thefile+aa

    # Photometry: Grayscale
    tag=chr(0x06)+chr(0x01)
    typs=chr(0x03)+chr(0x00)
    count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
    val=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
    aa=tag+typs+count+val
    thefile=thefile+aa

    # Fill Order: 1
    tag=chr(0x01)+chr(0x0a)
    typs=chr(0x03)+chr(0x00)
    count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
    val=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
    aa=tag+typs+count+val
    thefile=thefile+aa

    # Document name: 1
    tag=chr(0x0d)+chr(0x01)
    typs=chr(0x02)+chr(0x00)
    count=chr((len(filename)))+chr(0x00)+chr(0x00)+chr(0x00)
    offset = dim0*dim1*2 + 8 + 2 +12*16
    a1=(offset & 0xff000000)/2**32
    a2=(offset & 0x00ff0000)/2**16
    a3=(offset & 0x0000ff00)/2**8
    a4=(offset & 0x000000ff)
    val=chr(a4)+chr(a3)+chr(a2)+chr(a1)
    aa=tag+typs+count+val
    thefile=thefile+aa

    # Description: 1
    tag=chr(0x0e)+chr(0x01)
    typs=chr(0x02)+chr(0x00)
    count=chr((len(description)))+chr(0x00)+chr(0x00)+chr(0x00)
    offset = dim0*dim1*2 + 8 + 2 +12*16 + len(filename)
    a1=(offset & 0xff000000)/2**32
    a2=(offset & 0x00ff0000)/2**16
    a3=(offset & 0x0000ff00)/2**8
    a4=(offset & 0x000000ff)
    val=chr(a4)+chr(a3)+chr(a2)+chr(a1)
    aa=tag+typs+count+val
    thefile=thefile+aa

    # Strip Offset: after header
    tag=chr(0x11)+chr(0x01)
    typs=chr(0x04)+chr(0x00)
    count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
    val=chr(0x08)+chr(0x00)+chr(0x00)+chr(0x00)
    aa=tag+typs+count+val
    thefile=thefile+aa

    # Orientation
    tag=chr(0x12)+chr(0x01)
    typs=chr(0x03)+chr(0x00)
    count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
    val=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
    aa=tag+typs+count+val
    thefile=thefile+aa

    # Sample per pixel
    tag=chr(0x15)+chr(0x01)
    typs=chr(0x03)+chr(0x00)
    count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
    val=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
    aa=tag+typs+count+val
    thefile=thefile+aa

    # Rows per strip
    tag=chr(0x16)+chr(0x01)
    typs=chr(0x03)+chr(0x00)
    count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
    aa=tag+typs+count+vall
    thefile=thefile+aa

    # Strip byte count: 16 bits (2 bytes)
    tag=chr(0x17)+chr(0x01)
    typs=chr(0x04)+chr(0x00)
    count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
    byts = dim0*dim1*2
    a1=(byts & 0xff000000)/2**32
    a2=(byts & 0x00ff0000)/2**16
    a3=(byts & 0x0000ff00)/2**8
    a4=(byts & 0x000000ff)
    val=chr(a4)+chr(a3)+chr(a2)+chr(a1)
    aa=tag+typs+count+val
    thefile=thefile+aa

    # X Resolution
    tag=chr(0x1a)+chr(0x01)
    typs=chr(0x05)+chr(0x00)
    count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
    offset = dim0*dim1*2 + 8 + 2 +12*16 + len(filename)+len(description)
    a1=(offset & 0xff000000)/2**32
    a2=(offset & 0x00ff0000)/2**16
    a3=(offset & 0x0000ff00)/2**8
    a4=(offset & 0x000000ff)
    val=chr(a4)+chr(a3)+chr(a2)+chr(a1)
    aa=tag+typs+count+val
    thefile=thefile+aa

    # Y Resolution
    tag=chr(0x1b)+chr(0x01)
    typs=chr(0x05)+chr(0x00)
    count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
    offset = dim0*dim1*2 + 8 + 2 +12*16 + len(filename)+len(description)+8
    a1=(offset & 0xff000000)/2**32
    a2=(offset & 0x00ff0000)/2**16
    a3=(offset & 0x0000ff00)/2**8
    a4=(offset & 0x000000ff)
    val=chr(a4)+chr(a3)+chr(a2)+chr(a1)
    aa=tag+typs+count+val
    thefile=thefile+aa

    # Planar Configuration
    tag=chr(0x1c)+chr(0x01)
    typs=chr(0x03)+chr(0x00)
    count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
    val=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
    aa=tag+typs+count+val
    thefile=thefile+aa

    # Name + Description
    thefile=thefile+filename+description

    #Xres and Yres
    a4=chr(0x00)+chr(0x00)+chr(0x00)+chr(0x64)
    a3=chr(0x00)+chr(0x00)+chr(0x00)+chr(0x01)
    a2=chr(0x00)+chr(0x00)+chr(0x00)+chr(0x64)
    a1=chr(0x00)+chr(0x00)+chr(0x00)+chr(0x01)
    aa=a4+a3+a2+a1
    thefile=thefile+aa

    output.write(bytes(thefile))
    output.close() 

def Main():
    vmp = mpl.__version__
    vnp = np.__version__
    vsc = sci.__version__
    if vmp=='1.4.2':
        logging.basicConfig(filename='myapp.log', level=logging.DEBUG)
        logging.info('Started')
        try:
            app = wx.App()
            frame = app_wx(None,-1,'D17_1.2')
            frame.Show()
            app.MainLoop()
        except:
            logging.exception("Some problems")
            logging.info()
            logging.warning()
            logging.error()
            logging.critical()
            raise
    else:
        mess = "Matplolib vers. < "+"1.4.2\nYour version is "+vmp+"\nNumpy v. "+vnp+"\nScipy v. "+vsc
        ctypes.windll.user32.MessageBoxA(0, mess, "Update python", 1)
    
if __name__ == "__main__":
    Main()
