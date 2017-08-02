#!/usr/bin/env python

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from mpl_toolkits.axes_grid1 import make_axes_locatable

def saveImageAndData(par, idx, singleImage, string):
    firstImageName = par.myFiles[idx] + string + ".png"
    plt.savefig(firstImageName)
    np.savetxt(par.myFiles[idx] + string + ".dat", singleImage.astype('float32'))    


def updateAxisValuesOnUI(window, p, singleImage, regularXAxis, regularYAxis, stopX, stopY, isQxz):
    p.axisQxy = regularXYAxis[stopX[0]:stopX[7]]
    if (isQxz):
        info = dict(
            qxy_min = min(regularXAxis), 
            qxy_max = max(regularXAxis), 
            qxz_min = min(regularYAxis), 
            qxz_max = max(regularYAxis)
        )
        p.axisQxz = regularYAxis[stopY[2]:stopY[1]]
    else:
        info = dict( 
                qxy_min = min(regularXAxis), 
                qxy_max = max(regularXAxis), 
                qz_min = min(regularYAxis), 
                qz_max = max(regularYAxis)
            )
        p.axisQz = regularYAxis[stopY[2]:stopY[1]]
        
    info = json.dumps(info)
    
    window.lowerLimitXAxisEdt.SetValue('{:4.4f}'.format(min(regularXAxis)))
    window.upperLimitXAxisEdt.SetValue('{:4.4f}'.format(max(regularXAxis)))
    window.lowerLimitYAxisEdt.SetValue('{:4.4f}'.format(min(regularYAxis)))
    window.upperLimitYAxisEdt.SetValue('{:4.4f}'.format(max(regularYAxis)))
    
    p.minXAxis = min(regularXAxis)
    p.minYAxis = min(regularYAxis)
    p.maxXAxis = max(regularXAxis)
    p.maxYAxis = max(regularYAxis)    
    
    p.lowerValueColorbar = np.amin(logSingleImage)
    p.upperValueColorbar = np.amax(logSingleImage)
    p.fixedLowerValueColorbar = p.lowerValueColorbar
    p.fixedUpperValueColorbar = p.upperValueColorbar
        
    
def preparePlot(window, p, regularXAxis, regularYAxis, stopX, stopY, singleImage, isQxz):

    p.areaGraph = plt.figure(num=None, figsize=(8,8), dpi=120)
    p.axisGraph = p.areaGraph.add_subplot(111)
    logSingleImage = np.log10(singleImage-np.amin(singleImage)+1)

    p.initGraph = plt.imshow(
                np.flipud(logSingleImage),
                extent = [min(regularXAxis), max(regularXAxis), min(regularYAxis), max(regularYAxis)]
            )
    plt.xlabel('$q_{xy}$ [nm$^{-1}$]',fontsize=22)
    if (isQxz):
        plt.ylabel('$q_{xz}$ [nm$^{-1}$]',fontsize=22)
    else:
        plt.ylabel('$q_{z}$ [nm$^{-1}$]',fontsize=22)
    divider = make_axes_locatable(plt.gca())
    cax = divider.append_axes("right", "5%", pad="3%")
    p.colorbarGraph = plt.colorbar(p.initGraph, cax=cax)
    for axis in ['top','bottom','left','right']:
        p.axisGraph.spines[axis].set_linewidth(p.borderThickness)
    p.colorbarGraph.outline.set_linewidth(p.borderThickness)
    p.colorbarGraph.ax.tick_params(
                labelsize = p.fontSizeLabel,
                length = p.tickLength,
                width = p.tickWidth
            )
    p.axisGraph.get_xaxis().set_tick_params(
                labelsize = p.fontSizeLabel,
                length = p.tickLength,
                width = p.tickWidth
            )
    p.axisGraph.get_yaxis().set_tick_params(
                labelsize = p.fontSizeLabel,
                length = p.tickLength,
                width = p.tickWidth
            )
    plt.tight_layout()    


