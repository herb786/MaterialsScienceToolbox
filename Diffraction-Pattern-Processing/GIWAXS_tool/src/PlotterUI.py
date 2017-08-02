#!/usr/bin/env python

import os
import numpy as np
import matplotlib.pyplot as plt

def changeLimitColorMapSlider(window, par, isUpper):

    if (isUpper):
        uiValue = window.upperLimitColorMapSlider.GetValue()
    else:
        uiValue = window.lowerLimitColorMapSlider.GetValue()
        
    limit1 = par.lowerValueColorbar
    limit2 = par.upperValueColorbar
    
    if window.logScaleBtn.GetValue() == True:
        actualValue = limit1 + val*(limit2-limit1)/100
        if (isUpper):
            par.fixedUpperValueColorbar = actualValue
            window.upperLimitColorMapTxt.SetLabel('{:4.0f}'.format(np.power(10,actualValue)))
            par.initGraph.set_clim(vmax = actualValue)
        else:
            par.fixedLoweValueColorbar = actualValue
            window.lowerLimitColorMapTxt.SetLabel('{:4.0f}'.format(np.power(10,actualValue)))
            par.initGraph.set_clim(vmin = actualValue)
    else:
        actualValue = np.power(10,limit1) + val*(np.power(10,limit2) - np.power(10,limit1))/100
        if (isUpper):
            window.upperLimitColorMapTxt.SetLabel('{:4.0f}'.format(actualValue))
            par.fixedUpperValueColorbar = np.log10(actualValue)
            par.initGraph.set_clim(vmax = np.log10(actualValue))
        else:
            window.lowerLimitColorMapTxt.SetLabel('{:4.0f}'.format(actualValue))
            par.fixedLowerValueColorbar = np.log10(actualValue)
            par.initGraph.set_clim(vmin = np.log10(actualValue))
        
    par.colorbarGraph.draw_all()
    plt.savefig(par.firstImageName)
    plt.draw()

    
def plotAgainRoutine(window, par):
    par.fontSizeLabel = float(window.tickFontSizeEdt.GetValue())
    par.borderThickness = float(window.borderThicknessEdt.GetValue())
    par.tickWidth = float(window.tickWidthEdt.GetValue())
    par.tickLength = float(window.tickLengthEdt.GetValue())
    
    par.minXAxis = float(window.lowerLimitXAxisEdt.GetValue())
    par.minYAxis = float(window.upperLimitXAxisEdt.GetValue())
    par.maxXAxis = float(window.lowerLimitYAxisEdt.GetValue())
    par.maxYAxis = float(window.upperLimitYAxisEdt.GetValue())
    
    par.axisGraph.set_ylim([par.minYAxis, par.maxYAxis])
    par.axisGraph.set_xlim([par.minXAxis, par.maxYAxis])
    
    par.axisGraph.xaxis.set_major_locator(MaxNLocator(nbins=6))#tick numbers at the x-axis
    par.axisGraph.yaxis.set_major_locator(MaxNLocator(nbins=4))#tick numbers at the y-axis
    
    for axis in ['top','bottom','left','right']:
        par.axisGraph.spines[axis].set_linewidth(par.borderThickness)
    mpl.rcParams['axes.linewidth'] = par.borderThickness
    
    par.colorbarGraph.ax.tick_params(
        labelsize=par.fontSizeLabel, 
        length=par.tickLength, 
        width=par.tickWidth )
        
    par.axisGraph.get_xaxis().set_tick_params(
        labelsize=par.fonty,
        length=par.tickLength,
        width=par.tickWidth )
        
    par.axisGraph.get_yaxis().set_tick_params(
        labelsize=par.fontSizeLabel,
        length=par.tickLength,
        width=par.tickWidth )
        
    plt.tight_layout()
    par.colorbarGraph.draw_all()
    plt.savefig(par.firstImageName)
    plt.draw()