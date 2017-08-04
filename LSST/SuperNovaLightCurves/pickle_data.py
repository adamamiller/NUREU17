import os 
from Lightcurve_class import *


directory = "../../../OSC_data/JSON_data/"

#Loop through JSON files, loading them and pickling lightcurves and meta data
for root, dirs, files in os.walk(directory):
	for file in files:
		file_name, ext = os.path.splitext(os.path.basename(file))
		if(ext == '.json'):
			SN = Supernovae(root + "/" + file)
			#if(os.path.exists("../../../OSC_data/pickled_data/" + file_name + ".pickle")):
			#	print(file_name + "exists")
			#	continue
			print("processing " + file_name)
			SN.load_LightCurves()
			SN.meta_data()
			SN.serialize()


#Clean up all pickle files that don't have photometry data
for root, dirs, files in os.walk("../../../OSC_data/pickled_data"):
	for file in files:
		SN = deserialize("../../../OSC_data/pickled_data/" + file)
		if(not hasattr(SN, 'Lightcurves')):
			os.remove("../../../OSC_data/pickled_data/" + file)
			print(file + " removed")

		else:
			print(file + " saved")





			


			
			




	
	
