""" lightCurve.py 

    This purpose of this program is to produce a light curve from data for time and brightness.

    Language: Python 3

    Tanner Leighton

    Written for CIERA Summer Internship, Northwestern University.
    6/22/17
"""

"""First let's import the libraries that will provide you with some useful functions.
We'll start by importing the matplotlib, numpy, and curve_fit libraries"""
#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

xList = []
yList = []
errorList = []

fin = open("star1DataPrime.txt")
for line in fin:
    #line = line.strip()
    line = line.split() # Splits each line into constituent numbers. 
    xList.append(line[0])
    yList.append(line[1])
    errorList.append(line[2])
fin.close()

xListPrime = []
for element in xList:
    xListPrime.append(float(element))

yListPrime = []
for element in yList:
    yListPrime.append(float(element))

errorListPrime = []
for element in errorList:
    errorListPrime.append(float(element))

plt.errorbar(xListPrime, yListPrime, yerr = errorListPrime, fmt='ro', markersize=3) 
plt.title("Star 1 Light Curve")
plt.xlabel("time")
plt.ylabel("brightness")
plt.show()

xListSmallTime = []
xListLargeTime = []

yListSmallTime = []
yListLargeTime = []

errorListSmallTime = []
errorListLargeTime = []

length = len(xListPrime)
for i in range(length):
    if xListPrime[i] < 55600:
        xListSmallTime.append(xListPrime[i])
        yListSmallTime.append(yListPrime[i])
        errorListSmallTime.append(errorListPrime[i])
    else:
        xListLargeTime.append(xListPrime[i])
        yListLargeTime.append(yListPrime[i])
        errorListLargeTime.append(errorListPrime[i])

plt.errorbar(xListSmallTime, yListSmallTime, yerr = errorListSmallTime, fmt='ro', markersize=3) 
plt.title("Star 1 Light Curve 1")
plt.xlabel("time")
plt.ylabel("brightness")
plt.show()

plt.errorbar(xListLargeTime, yListLargeTime, yerr = errorListLargeTime, fmt='ro', markersize=3) 
plt.title("Star 1 Light Curve 2")
plt.xlabel("time")
plt.ylabel("brightness")
plt.show()
