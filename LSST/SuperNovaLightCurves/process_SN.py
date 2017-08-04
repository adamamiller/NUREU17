#import necessary python libraries
import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit, minimize
import pandas as pd
import math
from JSON_to_DF import JSON_to_DataFrame
from Lightcurve_class import *
import celerite
import pickle

#Create Kernels for Gaussian Process

#Real term parameter initialization
a = 1e-5
c = 1
#Matern term parameter initialization
sig = 1e-5
rho = 100

#Bounds on parameters 
bounds = dict(log_a = (-15,15), log_c = (-15,15))
bounds = dict(log_sigma = (-15, 15), log_rho = (-15, 15))

#Create Kernels
Real_Kernel = celerite.terms.RealTerm(log_a = np.log(a), log_c = np.log(c), bounds=bounds)
Matern_Kernel = celerite.terms.Matern32Term(log_sigma = np.log(sig), log_rho = np.log(rho))





#Create lists to store Rchi2 and median values for given fit
Poly4_median = []
Poly4_Rchi2 = []

Poly6_median = []
Poly6_Rchi2 = []

Poly8_median = []
Poly8_Rchi2 = []

GP_Real_median = []
GP_Real_Rchi2 = []

GP_Matern_median = []
GP_Matern_Rchi2 = []

Kapernka_median = []
Kapernka_Rchi2 = []

Bazin_median = []
Bazin_Rchi2 = []



#Loop through pickle files gathering Rchi2 and median data for each fit
directory = "../../../OSC_data/pickled_data/"
for roots, dirs, files in os.walk(directory):
	for file in files:
		SN = deserialize(directory + file)
		for key in SN.Lightcurves.keys():
			if(SN.Lightcurves[key].n_good_obs < 3):
				continue
			print(SN.name, key)
			SN.Lightcurves[key].polynomial_fit_plot(4, plot=False)
			SN.Lightcurves[key].polynomial_fit_plot(6, plot=False)
			SN.Lightcurves[key].polynomial_fit_plot(8, plot=False)
			SN.Lightcurves[key].Kapernka_fit_plot(plot=False)
			SN.Lightcurves[key].Bazin_fit_plot(plot=False)
			SN.Lightcurves[key].Gaussian_process(Real_Kernel, plot=False)
			SN.Lightcurves[key].Gaussian_process(Matern_Kernel, plot=False)
			print("Models fitted")
			for fit, value in SN.Lightcurves[key].Rchi2.items():
				if(fit == 'poly_4'):
					Poly4_Rchi2.append(value)
				elif(fit == 'poly_6'):
					Poly6_Rchi2.append(value)
				elif(fit == 'poly_8'):
					Poly8_Rchi2.append(value)
				elif(fit == 'GP_1'):
					GP_Real_Rchi2.append(value)
				elif(fit == 'GP_2'):
					GP_Matern_Rchi2.append(value)
				elif(fit == 'Kapernka'):
					Kapernka_Rchi2.append(value)
				elif(fit == 'Bazin'):
					Bazin_Rchi2.append(value)
			print("Rchi2 loaded")
			for fit, value in SN.Lightcurves[key].medians.items():
				if(fit == 'poly_4'):
					Poly4_median.append(value)
				elif(fit == 'poly_6'):
					Poly6_median.append(value)
				elif(fit == 'poly_8'):
					Poly8_median.append(value)
				#elif(key == 'GP'):
					#GP_Real_median.append(value)
				elif(fit == 'GP'):
					GP_Matern_median.append(value)
				elif(fit == 'Kapernka'):
					Kapernka_median.append(value)
				elif(fit == 'Bazin'):
					Bazin_median.append(value)
			print("medians loaded")


print(len(Poly6_median))
print(len(Poly6_Rchi2))

