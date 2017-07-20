import os 
from Lightcurve_class import *


directory = "../../../OSC_data/JSON_data/"


for root, dirs, files in os.walk(directory):
	for file in files:
		file_name = os.path.splitext(os.path.basename(file))[0]
		if(file_name[:2] == "SN"):
			SN = Supernovae(root + "/" + file)
			if(os.path.exists("../../../OSC_data/pickled_data/" + file_name + ".pickle")):
				print(file_name + "exists")
				continue
			print("processing " + file_name)
			SN.load_LightCurves()
			SN.meta_data()
			SN.serialize()
			




	
	
