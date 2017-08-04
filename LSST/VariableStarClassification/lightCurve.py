""" lightCurve.py 

    This purpose of this program is to produce light curves with error bars (phase-folded and non-phase-folded 
    [i.e. the raw data]) using data downloaded from the Caltech IRSA website.
    
    Language: Python 3

    Tanner Leighton, Adam Miller

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

    # freq1_amplitude1: Get the amplitude of the jth harmonic of the ith frequency from a fitted Lomb-Scargle model.

    features_to_use = ["freq1_freq", "amplitude", "freq1_amplitude1"]

    fset_cesium = featurize.featurize_time_series(times=dataTable["obsmjd"],
                                                  values=dataTable["mag_autocorr"],
                                                  errors=dataTable["magerr_auto"],
                                                  features_to_use=features_to_use)
                                                
    print(fset_cesium)

def plotLightCurves(dataTable, period):
    """ This is a fully general light curve plotting function that works with the dataTable
        downloaded from the Caltech IRSA website to produce phase-folded light curves and non-phase-folded
        light curves (i.e. the raw data) with error bars for each observation.

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

    # color_dict = {"g": "MediumAquaMarine", "R": "FireBrick"}

    length = len(oids)  
    oidsArray = np.empty(length)

    for i in range(length):
        oidsArray[i] = oids[i]

    oidsArraySorted = np.empty(length)
    oidsArraySorted = np.sort(oidsArray) 

    fmtToBeUsed = 'ro'

    index = 0
    swapVar = 0
    tempOID = 0
    newOID = int(oidsArraySorted[index])

    while newOID != tempOID: # while loop because number of unique OID's is not fixed 
        swapVar = newOID
        tempOID = swapVar

        indexesTempOID = np.where(dataTable[3][:] == tempOID)
        fmtToBeUsedNumber = fids[indexesTempOID[0][0]]

        # Filter identifier (1 = g; 2 = R)
        if fmtToBeUsedNumber == 2:
            fmtToBeUsed = 'ro'
        else:
            fmtToBeUsed = 'go'

        # returns figure object and axis object
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize = (8,8), gridspec_kw = {'height_ratios':[1, 3]})
        
        # raw light curve
        ax1.errorbar(times[indexesTempOID], values[indexesTempOID], yerr=errors[indexesTempOID], fmt=fmtToBeUsed, 
            markersize=3, mec="k", mew=0.59)
        ax1.set_ylim(ax1.get_ylim()[::-1])
        ax1.set_title("Light Curve for Object {} (raw data)".format(tempOID))
        ax1.set_xlabel("time")
        ax1.set_ylabel("brightness (mag)")
            
        # phase-folded light curve
        tempLength = len(indexesTempOID[0])
        timesTemp = np.empty(tempLength)
        timesPhaseFolded = np.empty(tempLength)
        timesTemp = times[indexesTempOID]

        for i in range(tempLength):
            timesPhaseFolded[i] = (timesTemp[i] % period) / period

        timesPhaseFoldedPlusOne = np.empty(tempLength)
        for j in range(tempLength):
            timesPhaseFoldedPlusOne[j] = timesPhaseFolded[j]+1
        ax2.errorbar(timesPhaseFolded, values[indexesTempOID], yerr=errors[indexesTempOID], fmt=fmtToBeUsed, 
            markersize=3, mec="k", mew=0.59)
        ax2.set_ylim(ax2.get_ylim()[::-1]) # reversing the y-axis as desired  
        ax2.set_title("Light Curve for Object {} (phase-folded)".format(tempOID))
        ax2.set_xlabel("phase")
        ax2.set_ylabel("brightness (mag)")
        
        fig.tight_layout()
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
    plotLightCurves(dataTable, period)
    print("'period':", period)
    
   

