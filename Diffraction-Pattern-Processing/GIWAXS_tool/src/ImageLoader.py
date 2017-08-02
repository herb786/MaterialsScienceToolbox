#!/usr/bin/env python

import sys, os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcol
import matplotlib.widgets as widgets


def logFile(string):
    file = open("log.txt", "w")
    file.write(string)
    file.close()

    
def flattenImage(imagefile, vertices, flag):
    imagen = plt.imread(imagefile)
    imagenArray = imagen.astype(float)
            
    if np.ndim(imagenArray) > 2:
        imagenArray =  np.sum(imagenArray, axis=2)
        
    if (flag):
        newImage = np.zeros((vertices[3],vertices[2]))
        for i in range (0, vertices[3]):
                for j in range (0, vertices[2]):
                    newImage[i,j] = imagenArray[vertices[1]+i, vertices[0]+j]
        return newImage[ ::-1, :]
    else:
        return imagenArray
    

def putPixelCoordinatesOnUI(appMainWindow, par, event):
    par.yBeamCoordinate = event.ydata.astype(int)
    par.xBeamCoordinate = event.xdata.astype(int)
    appMainWindow.horizontalPixelOnDetectorEdt.SetValue(str(par.xBeamCoordinate))
    appMainWindow.verticalPixelOnDetectorEdt.SetValue(str(par.yBeamCoordinate))
    appMainWindow.statusMessageTxt.SetLabel('Select an Area')
    
    
def changeFocusToWavelength(appMainWindow):
    appMainWindow.statusMessageTxt.SetLabel('Close the figure\nbefore run the correction')
    appMainWindow.wavelengthEdt.SetFocus()
    appMainWindow.wavelengthEdt.SetSelection(-1,-1)
    
    
def updateWorkAreaParametersOnUI(appMainWindow, par, dimension, extremes):
    #Write out the new direct beam coordinates on screen
    appMainWindow.verticalPixelOnDetectorEdt.SetValue(str(par.yBeamCoordinate))
    appMainWindow.horizontalPixelOnDetectorEdt.SetValue(str(par.xBeamCoordinate))
    #Write out the dimension of the crop rectangle
    appMainWindow.cropSizeEdt.SetLabel(str(dimension[0]) + 'x' + str(dimension[1]))
    #Write out the limits of the current colormap
    appMainWindow.lowerLimitColorMapSliderTxt.SetLabel('{:4.0f}'.format(extremes[0]))
    appMainWindow.upperLimitColorMapSliderTxt.SetLabel('{:4.0f}'.format(extremes[1]))
    
    
def lockDirectBeamCoordinates(appMainWindow, par):
    par.yBeamCoordinate = np.int32(float(appMainWindow.verticalPixelOnDetectorEdt.GetValue()))
    par.xBeamCoordinate = np.int32(float(appMainWindow.horizontalPixelOnDetectorEdt.GetValue()))
    appMainWindow.verticalPixelOnDetectorEdt.Disable()
    appMainWindow.horizontalPixelOnDetectorEdt.Disable()

    
def imageLoader(appMainWindow, par, imageFile):
    nfile = len(imageFile)
    #new = []
    graphContainer = {}
    vertices = ()
    
    for file in range (0, nfile):
        filekey = 1 + file
        
        if file == 0:
            plt.close()
            imagen = flattenImage(imageFile[file], vertices, False)
            
            fig = plt.figure()
            ax = fig.add_subplot(111)
                
            def doubleClick(event):
                if event.dblclick:
                    putPixelCoordinatesOnUI(appMainWindow, par, event)
                    
            def onSelect(eclick, erelease):
                par.xLeftLowerCornerArea = np.minimum(erelease.xdata, eclick.xdata)
                par.yLeftLowerCornerArea = np.minimum(erelease.ydata, eclick.ydata)
                par.workAreaHeight = np.absolute(erelease.ydata - eclick.ydata)
                par.workAreaWidth = np.absolute(erelease.xdata - eclick.xdata)
                
                if par.workAreaHeight > 10:
                    changeFocusToWavelength(appMainWindow)
                    
                fig.canvas.draw()
           
            
            # Select pixel for the direct beam
            plt.imshow(imagen, interpolation='none', cmap = cm.jet, norm=mcol.LogNorm())
            appMainWindow.statusMessageTxt.SetLabel('Double Click for\nDirect Beam Coordinates')
            fig.canvas.mpl_connect('button_press_event', doubleClick)
            
            # Select region to work
            selector = widgets.RectangleSelector(ax, onSelect, drawtype='box', rectprops = dict(facecolor='yellow', edgecolor = 'black', alpha=0.5, fill=True))
            plt.show()
            a = np.int32(par.xLeftLowerCornerArea)
            b = np.int32(par.yLeftLowerCornerArea)
            c = np.int32(par.workAreaWidth)
            d = np.int32(par.workAreaHeight)
            vertices = (a,b,c,d)
            lockDirectBeamCoordinates(appMainWindow, par)
            imagen = flattenImage(imageFile[file], vertices, False)            
                 
            # Assign new direct beam coordinates respect to the crop rectangle
            par.yBeamCoordinate = par.yBeamCoordinate - b
            par.xBeamCoordinate = par.xBeamCoordinate - a
            
            # Update UI
            graphContainer[filekey] = flattenImage(imageFile[file], vertices, True)
            logFile(graphContainer[1].flatten().tostring())
            extremes = (np.amin(graphContainer[1]), np.amax(graphContainer[1]))
            updateWorkAreaParametersOnUI(appMainWindow, par, graphContainer[1].shape, extremes)
            
        else:      
            plt.close()
            appMainWindow.statusMessageTxt.SetLabel('Reading file ' + str(file+1))                  
            graphContainer[filekey] = flattenImage(imageFile[file], vertices, True)
            
    #Allocate data in array
    par.imageContainer = graphContainer
    appMainWindow.statusMessageTxt.SetLabel('Enter parameters\nClick on RUN')
    #Flush memory
    del graphContainer