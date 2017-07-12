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
    """ This function obtain the frequency using cesium, which implies the period.

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
        downloaded from the Caltech IRSA website to produce phase-folded light curves with 
        error bars for each oid.

        Caltech IRSA website: http://irsa.ipac.caltech.edu/cgi-bin/Gator/nph-scan?projshort=PTF

        Arguments:
            dataTable (array-like) : data table from Caltech IRSA website (.tbl)   
            period (float) : the period of the light curve for phase folding (obtained with cesium) 
    """

    times = dataTable["obsmjd"] 
    values = dataTable["mag_autocorr"] 
    errors = dataTable["magerr_auto"]
    oids = dataTable["oid"]
    fids = dataTable["fid"]

    length = len(oids)  
    oidsArray = np.empty(length)

    for i in range(length):
        oidsArray[i] = oids[i]

    oidsArraySorted = np.empty(length)
    oidsArraySorted = np.sort(oidsArray) 

    fmtToBeUsed = 'ro'

    # Let's make a variable called index (to represent the index of a list) and set it equal to 0.
    index = 0
    swapVar = 0
    tempOID = 0
    newOID = int(oidsArraySorted[index])

    while newOID != tempOID: # while loop because number of unique OID's is not fixed 
        swapVar = newOID
        tempOID = swapVar

        indexesTempOID = np.where(dataTable[3][:] == tempOID)
        fmtToBeUsedNumber = fids[indexesTempOID[0][0]]

        if fmtToBeUsedNumber == 2:
            fmtToBeUsed = 'ro'
        else:
            fmtToBeUsed = 'go'

        # phase-folding
        tempLength = len(indexesTempOID[0])
        timesTemp = np.empty(tempLength)
        timesPhaseFolded = np.empty(tempLength)
        timesTemp = times[indexesTempOID]

        for i in range(tempLength):
            timesPhaseFolded[i] = (timesTemp[i] % period) / period

        timesPhaseFoldedPlusOne = np.empty(tempLength)
        for j in range(tempLength):
            timesPhaseFoldedPlusOne[j] = timesPhaseFolded[j]+1

        plt.errorbar(timesPhaseFolded, values[indexesTempOID], yerr=errors[indexesTempOID], fmt=fmtToBeUsed, markersize=3)
        plt.errorbar(timesPhaseFoldedPlusOne, values[indexesTempOID], yerr=errors[indexesTempOID], fmt=fmtToBeUsed, markersize=3)
        plt.gca().invert_yaxis() 
        plt.title("Light Curve for Object {}".format(tempOID))
        plt.xlabel("phase")
        plt.ylabel("brightness (mag)")
        plt.show()
        
        index += 1
        newOID = int(oidsArraySorted[index]) 
        # at this point, newOID will equal tempOID, unless the there is only one oid of that variety
        while (newOID == tempOID and index < (length-1)): 
            index += 1
            newOID = int(oidsArraySorted[index])

if __name__ == '__main__':
    filename = input("Enter .tbl filename: ")
    dataTable = Table.read(filename, format='ipac')
    printFrequency(dataTable)
    frequency = float(input("Enter the frequency: "))
    period = 1/frequency
    plotLightCurve(dataTable, period)
    print("period:", period)



    
    
   

