#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage import exposure
from collections import Counter

def hist_eq(image):
    content = Counter(image.ravel())
    pixels = 1.*np.size(image)
    weight = np.zeros(np.shape(image))
    for i in range (np.size(image,0)):
        for j in range (np.size(image,1)):
            item = image[i,j]
            # print item
            for pixel in range(item):
                weight[i,j] += pixel*content[pixel]/pixels
            # print weight[i,j]
            image[i,j] = image[i,j]*weight[i,j]/255.
    return image
    


filename = 'nasa_curiosity_fcam_2016_Jan_23.tiff'
filename = 'nasa_curiosity_crop_2016_Jan_23.tiff'
sampleRGB = mpimg.imread(filename)
if len(np.shape(sampleRGB)) == 2:
    sample = sampleRGB
if len(np.shape(sampleRGB)) == 3:
    sample = sampleRGB[:,:,0]
print np.size(sampleRGB,1)
img_eq = exposure.equalize_hist(sample)

# Show IMAGE
plt.close('all')
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex=False, sharey=False, figsize=(1,1), dpi=80)

mEqual = hist_eq(sample)
ax1.imshow(mEqual, interpolation='none', cmap=plt.get_cmap('gray'))
ax1.axis('off')
ax2.hist(mEqual.ravel(), bins=256, histtype='step', color='green')
ax3.imshow(img_eq, interpolation='none', cmap=plt.get_cmap('gray'))
ax3.axis('off')
ax4.hist(img_eq.ravel(), bins=256, histtype='bar', color='green')
plt.show()
        