def interpolationOnRegularGrid(gridPatch, imagePatch, regularXAxis, regularYAxis, stopX, stopY, imageNumber):
    segmentX = {}
    segmentY = {}
    block = {}
    newImage = {}
    gridA = {}
    gridB = {}
    for i in range (0, imageNumber):
        for j in range (0,4):
            key1, key2 = str(10000*(j+1)+i),str(10000*(j+5)+i)
            
            segmentX[key1] = regularXAxis[stopX[2*j]:stopX[2*j+1]]
            segmentX[key2] = regularXAxis[stopX[2*j]:stopX[2*j+1]]
            
            segmentY[key1] = regularYAxis[stopY[0]:stopY[1]]
            segmentY[key2] = regularYAxis[stopY[2]:stopY[3]]
            
            gridA[key1], gridB[key1] = np.meshgrid(segmentX[key1], segmentY[key1])
            gridA[key2], gridB[key2] = np.meshgrid(segmentX[key2], segmentY[key2])

            block[key1] = griddata( gridPatch[key1].T, imagePatch[key1], 
                            (gridA[key1], gridB[key1]), method='linear')
                            
            block[key2] = griddata( gridPatch[key2].T, imagePatch[key2], 
                            (gridA[key2], gridB[key2]), method='linear')
        #print mx['40000']
        blockDown = np.concatenate(( block[str(10000+i)], block[str(20000+i)],
                                block[str(30000+i)], block[str(40000+i)]), axis=1)
        
        blockUp = np.concatenate(( block[str(50000+i)], block[str(60000+i)], 
                                block[str(70000+i)], block[str(80000+i)]), axis=1)
                                
        fullBlock = np.concatenate((blockUp, blockDown), axis=0)
        newImage[i+1] = np.nan_to_num(fullBlock)
    return newImage
    
           
def createEigthPatches(imageBundle, initialXGrid, regularXAxis, initialYGrid, regularYAxis, stopX, stopY):
    imagePatch = {}
    gridPatch = {}
    dim1 = imageBundle[1].shape[0]
    dim2 = imageBundle[1].shape[1]
    dim3 = len(imageBundle)
    
        
    for l in range (0, dim3):
            values = np.ravel(imageBundle[l+1])
            # Tolerance for the points
            t=20
            # Create 8 Patches
            def evaluateLimitsOnY(i, case):
                if (case==1):
                    checkAy = initialYGrid[i] < regularYAxis[stopY[0]-t]
                    checkBy = initialYGrid[i] > regularYAxis[stopY[1]]                  
                    return checkAy or checkBy
                else:
                    checkCy = initialYGrid[i] < regularYAxis[stopY[2]]
                    checkDy = initialYGrid[i] > regularYAxis[stopY[3]+t]
                    return checkCy or checkDy
                        
            def evaluateLimitsOnX(i, case):
                if (case==1):
                    checkAx = initialXGrid[i] < regularXAxis[stopX[0]]
                    checkBx = initialXGrid[i] > regularXAxis[stopX[1]+t]
                    return checkAx or checkBx
                elif (case==2):
                    checkCx = initialXGrid[i] < regularXAxis[stopX[2]-t]
                    checkDx = initialXGrid[i] > regularXAxis[stopX[3]]
                    return checkCx or checkDx
                elif (case==3):
                    checkEx = initialXGrid[i] < regularXAxis[stopX[4]]
                    checkFx = initialXGrid[i] > regularXAxis[stopX[5]+t]
                    return checkEx or checkFx
                else:
                    checkGx = initialXGrid[i] < regularXAxis[stopX[6]-t]
                    checkHx = initialXGrid[i] > regularXAxis[stopX[7]]
                    return checkGx or checkHx
        
            
            index = []
            for i in range (0,dim1*dim2):
                if ( evaluateLimitsOnX(i,1) or evaluateLimitsOnY(i,1) ):
                    index.append(i)
            imagePatch[str(10000+l)] = np.delete(values, index)
            gridPatch[str(10000+l)] = np.array([np.delete(initialXGrid,index),np.delete(initialYGrid,index)])
            
            index = []
            for i in range (0,dim1*dim2):
                if ( evaluateLimitsOnX(i,2) or evaluateLimitsOnY(i,1) ):
                    index.append(i)
            imagePatch[str(20000+l)] = np.delete(values,index)
            gridPatch[str(20000+l)] = np.array([np.delete(initialXGrid,index),np.delete(initialYGrid,index)])
            
            index = []
            for i in range (0,dim1*dim2):
                if ( evaluateLimitsOnX(i,3) or evaluateLimitsOnY(i,1) ):
                    index.append(i)
            imagePatch[str(30000+l)] = np.delete(values,index)
            gridPatch[str(30000+l)] = np.array([np.delete(initialXGrid,index),np.delete(initialYGrid,index)])
            
            index = []
            for i in range (0,dim1*dim2):
                if ( evaluateLimitsOnX(i,4) or evaluateLimitsOnY(i,1) ):
                    index.append(i)
            imagePatch[str(40000+l)]=np.delete(values,index)
            gridPatch[str(40000+l)]=np.array([np.delete(initialXGrid,index),np.delete(initialYGrid,index)])
            
            # Data cloud for each region
            index = []
            for i in range (0,dim1*dim2):
                if ( evaluateLimitsOnX(i,1) or evaluateLimitsOnY(i,2) ):
                    index.append(i)
            imagePatch[str(50000+l)]=np.delete(values,index)
            gridPatch[str(50000+l)]=np.array([np.delete(initialXGrid,index),np.delete(initialYGrid,index)])
            
            index = []
            for i in range (0,dim1*dim2):
                if ( evaluateLimitsOnX(i,2) or evaluateLimitsOnY(i,2) ):
                    index.append(i)
            imagePatch[str(60000+l)]=np.delete(values,index)
            gridPatch[str(60000+l)]=np.array([np.delete(initialXGrid,index),np.delete(initialYGrid,index)])
            
            index = []
            for i in range (0,dim1*dim2):
                if ( evaluateLimitsOnX(i,3) or evaluateLimitsOnY(i,2) ):
                    index.append(i)
            imagePatch[str(70000+l)]=np.delete(values,index)
            gridPatch[str(70000+l)]=np.array([np.delete(initialXGrid,index),np.delete(initialYGrid,index)])
            
            index = []
            for i in range (0,dim1*dim2):
                if ( evaluateLimitsOnX(i,4) or evaluateLimitsOnY(i,2) ):
                    index.append(i)
            imagePatch[str(80000+l)]=np.delete(values,index)
            gridPatch[str(80000+l)]=np.array([np.delete(initialXGrid,index),np.delete(initialYGrid,index)])
    return imagePatch, gridPatch
    

