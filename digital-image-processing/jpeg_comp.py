#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.cm as cm
from scipy.fftpack import dct as dct
from scipy.fftpack import idct as idct
from scipy.fftpack import dst as dst
from scipy.fftpack import idst as idst
from scipy.fftpack import fft as fft
from scipy.fftpack import ifft as ifft
from PIL import Image

filename = 'jen512.jpg'
int_sample = mpimg.imread(filename)
sample = int_sample.astype(np.float32)
plt.subplot(1, 3, 1)
plt.imshow(sample, interpolation='none', cmap=plt.get_cmap('gray'))       
# plt.imshow(sample, interpolation='none', cmap = cm.gray)


# Fast Fourier Transform
def getFFT(matrix):
    for x in range (64):
        i1 = 8*x
        i2 = 8*(x+1)
        for y in range (64):
            j1 = 8*y
            j2 = 8*(y+1)
            block = matrix[i1:i2,j1:j2]
            matrix[i1:i2,j1:j2] = fft(block).real
    return matrix

# Direct Cosine Transform
def getDCT(matrix):
    for x in range (64):
        i1 = 8*x
        i2 = 8*(x+1)
        for y in range (64):
            j1 = 8*y
            j2 = 8*(y+1)
            block = matrix[i1:i2,j1:j2]
            matrix[i1:i2,j1:j2] = dct(block)
            # matrix[i1:i2,j1:j2] = dct(dct(block, axis=0, norm="ortho"), axis=1, norm="ortho")
    # print np.max(matrix)
    return matrix
    
# Direct Sine Transform
def getDST(matrix):
    for x in range (64):
        i1 = 8*x
        i2 = 8*(x+1)
        for y in range (64):
            j1 = 8*y
            j2 = 8*(y+1)
            block = matrix[i1:i2,j1:j2]
            matrix[i1:i2,j1:j2] = dst(block)
            # matrix[i1:i2,j1:j2] = dct(dct(block, axis=0, norm="ortho"), axis=1, norm="ortho")
    # print np.max(matrix)
    return matrix
    
# Quantization
def setQuantization(n,map,max):
    # print max
    return n*(np.floor(map/n))
    
# Fast Fourier Transform
def getIFFT(matrix):
    for x in range (64):
        i1 = 8*x
        i2 = 8*(x+1)
        for y in range (64):
            j1 = 8*y
            j2 = 8*(y+1)
            block = matrix[i1:i2,j1:j2]
            matrix[i1:i2,j1:j2] = ifft(block).real
    return matrix
    
# Inverse Direct Cosine Transform
def getIDCT(matrix):
    for x in range (64):
        i1 = 8*x
        i2 = 8*(x+1)
        for y in range (64):
            j1 = 8*y
            j2 = 8*(y+1)
            block = matrix[i1:i2,j1:j2]
            matrix[i1:i2,j1:j2] = idct(block)
            # matrix[i1:i2,j1:j2] = dct(dct(block, axis=0, norm="ortho"), axis=1, norm="ortho")
    # print np.max(matrix)
    return matrix

# Inverse Direct Sine Transform
def getIDST(matrix):
    for x in range (64):
        i1 = 8*x
        i2 = 8*(x+1)
        for y in range (64):
            j1 = 8*y
            j2 = 8*(y+1)
            block = matrix[i1:i2,j1:j2]
            matrix[i1:i2,j1:j2] = idst(block)
            # matrix[i1:i2,j1:j2] = dct(dct(block, axis=0, norm="ortho"), axis=1, norm="ortho")
    # print np.max(matrix)
    return matrix

# matrix_boat = getFFT(matrix_boat)
max = np.max(sample)
matrix = getDCT(1.*sample)
# matrix = getDST(1.*sample)
# matrix = getFFT(1.*sample)
matrix = setQuantization(32,matrix,max)
matrix2 = getIDCT(1.*matrix)
# matrix2 = getIDST(1.*matrix)
# matrix2 = getIFFT(1.*matrix)



# Show IMAGE
plt.subplot(1, 3, 1)
plt.imshow(matrix, interpolation='none', cmap=plt.get_cmap('gray'))
plt.subplot(1, 3, 2)
plt.imshow(matrix2, interpolation='none', cmap=plt.get_cmap('gray'))
# plt.imshow(matrix, interpolation='none', cmap = cm.gray)
plt.show()
        