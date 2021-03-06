import pandas as pd 
import numpy as np 
import os
import json
import sys



def JSON_to_DataFrame(source):
	
	#Open source file and load data 
	file_ = open(source)
	json_data = json.load(file_)

	#grab supernovae name frome source file
	SN_name = os.path.splitext(os.path.basename(source))[0]

	#If there are no photometric elements, ignore 
	if('photometry' not in json_data[SN_name]):
		return 
	#grab only the photometry elements from data
	photometry = json_data[SN_name]['photometry']
	
	#rid the data where 'upperlimit' is true
	photometry_clean = [x for x in photometry if 'upperlimit' not in x]
	
	#minimum number of elements needed for analysis 
	
	#initialize and create a dataframe out of photometry data
	DF = pd.DataFrame(photometry_clean)
	
	#If bands arent specified, ignore
	if('band' not in DF):
		return
	
	DF.index.name = "Observation"
	
	#Reduce DF to these columns, only if they exist
	DF = DF.loc[:, DF.columns.isin(['time', 'magnitude', 'e_magnitude', 'e_upper_magnitude', 'e_lower_magnitude', 'band', 'source', 'telescope'])]
	

	#convert numerical quantities from strings to floats
	DF.time = DF.time.apply(float)
	if('magnitude' in DF.columns):
		DF.magnitude = DF.magnitude.apply(float)
	if('e_magnitude' in DF.columns):
		DF.e_magnitude = DF.e_magnitude.apply(float)
	if('e_upper_magnitude' in DF.columns):
		DF.e_upper_magnitude = DF.e_upper_magnitude.apply(float)
	if('e_lower_magnitude' in DF.columns):
		DF.e_lower_magnitude = DF.e_lower_magnitude.apply(float)

	file_.close()

	
	#save Dataframe as HDF5 file
	DF.to_hdf("../../../OSC_data/HDF5_data/" + SN_name + '.h5', "SN")
	return DF