def getRegularAndInitialAxis(wavelength, incidentAngleDegree, pixelDensity, sampleToDetectorDistanceMeter, xDirectBeam, yDirectBeam, dimensionXY):
    wavevector = 2 * np.pi / wavelength
    incidentAngle = incidentAngleDegree * np.pi/180
    sampleToDetectorDistance = sampleToDetectorDistanceMeter * 1e6 / pixelDensity
    pixelY, pixelX = np.mgrid[0:dimensionXY[0], 0:dimensionXY[1]]
    # polar angle in radians
    pixelX = pixelX.astype(float)
    pixelY = pixelY.astype(float)
    zAngle = np.arctan((pixelY-yDirectBeam)/np.sqrt(sampleToDetectorDistance**2+(pixelX-xDirectBeam)*(pixelX-xDirectBeam)))
    # azimuth angle in radians
    xyDoubleAngle = np.arctan((pixelX-xDirectBeam)/sampleToDetectorDistance)
    # exit angle
    sampleZAngle = zAngle - incidentAngle*np.cos(xyDoubleAngle)
    #af2=asin(cos(z2f).*sin(af-tlt));
    momentumX = wavevector*(np.cos(sampleZAngle)*np.cos(xyDoubleAngle) - np.cos(incidentAngle))
    momentumY = wavevector*(np.cos(sampleZAngle)*np.sin(xyDoubleAngle))
    momentumZ = wavevector*(np.sin(sampleZAngle) + np.sin(incidentAngle))
    momentumXY = np.zeros([dimensionXY[0],dimensionXY[1]])
    momentumXZ = np.zeros([dimensionXY[0],dimensionXY[1]])
    
    for i in range (0, dimensionXY[0]):
        for j in range (0, dimensionXY[1]):
            if momentumY[i,j] >= 0:
                momentumXY[i,j] = np.sqrt(momentumX[i,j]**2+momentumY[i,j]**2)
                if momentumZ[i,j] >= 0:
                    momentumXZ[i,j] = np.sqrt(momentumX[i,j]**2+momentumZ[i,j]**2)
                else:
                    momentumXZ[i,j] = -np.sqrt(momentumX[i,j]**2+momentumZ[i,j]**2)
            else:
                momentumXY[i,j] = -np.sqrt(momentumX[i,j]**2+momentumY[i,j]**2)
                if momentumZ[i,j] >= 0:
                    momentumXZ[i,j] = np.sqrt(momentumX[i,j]**2+momentumZ[i,j]**2)  
                else:
                    momentumXZ[i,j] = -np.sqrt(momentumX[i,j]**2+momentumZ[i,j]**2)          
    
    initialXYGrid = np.ravel(momentumXY)
    initialXZGrid = np.ravel(momentumXZ)
    initialZGrid = np.ravel(momentumZ)
    
    #New Coordinates
    regularXYAxis = np.linspace(min(initialXYGrid), max(initialXYGrid), dimensionXY[1])
    regularXZAxis = np.linspace(0, max(initialXZGrid),dimensionXY[0]-yDirectBeam)
    regularZAxis = np.linspace(0, max(initialZGrid),dimensionXY[0]-yDirectBeam)
    #New Center due to delocalization
    for i in range (0, dimensionXY[1]-1):
        if (regularXYAxis[i+1]>=0) and (regularXYAxis[i]<0):
            newXCenter=i+1
    leftX,rightX,lowerY,upperY = newXCenter/2,(dimensionXY[1]+newXCenter)/2,yDirectBeam/2,(dimensionXY[0]+yDirectBeam)/2
    #Divide the image in 16 regions
    stopY = np.array([upperY-yDirectBeam,dimensionXY[0]-yDirectBeam-1,0,upperY-yDirectBeam])
    stopX = np.array([0,leftX,leftX,newXCenter,newXCenter,rightX,rightX,dimensionXY[1]-1])
    return initialXYGrid, initialXZGrid, initialZGrid, regularXYAxis, regularXZAxis, regularZAxis, stopX, stopY


