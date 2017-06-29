""" lightCurve.py 

    This purpose of this program is to produce a light curve with error bars.
    Language: Python 3

    Tanner Leighton

    Written for CIERA Summer Internship, Northwestern University.
    6/28/17
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
  
"""
Below is my most updated lightCurve plotting function => more general, i.e. works with a 
more general data set; in particular, the previous version assumes the oid changes at 
particular locations in the list, and the software of this new version determines that. 
This version still assumes there are at least two unique object id's and no more than three.
"""  
def plotLightCurve(filename):
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
        fidList.append(line[4])
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

    fmtToBeUsed = 'ro'
    xListTemp = []
    yListTemp = []
    errorListTemp = []

    # first make the code for three oid's
    # then generalize code so it works for any number
    # (generalized code better but don't need to right now,
    # not for what I am trying to do here)

    index = 0

    tempOID = oidList[index]

    oidListLength = len(oidList)
    listLength = oidListLength # better to use this generic name everywhere

    #print("oidList: ", oidList)
    #print("fidList: ", fidList)

    for i in range(oidListLength):
        if tempOID == oidList[i]:
            xListTemp.append(xList[i])
            yListTemp.append(yList[i])
            errorListTemp.append(errorList[i])
            if fidList[i] == 1:
                fmtToBeUsed = 'go'
            else:
                fmtToBeUsed = 'ro'

    # plot for oid #1
    plt.errorbar(xListTemp, yListTemp, yerr = errorListTemp, fmt=fmtToBeUsed, markersize=3) 

    # use .format
    plt.title("Star 2 Light Curve for Object {}".format(tempOID))
    plt.xlabel("time")
    plt.ylabel("brightness")
    plt.show()

    """

    # here we need to find the index of the next unique oid

    # this block is not completely general
    # it assumes there is at least two unique oid's in the list (starData.txt's from IRSA)
    # need to update
    newOID = oidList[index+1]
    while newOID == tempOID:
            index += 1
            newOID = oidList[index+1]

    """

    newOID = oidList[index+1]
    counter = 0
    while newOID == tempOID and counter < (listLength - (index+1)):
        index += 1
        newOID = oidList[index+1]
        counter += 1

    # when here (out of above loop), newOID is truly 'new', if it is :)
    # if there is only one oid, code will not enter through next if statement and will be done
    # as desired

    while newOID != tempOID: # <- most recent change

        firstIndexOfNextOid = index+1

        tempOID = oidList[firstIndexOfNextOid]
        for i in range(oidListLength):
            if tempOID == oidList[i]:
                xListTemp.append(xList[i])
                yListTemp.append(yList[i])
                errorListTemp.append(errorList[i])
                if fidList[i] == 1:
                    fmtToBeUsed = 'go'
                else:
                    fmtToBeUsed = 'ro'

        plt.errorbar(xListTemp, yListTemp, yerr = errorListTemp, fmt=fmtToBeUsed, markersize=3) 
        plt.title("Star 2 Light Curve for Object {}".format(tempOID))
        plt.xlabel("time")
        plt.ylabel("brightness")
        plt.show()

        # need to find first index of next OID (the third oid in the list, if it exists)
        # need to also make code for if 2nd oid does not exist (general version - but acutally
        # for our purposes here, we don't need that)

        newOID = oidList[index+1] # initially assigning newOID the same value as tempOID
        counter = 0
        # listLength - (index+1) works!
        # newOID is (perhaps) altered in following while loop
        while newOID == tempOID and counter < (listLength - (index+1)):
            index += 1
            newOID = oidList[index+1]
            counter += 1

        firstIndexOfNextOid = index+1
        newOID = oidList[firstIndexOfNextOid]

# oldNews
def plotLightCurveOld(filename):
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

if __name__ == '__main__':
    filename = input("Enter the data file name: ")
    plotLightCurve(filename)
    
