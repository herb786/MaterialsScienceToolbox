#!/usr/bin/env python

import os
import numpy as np
import matplotlib.pyplot as plt

def integrateAxis(minValue, maxValue, axisX, singleImage):
    if minValue != 0 and maxValue != 0: 
        i1,i2=0,0
        while minValue >= axisX[i1]:
            a, i1 = i1, i1+1
        while maxValue >= axisX[i2]:
            b, i2 = i2, i2+1
        intensity = np.sum(singleImage[a:b,:], axis=0)
    else:
        intensity = np.sum(singleImage, axis=0)
    return intensity

 
def plotIntegration(par, integrationNumber):
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.ylabel(r'$Intensity[u.a.]$', fontsize=22)
    
    if integrationNumber == 1:
        intensity = integrateAxis(par.lowerBoundIntegration, par.upperBoundIntegration, par.axisQz, par.imageQxyQz[1])   
        plt.semilogy(par.axisQxy, intensity, 'r.-')
        plt.xlabel(r'$q_{xy}$', fontsize=22)
        
        
    if integrationNumber == 2:
        intensity = integrateAxis(par.lowerBoundIntegration, par.upperBoundIntegration, par.axisQxz, par.imageQxyQxz[1])   
        plt.semilogy(par.axisQxy, intensity, 'b.-')
        plt.xlabel(r'$q_{xy}$', fontsize=22)

        
    if integrationNumber == 3:
        intensity = integrateAxis(par.lowerBoundIntegration, par.upperBoundIntegration, par.axisQxy, par.imageQxyQz[1])   
        plt.semilogy(par.axisQz, intensity, 'r.-')
        plt.xlabel(r'$q_z$', fontsize=22)

        
    if integrationNumber == 4:
        intensity = integrateAxis(par.lowerBoundIntegration, par.upperBoundIntegration, par.axisQxy, par.imageQxyQxz[1])   
        plt.semilogy(par.axisQxz, intensity, 'b.-')
        plt.xlabel(r'$q_{xz}$', fontsize=22)
        
    plt.show()
    
    
def integrationRoutine(appMainWindow, par):

    imageBundle = par.imageContainer
    imageNumber = len(imageBundle)
    
    integrateOverQxzKeepQxy = appMainWindow.integrateOverQxzKeepQxyBtn.GetValue()
    integrateOverQzKeepQxy = appMainWindow.integrateOverQzKeepQxyBtn.GetValue()
    integrateOverQxyKeepQz = appMainWindow.integrateOverQxyKeepQzBtn.GetValue()
    integrateOverQxyKeepQxz = appMainWindow.integrateOverQxyKeepQxzBtn.GetValue()
    
    par.lowerBoundIntegration = float(appMainWindow.lowerLimitQAxisEdt.GetValue())
    par.upperBoundIntegration = float(appMainWindow.upperLimitQAxisEdt.GetValue())
    
    if integrateOverQzKeepQxy == True:
        plotIntegration(par, 1)
      
    if integrateOverQxzKeepQxy == True:
        plotIntegration(par, 2)

    if integrateOverQxyKeepQz == True:
        plotIntegration(par, 3)
        
    if integrateOverQxyKeepQxz == True:
        plotIntegration(par, 4)
    
    
