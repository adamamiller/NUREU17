""" lightCurve.py 

    This purpose of this program is to produce a light curve with error bars.
    Language: Python 3

    Tanner Leighton

    Written for CIERA Summer Internship, Northwestern University.
    6/25/17
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def plotLightCurve(filename):
    """ This function just works with time, mag, and error,
        i.e. does not filter by oid.

        Arguments:
            filename (string) : name of data txt file       
    """

    xList = []
    yList = []
    errorList = []

    fin = open(filename)
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

    timeCutOff = int(input("Enter time cut-off by looking at first plot: "))

    xListSmallTime = []
    xListLargeTime = []

    yListSmallTime = []
    yListLargeTime = []

    errorListSmallTime = []
    errorListLargeTime = []

    length = len(xListPrime)
    for i in range(length):
        if xListPrime[i] < timeCutOff:
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
  
def plotLightCurvePrime(filename):
    """ This function works with time, mag, error and DOES filter by oid.
        Takes in four lists of data for each of the above mentioned things
        and then makes three plots (of the three objects), which is what
        is meant by filtering by oid

        Arguments:
            filename (string) : name of data txt file       
    """

    xList = []
    yList = []
    errorList = []
    oidList = []
    fidList = []

    fin = open(filename)
    for line in fin:
        #line = line.strip()
        line = line.split() # Splits each line into constituent numbers. 
        xList.append(line[0])
        yList.append(line[1])
        errorList.append(line[2])
        oidList.append(line[3])
    fin.close()

    xListPrime = []
    for element in xList:
        xListPrime.append(float(element))
    xList = xListPrime # so not using 'xListPrime' going forward

    yListPrime = []
    for element in yList:
        yListPrime.append(float(element))
    yList = yListPrime

    errorListPrime = []
    for element in errorList:
        errorListPrime.append(float(element))
    errorList = errorListPrime

    oidListPrime = []
    for element in oidList:
        oidListPrime.append(int(element))
    oidList = oidListPrime

    fidListPrime = []
    for element in fidList:
        fidListPrime.append(int(element))
    fidList = fidListPrime

    """
    This plots all objects ID's on same plot:
    plt.errorbar(xList, yList, yerr = errorList, fmt='ro', markersize=3) 
    plt.title("Star 2 Light Curve")
    plt.xlabel("time")
    plt.ylabel("brightness")
    plt.show()
    """

    xListTemp = []
    yListTemp = []
    errorListTemp = []

    # first make the code for three oid's
    # then generalize code so it works for any number
    # (generalized code better but don't need to right now,
    # not for what I am trying to do here)

    tempOID = oidList[0]

    oidListLength = len(oidList)

    for i in range(oidListLength):
        if tempOID == oidList[i]:
            xListTemp.append(xList[i])
            yListTemp.append(yList[i])
            errorListTemp.append(errorList[i])

    # plot for oid #1
    plt.errorbar(xListTemp, yListTemp, yerr = errorListTemp, fmt='go', markersize=3) 
    plt.title("Star 2 Light Curve for Object 226831060005494")
    plt.xlabel("time")
    plt.ylabel("brightness")
    plt.show()

    tempOID = oidList[1]
    for i in range(oidListLength):
        if tempOID == oidList[i]:
            xListTemp.append(xList[i])
            yListTemp.append(yList[i])
            errorListTemp.append(errorList[i])

    # plot for oid #2
    plt.errorbar(xListTemp, yListTemp, yerr = errorListTemp, fmt='ro', markersize=3) 
    plt.title("Star 2 Light Curve for Object 226832060006908")
    plt.xlabel("time")
    plt.ylabel("brightness")
    plt.show()

    tempOID = oidList[10]
    for i in range(oidListLength):
        if tempOID == oidList[i]:
            xListTemp.append(xList[i])
            yListTemp.append(yList[i])
            errorListTemp.append(errorList[i])

    # plot for oid #3
    plt.errorbar(xListTemp, yListTemp, yerr = errorListTemp, fmt='ro', markersize=3) 
    plt.title("Star 2 Light Curve for Object 26832000005734")
    plt.xlabel("time")
    plt.ylabel("brightness")
    plt.show()

if __name__ == '__main__':
    filename = input("Enter the data file name: ")
    plotLightCurvePrime(filename)
