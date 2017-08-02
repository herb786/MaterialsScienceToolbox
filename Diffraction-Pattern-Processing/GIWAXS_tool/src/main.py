#!/usr/bin/env python

import wx
import os, sys
import numpy as np
import scipy as sci
import matplotlib as mpl
from AppMainWindow import AppMainWindow
from AppParameters import AppParameters as par
from distutils.version import StrictVersion

def main():
    vmp = mpl.__version__
    vnp = np.__version__
    vsc = sci.__version__ 
    if StrictVersion(vmp) > StrictVersion("1.4.1"):
        app = wx.App()
        frame = AppMainWindow(None,-1,'GIWAXS Tool',par)
        frame.bindEvents()
        frame.Show()
        app.MainLoop()
    else:
        mess = "Matplolib vers. < "+"1.4.2\nYour version is "+vmp+"\nNumpy v. "+vnp+"\nScipy v. "+vsc
        # ctypes.windll.user32.MessageBoxA(0, mess, "Update python", 1)
    
if __name__ == "__main__":
    main()