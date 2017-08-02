import wx
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcol
import matplotlib.image as mpimg
import matplotlib.widgets as widgets
import logging
import scipy.constants as npc
import json

#%%
class app_wx(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent,id,title,size = wx.Size(400,520),style = wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER)
        # useful data [Coh Scat Length:fm, Abs X Section:barn]
        hb,ha=[-3.741, 0.3326]
        db,da=[6.671,0.3326]
        cb,ca=[6.646,0.00350]
        nb,na=[9.36, 1.9]
        ob,oa=[5.803, 0.00019]
        sb,sa=[2.847, 0.53]
        sib,sia=[4.149, 0.171]
        feb,fea=[9.450,2.56]
        clb,cla=[9.577, 33.5]
        pb,pa=[5.13, 0.172]
        tib,tia=[-3.438, 6.09]
        cab,caa=[4.70, 0.43]
        def getSLD1(inp,stech,mol,rho):
            inp = np.array(inp)
            stech = np.array(stech)
            #sld = sum(inp[:]*stech[:])*npc.N_A*rho*1e-42/mol
            sld = np.inner(inp,stech)*npc.N_A*rho*1e-42/mol
            return sld
        def getSLD2(inp,stech,mol,rho):
            inp = np.array(inp)
            stech = np.array(stech)
            absp = np.einsum('i,i',inp,stech)*npc.N_A*rho*1e-40/mol
            return absp
        #My Materials [Id, Name, g/mol, kg/m3, Coh Scat Length:fm/density:fm-2, Abs X Section:barn,density:fm-1,SLD]
        self.MatData = [
                        [0, 'Nickel', 58.69, 8907, 1.44,0.231,0],
                        [1, 'Berylium', 9.01, 1850, 7.79,0.0076,0],
                        [2, 'Iron', 55.84, 7800, 9.450,2.56,0],
                        [3, 'Aluminium', 26.98, 2700, 3.449,0.231,0],
                        [4, 'Silver', 107.87, 10500, 5.922, 63.3,0],
                        [5, 'Cadmium', 112.41, 8650, 4.87, 2520.0,0],
                        [6, 'Fluorine', 19.00, 1700, 5.654, 0.0096,0],
                        [7, 'Hydrogen', 1.008, 0.08988, -3.741, 0.3326,0],
                        [8, 'Deuterium', 2.016, 0.180, 6.671, 0.3326,0],
                        [9, 'Carbon', 12.01, 2267, 6.646, 0.00350,0],
                        [10, 'Nytrogen', 14.01, 1.251, 9.36, 1.9,0],
                        [11, 'Oxygen', 16.00, 1.429, 5.803, 0.00019,0],
                        [12, 'Sulfur', 32.06, 1960, 2.847, 0.53,0],
                        [13, 'Chlorine', 35.45, 3.214, 9.577, 33.5,0],
                        [14, 'Silicon', 28.09, 2330, 4.149, 0.171,0],
                        [15, 'SiO2', 60.0843, 2200, getSLD1([sib,ob],[1,2],60.0843, 2200), getSLD2([sia,oa],[1,2],60.0843, 2200),1],
                        [16, 'Calcium Phosphate', 132.06, 2310, getSLD1([cab,hb,pb,ob],[1,1,1,4],132.06, 2310), getSLD2([caa,ha,pa,oa],[1,1,1,4],132.06, 2310),1],#cahpo4
                        [17, 'Maghemite', 159.69, 5000, getSLD1([feb,ob],[2,3],159.69, 5000), getSLD2([fea,oa],[2,3],159.69, 5000),1],#fe2o3
                        [18, 'Gold', 196.96655, 19320, 7.63, 98.65,0]]
        self.MatName = [name[1] for name in self.MatData ]
        self.MatWork = []


        #My Toolbar
        self.toolbar = self.CreateToolBar()
        quitico = wx.ArtProvider.GetBitmap(wx.ART_DELETE,wx.ART_TOOLBAR,(32,32))
        self.quittool = self.toolbar.AddSimpleTool(-1,quitico,'Quit')

        #My Labels
        self.lempty = wx.StaticText(self,-1,label=u'')
        self.lwlength = wx.StaticText(self,-1,label=u'Wavelength')
        self.lwlength.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lalfai = wx.StaticText(self,-1,label=u'Incidence Angle')
        self.lalfai.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))


        #My buttons
        self.btnPlot = wx.Button(self,-1,label='Plot')
        self.btnAdd = wx.Button(self,-1,label='Add')
        self.btnRemove = wx.Button(self,-1,label='Remove')
        self.btnOk = wx.Button(self,-1,label='OK')
        self.btnChoice = wx.ToggleButton(self,-1,label='Constant Wavelength')
        self.btnChoice.SetValue(False)

        #Mylist
        self.MatSel = wx.ComboBox(self,-1, choices=self.MatName, style=wx.CB_READONLY)
        self.MatList =  wx.ListCtrl(self,-1,style=wx.LC_REPORT,size=(200,150))
        self.MatList.InsertColumn(1, 'Material')

        #My Inputs
        self.wlength = wx.TextCtrl(self,-1,value=u'in Amstrongs')
        self.wlength.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.wlength.Disable()
        self.alfai = wx.TextCtrl(self,-1,value=u'in degrees')
        self.alfai.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))


        #My Design
        self.toolbar.Realize()

        self.parameters = wx.StaticBox(self,-1,'Parameters')
        self.parameters.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        parboxsizer =  wx.StaticBoxSizer(self.parameters, wx.VERTICAL)
        sizer = wx.GridBagSizer(hgap=10,vgap=10)
        sizer.Add(self.lempty,(0,8),(1,2),wx.EXPAND)
        sizer.Add(self.lwlength,(0,1),(1,2),wx.EXPAND)
        sizer.Add(self.wlength,(0,3),(1,4),wx.EXPAND)
        sizer.Add(self.lalfai,(1,1),(1,2),wx.EXPAND)
        sizer.Add(self.alfai,(1,3),(1,4),wx.EXPAND)
        parboxsizer.Add(sizer,-1, flag=wx.EXPAND|wx.ALL, border=10)

        self.mater = wx.StaticBox(self,-1,'Materials')
        self.mater.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        matersizer =  wx.StaticBoxSizer(self.mater, wx.VERTICAL)
        sizermater = wx.GridBagSizer(hgap=10,vgap=10)
        sizermater.Add(self.MatSel,(0,0),(1,2),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=5)
        sizermater.Add(self.btnAdd,(0,2),(1,1),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=5)
        sizermater.Add(self.MatList,(1,0),(4,2),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=5)
        sizermater.Add(self.btnRemove,(1,2),(1,1),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=5)
        sizermater.Add(self.btnOk,(2,2),(1,1),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=5)
        matersizer.Add(sizermater,-1, flag=wx.EXPAND|wx.ALL, border=10)

        root = wx.GridBagSizer(2,2)
        root.Add(matersizer,(0,0),(12,6),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=20)
        root.Add(parboxsizer,(12,0),(8,6),flag=wx.RIGHT|wx.LEFT|wx.EXPAND, border=20)
        root.Add(self.btnPlot,(20,4),(1,2))
        root.Add(self.btnChoice,(20,1),(1,2))
        self.SetSizer(root)

        #My Events
        self.events = EventH(self)
        self.Bind(wx.EVT_TOOL,self.events.OnQuit,self.quittool)
        self.btnAdd.Bind(wx.EVT_BUTTON,self.events.OnAdd)
        self.btnPlot.Bind(wx.EVT_BUTTON,self.events.PlotButtonClick)
        self.btnRemove.Bind(wx.EVT_BUTTON,self.events.OnRemove)
        self.btnOk.Bind(wx.EVT_BUTTON,self.events.NextA)
        self.btnChoice.Bind(wx.EVT_TOGGLEBUTTON,self.events.ToggleSwitch)
        self.Bind(wx.EVT_TEXT_ENTER,self.events.NextC,self.wlength)
        self.Bind(wx.EVT_TEXT_ENTER,self.events.NextC,self.alfai)


