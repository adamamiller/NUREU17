""" lightCurve.py 

    This purpose of this program is to produce a light curve with error bars from IRSA data.
    Language: Python 3

    Tanner Leighton

    Written for CIERA Summer Internship, Northwestern University.
    6/28/17
"""
import matplotlib.pyplot as plt
import numpy as np
from astropy.table import Column, Table
from cesium import featurize
#from scipy.optimize import curve_fit

#cesium.featurize.featurize_time_series(…) #example from cesium website

how to get this way to work?

def printFrequency(dataTable): # give it star2.tbl to featurize for star 2

    features_to_use = ["freq1_freq"]

    fset_cesium = featurize.featurize_time_series(times=dataTable["obsmjd"],
                                                  values=dataTable["mag_autocorr"],
                                                  errors=dataTable["magerr_auto"],
                                                  features_to_use=features_to_use)
                                                
    print(fset_cesium)
  
def plotLightCurve(dataTable, period):
    """ This function works with time, mag, error and DOES filter by oid.
        Takes in four lists of data for each of the above mentioned things
        and then makes of light curves (one for each object ID).
        
        Note: This function is most general, i.e. it can deal with sources with any number 
        of object ID's!

        Arguments:
            filename (string) : name of data txt file    
            period (float) : the period of the light curve for phase folding   
    """

    times = dataTable["obsmjd"] # -> xList
    values = dataTable["mag_autocorr"] # -> yList
    errors = dataTable["magerr_auto"]
    oids = dataTable["oid"]
    fids = dataTable["fid"]

    xList = []
    yList = []
    errorList = []
    oidList = []
    fidList = []

    length = len(times)

    for i in range(length):
        xList.append(times[i])
        yList.append(values[i])
        errorList.append(errors[i])
        oidList.append(oids[i])
        fidList.append(fids[i])

    fmtToBeUsed = 'ro'
    xListTemp = []
    yListTemp = []
    errorListTemp = []

    # Let's make a variable called index (to represent the index of a list) and set it equal to 0.
    index = 0

    tempOID = oidList[index]

    oidListLength = len(oidList)
    listLength = oidListLength # better to use this generic name everywhere

    for i in range(oidListLength):
        if tempOID == oidList[i]:
            xListTemp.append(xList[i])
            yListTemp.append(yList[i])
            errorListTemp.append(errorList[i])
            if fidList[i] == 1:
                fmtToBeUsed = 'go'
            else:
                fmtToBeUsed = 'ro'

    xListTempLength = len(xListTemp)

    # phase-folding
    xListPhaseFolded = []
    for i in range(xListTempLength):
        xListPhaseFolded.append((xListTemp[i] % period) / period)

    # plot for the first OID
    plt.errorbar(xListPhaseFolded, yListTemp, yerr = errorListTemp, fmt=fmtToBeUsed, markersize=3) 

    # use .format
    plt.title("Light Curve for Object {}".format(tempOID))
    plt.xlabel("time")
    plt.ylabel("brightness")
    plt.show()

    newOID = oidList[index+1]
    counter = 0
    while newOID == tempOID and counter < (listLength - (index+1)):
        index += 1
        newOID = oidList[index+1]
        counter += 1

    # when here (out of above loop), newOID is truly 'new', unless the oidList only has one oid

    while newOID != tempOID: 

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

        xListTempLength = len(xListTemp)

        # phase-folding
        xListPhaseFolded = []
        for i in range(xListTempLength):
            xListPhaseFolded.append((xListTemp[i] % period) / period)

        plt.errorbar(xListPhaseFolded, yListTemp, yerr = errorListTemp, fmt=fmtToBeUsed, markersize=3) 
        plt.title("Light Curve for Object {}".format(tempOID))
        plt.xlabel("time")
        plt.ylabel("brightness")
        plt.show()

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


if __name__ == '__main__':
    
    filename = input("Enter .tbl filename: ")
    dataTable = Table.read(filename, format='ipac')
    printFrequency(dataTable)
    frequency = float(input("Enter the frequency: "))
    period = 1/frequency
    plotLightCurve(dataTable, period)
    
    # check if period from here matches period from IRSA

    """
    dataTable = Table.read("star2.tbl", format='ipac')

    times=dataTable["obsmjd"] # what the hell is this? a 1D array?
    values=dataTable["mag_autocorr"]
    errors=dataTable["magerr_auto"]

    print(times[0])
    print(len(times))

    # this works! => can throw data into lists and use my current code
    # or can skip the extra step of using lists
    """



    # don't need to read data table twice
    # working on making code only need the .tbl file
    # check if it works next time I code
