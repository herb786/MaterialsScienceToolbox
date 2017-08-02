#!/usr/bin/env python

import os
import numpy as np
import matplotlib.pyplot as plt

def prepareGraphPair(singleImage1, singleImage2, axis1, axis2, labelXAxis):
    y1 = np.sum(singleImage1, axis=0)
    y2 = np.sum(singleImage2, axis=0)
    
    p1, = plt.semilogy(axis1, y1, 'r.-')
    p2, = plt.semilogy(axis2, y2, 'b.-')
    
    plt.xlabel(labelXAxis, fontsize=22)
    plt.ylabel(r'$Intensity\ [a.u.]$', fontsize=22)
    plt.legend([p1, p2], ["$q_{z}$", "$q_{xz}$"])
    plt.setp(plt.gca().get_legend().get_texts(), fontsize='18') 
    
    
def comparatorRoutine(appMainWindow, par):

    imageBundle = par.imageContainer
    imageNumber = len(imageBundle)
    
    integrateOverQxzKeepQxy = appMainWindow.integrateOverQxzKeepQxyBtn.GetValue()
    integrateOverQzKeepQxy = appMainWindow.integrateOverQzKeepQxyBtn.GetValue()
    integrateOverQxyKeepQz = appMainWindow.integrateOverQxyKeepQzBtn.GetValue()
    integrateOverQxyKeepQxz = appMainWindow.integrateOverQxyKeepQxzBtn.GetValue()
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    if (integrateOverQzKeepQxy and integrateOverQxzKeepQxy):
        labelXAxis = r'$q_{xy}$'
        prepareGraphPair(par.imageQxyQz[1], par.imageQxyQxz[1], par.axisQxy, par.axisQxy, labelXAxis)    

            
    if (integrateOverQxyKeepQz and integrateOverQxyKeepQxz):
        labelXAxis = r'$q_{z}, q_{xz}$'
        prepareGraphPair(par.imageQxyQz[1], par.imageQxyQxz[1], par.axisQxy, par.axisQxz, labelXAxis) 
        
    plt.show()