class EventH():
    def __init__(self,parent):
        self.parent = parent

    def OnQuit(self,event):
        self.parent.Close()

    def NextA(self,event):
        if self.parent.btnChoice.GetValue() == True:
            self.parent.wlength.SetFocus()
            self.parent.wlength.SetSelection(-1,-1)
        self.parent.alfai.SetFocus()
        self.parent.alfai.SetSelection(-1,-1)

    def NextC(self,event):
        self.parent.btnPlot.SetFocus()

    def PlotButtonClick(self,event):
        #print self.parent.MatList.GetItemCount()
        Plotting(self.parent)

    def ToggleSwitch(self,event):
        if self.parent.btnChoice.GetValue() == False:
            self.parent.wlength.Disable()
            self.parent.alfai.Enable()
            self.parent.btnChoice.SetLabel('Constant Wavelength')
        if self.parent.btnChoice.GetValue() == True:
            self.parent.wlength.Enable()
            self.parent.alfai.Disable()
            self.parent.btnChoice.SetLabel('Constant Angle')

    def OnAdd(self,event):
        id_mat = self.parent.MatSel.GetSelection()
        self.parent.MatList.InsertStringItem(id_mat,self.parent.MatName[id_mat])
        objeto = self.parent.MatData[id_mat]
        self.parent.MatWork.append(objeto)
        #print self.parent.MatWork


    def OnRemove(self,event):
        id_obj = self.parent.MatList.GetFocusedItem()
        self.parent.MatList.DeleteItem(id_obj)
        objeto = self.parent.MatWork[id_obj]
        #print id_obj, objeto
        self.parent.MatWork.remove(objeto)
        #print self.parent.MatWork


