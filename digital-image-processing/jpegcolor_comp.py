#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.fftpack import dct as dct
from scipy.fftpack import idct as idct

# Convert RGB to YCbCr.
def ColorYCbCrInverse(RGBMatrix):
    xy = np.zeros(RGBMatrix.shape)
    matrix = np.matrix(
        [[ 0.299  , 0.587   , 0.114  ],
         [-0.169  ,-0.331   , 0.500  ],
         [ 0.500  ,-0.419   ,-0.081 ]])
    for x in range(512):
        for y in range(512):
            RGBvector = RGBMatrix[x,y,:]
            xy[x,y,:] = np.dot(matrix,RGBvector)+ np.array([0.,128./255.,128./255.])
    return xy
    
    
# YCrCb color model    
def ColorYCbCr(YBRMatrix):
    xy = np.zeros(YBRMatrix.shape)
    matrix = np.matrix(
        [[ 1.000 , 0.000 ,  1.400  ],
         [ 1.000 ,-0.343 , -0.711  ],
         [ 1.000 , 1.765 ,  0.000  ]])
    for x in range(512):
        for y in range(512):
            YBRvector = YBRMatrix[x,y,:]- np.array([0.,128./255.,128./255.])
            xy[x,y,:] = np.dot(matrix,YBRvector)
    return xy


filename = 'jencolor.png'
sample = mpimg.imread(filename)


# Direct Cosine Transform
def getDCT(matrix):
    xy = np.zeros(matrix.shape)
    for x in range (64):
        i1 = 8*x
        i2 = 8*(x+1)
        for y in range (64):
            j1 = 8*y
            j2 = 8*(y+1)
            block = matrix[i1:i2,j1:j2]
            xy[i1:i2,j1:j2] = dct(block)
    return xy
    

# Quantization
def setQuantization(n,map,max):
    # print max
    return n*(np.floor(map/n))
    
    
# Inverse Direct Cosine Transform
def getIDCT(matrix):
    xy = np.zeros(matrix.shape)
    for x in range (64):
        i1 = 8*x
        i2 = 8*(x+1)
        for y in range (64):
            j1 = 8*y
            j2 = 8*(y+1)
            block = matrix[i1:i2,j1:j2]
            xy[i1:i2,j1:j2] = idct(block)
    return xy

ySample = ColorYCbCrInverse(sample)
del sample
ySample1 = np.zeros(ySample.shape)
ySample2 = np.zeros(ySample.shape)
ySample2[:,:,0] = ySample[:,:,0]
ySample2[:,:,1] = ySample[:,:,1] 
ySample2[:,:,2] = ySample[:,:,2]        


# # Red Channel
ySample1[:,:,0] = getDCT(ySample[:,:,0])
# ySample1[:,:,0] = setQuantization(16,ySample1[:,:,0],max)
ySample2[:,:,0] = getIDCT(ySample1[:,:,0])


# # Green Channel
# ySample1[:,:,1] = getDCT(ySample[:,:,1])
# # ySample1[:,:,1] = setQuantization(16,ySample1[:,:,1],max)
# ySample2[:,:,1] = getIDCT(ySample1[:,:,1])


# # Blue Channel
# ySample1[:,:,2] = getDCT(ySample[:,:,2])
# # ySample1[:,:,2] = setQuantization(16,ySample1[:,:,0],max)
# ySample2[:,:,2] = getIDCT(ySample1[:,:,2])




# Show IMAGE
plt.subplot(1, 3, 1)
plt.imshow(ySample, interpolation='none')   
# plt.subplot(1, 3, 2)
# plt.imshow(ySample1, interpolation='none')
plt.subplot(1, 3, 3)
plt.imshow(ySample2, interpolation='none')
# plt.imshow(matrix, interpolation='none', cmap = cm.gray)
plt.show()
        