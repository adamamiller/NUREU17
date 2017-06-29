import pandas as pd 
import numpy as np 
import os
import json
import sys

source = sys.argv[1]

def JSON_to_DataFrame(source):
	
	#Open source file and load data 
	file_ = open(source)
	json_data = json.load(file_)

	#grab supernovae name frome source file
	SN_name = os.path.splitext(os.path.basename(source))[0]

	#grab only the photometry elements from data
	photometry = json_data[SN_name]['photometry']

	#rid the data where 'upperlimit' is true
	photometry_clean = [x for x in photometry if 'upperlimit' not in x]


	#initialize and create a dataframe out of photometry data
	DF = pd.DataFrame(photometry_clean)
	DF.index.name = "Observation"
	DF = DF.loc[:, ['time', 'magnitude', 'e_magnitude', 'e_upper_magnitude', 'e_lower_magnitude', 'band', 'source', 'telescope']]
	#convert numerical quantities from strings to floats
	DF.time = DF.time.apply(float)
	

	DF.magnitude = DF.magnitude.apply(float)
	DF.e_magnitude = DF.e_magnitude.apply(float)
	DF.e_upper_magnitude = DF.e_upper_magnitude.apply(float)
	DF.e_lower_magnitude = DF.e_lower_magnitude.apply(float)
	
	#save Dataframe as HDF5 file
	DF.to_hdf("../../../OSN_data/HDF5_data/" + SN_name + '.h5', "SN")
	return DF