#===============================================================================================
def Plotting(parent):
    #print parent.MatWork
    material = [x[1] for x in parent.MatWork]
    molg = [x[2] for x in parent.MatWork]
    molg = np.array(molg)
    rhod = [x[3] for x in parent.MatWork]
    rhod = np.array(rhod)
    dens = npc.N_A*rhod*1e3/molg
    bcoh = [x[4] for x in parent.MatWork]
    bcoh = np.array(bcoh)
    xabs = [x[5] for x in parent.MatWork]
    xabs = np.array(xabs)
    sld = [x[6] for x in parent.MatWork]
    sld = np.array(sld)
    def func1(x,i):
        wave = float(parent.wlength.GetValue())
        wave = wave*1e-10
        if sld[i]==0: 
            cang = wave*np.sqrt(dens[i]*1e-15*bcoh[i]/np.pi)
            iang = x*cang
            beta = wave*dens[i]*100e-30*xabs[i]/(4*np.pi)
        if sld[i]==1:
            cang = wave*np.sqrt(bcoh[i]*1e30/np.pi)
            iang = x*cang
            beta = wave*xabs[i]*1e15/(4*np.pi)
        den1 = np.sqrt((iang**2-cang**2)**2 + 4*beta**2) - (iang**2-cang**2)
        depth = 1e10*wave/(np.pi*np.sqrt(2*den1))
        #print dens
        return depth
    def func2(x,i):
        iang = float(parent.alfai.GetValue())
        iang = np.pi*iang/180
        wave = x
        wave = wave*1e-10
        if sld[i]==0:
            cang = wave*np.sqrt(dens[i]*1e-15*bcoh[i]/np.pi)
            beta = wave*dens[i]*100e-30*xabs[i]/(4*np.pi)
        if sld[i]==1:
            cang = wave*np.sqrt(1e30*bcoh[i]/np.pi)
            beta = wave*1e15*xabs[i]/(4*np.pi)        
        den1 = np.sqrt((iang**2-cang**2)**2 + 4*beta**2) - (iang**2-cang**2)
        #print den1, cang, beta,dens,bcoh,xabs
        depth = 1e10*wave/(np.pi*np.sqrt(2*den1))
        return depth
    fig = plt.figure()
    fig.add_subplot(111)
    if parent.btnChoice.GetValue() == False:
        material.insert(0,'wavelength')
        output = open('myfile_lambda.dat', 'w')
        x = np.linspace(1e-1, 20, 200)
        y = [[func2(a,i) for a in x] for i in range(len(dens))]
        for i in range(len(dens)):
            plt.semilogy(x, y[i],label=material[i+1])
        plt.xlabel('$\lambda$ [$\AA$]',fontsize=22)
        plt.ylabel('Penetration depth [$\AA$]',fontsize=22)
    if parent.btnChoice.GetValue() == True:
        material.insert(0,'angle')
        output = open('myfile_angle.dat', 'w')
        x = np.linspace(0,4, 200)
        y = [[func1(a,i) for a in x] for i in range(len(dens))]
        for i in range(len(dens)):
            plt.semilogy(x, y[i],label=material[i+1])
        plt.xlabel(r'$\alpha_i/\alpha_c}$',fontsize=22)
        plt.ylabel('Penetration depth [$\AA$]',fontsize=22)
    plt.legend()
    plt.setp(plt.gca().get_legend().get_texts(), fontsize='18')
    plt.show()
    axisx = x.reshape((len(x),1))
    y = np.array(y)
    axisy = y.T
    xout = np.hstack([axisx,axisy])
    np.savetxt(output,xout, fmt='%4.5f',header=json.dumps(material))

#%%

def Main():
    app = wx.App()
    frame = app_wx(None,-1,'Penetration depth')
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    Main()
