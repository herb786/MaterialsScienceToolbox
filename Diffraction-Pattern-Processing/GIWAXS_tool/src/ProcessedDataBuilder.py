#!/usr/bin/env python

import os
import numpy as np
import matplotlib.pyplot as plt

def saveIntegrationData(par, case, folderpath):

    imageBundle = par.imageContainer
    imageNumber = len(imageBundle)
    
    for i in range (0, imageNumber):
    
        if case == 1:
            filename = os.path.join(folderpath, par.myFiles[i]+'_QxyOverQxz.dat')
            xAxis = par.axisQxy
            yAxis = np.sum(par.imageQxyQxz[i+1], axis=0)
            
        if case == 2:
            filename = os.path.join(folderpath, par.myFiles[i]+'_QxyOverQz.dat')
            xAxis = par.axisQxy
            yAxis = np.sum(par.imageQxyQz[i+1], axis=0)
            
        if case == 3:
            filename = os.path.join(folderpath, par.myFiles[i]+'_QzOverQxy.dat')
            xAxis = par.axisQz
            yAxis = np.sum(par.imageQxyQz[i+1], axis=1)   
            
        if case == 4:
            filename = os.path.join(folderpath, par.myFiles[i]+'_QxzOverQxy.dat')
            xAxis = par.axisQxz
            yAxis = np.sum(par.imageQxyQxz[i+1], axis=1)
            
        xAxis = xAxis.reshape((len(xAxis), 1))
        yAxis = yAxis.reshape((len(xAxis), 1))
        axisArray = np.hstack([xAxis, yAxis])
        #print xout, theaxisx.shape
        np.savetxt(filename, axisArray, fmt=['%4.5f', '%4.5f'])    