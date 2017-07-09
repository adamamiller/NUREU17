""" lightCurve.py 

    This purpose of this program is to produce phase-folded light curves (with error bars) 
    using data downloaded from the Caltech IRSA website.
    
    Language: Python 3

    Tanner Leighton

    Written for CIERA Summer Internship - Variable Star Classification 
    Northwestern University
"""
import matplotlib.pyplot as plt
import numpy as np
from astropy.table import Column, Table 
from cesium import featurize

def printFrequency(dataTable): 
    """ This function obtain the frequency using cesium, and this implies the period!

        Arguments:
            dataTable (array-like) : this is the .tbl data file downloaded from Caltech
            IRSA website
    """

    features_to_use = ["freq1_freq"]

    fset_cesium = featurize.featurize_time_series(times=dataTable["obsmjd"],
                                                  values=dataTable["mag_autocorr"],
                                                  errors=dataTable["magerr_auto"],
                                                  features_to_use=features_to_use)
                                                
    print(fset_cesium)
  
def plotLightCurve(dataTable, period):
    """ This is a fully general light curve plotting function that works with the dataTable
        downloaded from the Caltech IRSA website to produce phase-folded light curves for 
        each oid.

        Caltech IRSA website: http://irsa.ipac.caltech.edu/cgi-bin/Gator/nph-scan?projshort=PTF

        Arguments:
            dataTable (array-like) : data table from Caltech IRSA website (.tbl)   
            period (float) : the period of the light curve for phase folding (obtained with cesium) 
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

    for i in range(length): # could turn this into list comprehensions to be more efficient
        xList.append(times[i])
        yList.append(values[i])
        errorList.append(errors[i])
        oidList.append(oids[i])
        fidList.append(fids[i])   

    fmtToBeUsed = 'ro'

    # Let's make a variable called index (to represent the index of a list) and set it equal to 0.
    index = 0
    newOID = oidList[index]
    tempOID = 0
    oidListLength = len(oidList)
    listLength = oidListLength # better to use this generic name everywhere

    while tempOID != newOID: # while loop because number of unique OID's is not fixed 
        tempOID = newOID
        xListTemp = []
        yListTemp = []
        errorListTemp = []

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

        xListPhaseFoldedPlusOne = []
        for element in xListPhaseFolded:
            elementPrime = element + 1
            xListPhaseFoldedPlusOne.append(elementPrime)

        # plotting phase-folded light curve
        plt.errorbar(xListPhaseFolded, yListTemp, yerr=errorListTemp, fmt=fmtToBeUsed, markersize=3)
        plt.errorbar(xListPhaseFoldedPlusOne, yListTemp, yerr=errorListTemp, fmt=fmtToBeUsed, markersize=3)
        plt.gca().invert_yaxis() 
        plt.title("Light Curve for Object {}".format(tempOID))
        plt.xlabel("phase")
        plt.ylabel("brightness (mag)")
        plt.show()

        newOID = oidList[index+1] 
        # at this point, newOID might not be new oid, unless the first oid only showed up once
        counter = 0
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
    print("period:", period)

   

