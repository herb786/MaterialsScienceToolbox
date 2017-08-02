import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcol

stringFile = open("mycolor.txt")
lstR, lstG, lstB = [], [], []
for line in stringFile:
    line = line.strip()
    if len(line) != 0:
        strLin = line.split()
        lstR.append(float(strLin[0]))
        lstG.append(float(strLin[1]))
        lstB.append(float(strLin[2]))
red = np.array(lstR)/255.
blue = np.array(lstB)/255.
green = np.array(lstG)/255.
xval = np.linspace(0,1,len(red))
file = open('convert.dat','w')
file.write('red:(')
for i in range (len(xval)):
	file.write("( %2.3f, %2.3f, %2.3f)," % (xval[i],red[i],red[i]))
file.write('),\n')
file.write('green:(')
for i in range (len(xval)):
	file.write("( %2.3f, %2.3f, %2.3f)," % (xval[i],green[i],green[i]))
file.write('),\n')
file.write('blue:(')
for i in range (len(xval)):
	file.write("( %2.3f, %2.3f, %2.3f)," % (xval[i],blue[i],blue[i]))
file.write(')')