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

errorVal = 0.1

plt.errorbar(xListPrime, yListPrime, yerr = errorListPrime, fmt='ro', markersize=3) 

# Label the plot with your own titles, make sure they are strings (enclosed in quotation marks)
plt.title("Star 1 Light Curve")
plt.xlabel("time")
plt.ylabel("brightness")
plt.show()