def imageCorrector(appMainWindow, par):
    wavelength = float(appMainWindow.wavelengthEdt.GetValue())
    incidentAngleDegree = float(appMainWindow.incidentAlphaEdt.GetValue())
    sampleToDetectorDistanceMeter = float(appMainWindow.sampleToDetectorDistanceEdt.GetValue())
    pixelDensity = float(appMainWindow.densityPixelEdt.GetValue())
    imageBundle = par.imageContainer
    imageNumber = len(imageBundle)
    dimensionXY = (imageBundle[1].shape[0], imageBundle[1].shape[1])
    appMainWindow.statusMessageTxt.SetLabel('Be patient\nLarge Images - Each one at least 3 min')
    yDirectBeam = dimensionXY[0] - appMainWindow.verticalPixelOnDetectorEdt
    xDirectBeam = appMainWindow.horizontalPixelOnDetectorEdt

    initialXYGrid, initialXZGrid, initialZGrid, regularXYAxis, regularXZAxis, regularZAxis, stopX, stopY = \
        getRegularAndInitialAxis(wavelength, incidentAngleDegree, pixelDensity, sampleToDetectorDistanceMeter, xDirectBeam, yDirectBeam, dimensionXY)
    
    imagePatch =  {}
    gridPatchXYZ = {}
    gridPatchXZZ = {}
    
    if appMainWindow.plotQzQxyBtn.GetValue() == True:
        imagePatch, gridPatchXYZ = createEigthPatches(imageBundle, initialXYGrid, regularXYAxis, initialZGrid, regularZAxis, stopX, stopY)
        
        
    if appMainWindow.plotQxzQxyBtn.GetValue() == True:
        imagePatch, gridPatchXZZ = createEigthPatches(imageBundle, initialXYGrid, regularXYAxis, initialXZGrid, regularXZAxis, stopX, stopY)
        
        
    # Mapping with the new coordinates
    if appMainWindow.plotQzQxyBtn.GetValue() == True:        
        par.imageQxyQz = interpolationOnRegularGrid(gridPatchXYZ, imagePatch, regularXYAxis, regularZAxis, stopX, stopY, imageNumber)
        
              
    if appMainWindow.plotQxzQxyBtn.GetValue() == True:        
        par.imageQxyQxz = interpolationOnRegularGrid(gridPatchXZZ, imagePatch, regularXYAxis, regularXZAxis, stopX, stopY, imageNumber)   
        
            
    #======================================================================================            
    # Make the plot
    
    if appMainWindow.plotQzQxyBtn.GetValue() == True:
        singleImage = par.imageQxyQz[1]
        updateAxisValuesOnUI(appMainWindow, par, singleImage, regularXYAxis, regularZAxis, stopX, stopY, False)
        for l in range (0, imageNumber):
            if l == 0:
                singleImage = par.imageQxyQz[l+1]
                preparePlot(appMainWindow, par, regularXYAxis, regularZAxis, stopX, stopY, singleImage, False)
                saveImageAndData(par, l, singleImage, "_qxy")                         
                plt.show()
            else:
                plt.close()
                singleImage = par.imageQxyQz[l+1]
                preparePlot(appMainWindow, par, regularXYAxis, regularZAxis, stopX, stopY, singleImage, False)
                par.colorbarGraph.draw_all()
                saveImageAndData(par, l, singleImage, "_qxy")             

                
    if appMainWindow.plotQxzQxyBtn.GetValue() == True:
        singleImage = par.imageQxyQxz[1]
        updateAxisValuesOnUI(appMainWindow, par, singleImage, regularXYAxis, regularXZAxis, stopX, stopY, True)
        for l in range (0, imageNumber):
            if l==0:
                plt.close()
                singleImage = par.imageQxyQxz[l+1]
                preparePlot(appMainWindow, par, regularXYAxis, regularXZAxis, stopX, stopY, singleImage, True)
                saveImageAndData(par, l, singleImage, "_qxz")             
                plt.show()              
            else:
                plt.close()
                singleImage = par.imageQxyQxz[l+1]
                preparePlot(appMainWindow, par, regularXYAxis, regularXZAxis, stopX, stopY, singleImage, True)
                par.colorbarGraph.draw_all()
                saveImageAndData(par, l, singleImage, "_qxz")     
               