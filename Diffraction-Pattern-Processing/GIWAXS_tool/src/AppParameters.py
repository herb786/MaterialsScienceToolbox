#!/usr/bin/env python

import os
import numpy as np
import matplotlib.pyplot as plt


class AppParameters():       
 
        myFiles = []#container for the filenames
        folderName = os.getcwd()#directory path of the output
        imageContainer = {}#container with data image as 3D arrays
        yBeamCoordinate = []#direct beam y-coordinate
        xBeamCoordinate = []#direct beam x-coordinate
        xLeftLowerCornerArea = []#x-coordinate of the origin for the crop rectangle
        yLeftLowerCornerArea = []#y-coordinate of the origin for the crop rectangle
        workAreaWidth = []#width of the crop rectangle
        workAreaHeight = []#height of the crop rectangle
        
        imageQxyQz = {}#new 3D array of data image
        imageQxyQxz = {}#new 3D array of data image
        
        axisQxy = []#values of the new axis
        axisQz = []#values of the new axis
        axisQxz = []#values of the new axis
        minXAxis = []#minimum value for the qxy coordinate
        minYAxis = []#minimum value for the qz(qxz) coordinate
        maxXAxis = []#maximum value for the qxy coordinate
        maxYAxis = []#maximum value for the qz(qxz) coordinate
        
        init = np.random.random((10,10))#data to intialize a figure window
        areaGraph = plt.figure()#handler for the plot
        axisGraph = areaGraph.add_subplot()#handler for the axis
        initGraph = plt.imshow(init)#initialize a plot
        colorbarGraph = plt.colorbar(initGraph)#handler for the colormap
        
        firstImageName = ''#name of the first plot 
        
        lowerValueColorbar = []#minimum value of the colormap from the slidebar
        upperValueColorbar = []#maximum value of the colormap from the slidebar
        fixedUpperValueColorbar = []#current maximum value of the colormap for all the plots
        fixedLowerValueColorbar = []#current minimum value of the colormap for all the plots
        
        fontSizeLabel = 12#fontsize value plot labels
        borderThickness = 2#thickness of the plot border
        tickWidth = 2#width of the tick
        tickLength = 6#length of the tick

        upperBoundIntegration = []#upper limit for the integration
        lowerBoundIntegration = []#lower limit for the integration