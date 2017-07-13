#Sample Lightcurve class with Kapernka model 
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import os
from JSON_to_DF import JSON_to_DataFrame
import ntpath
import json
import pandas as pd

class Supernovae:
	
	def __init__(self, path):
		self.name = os.path.splitext(os.path.basename(path))[0]
		self.path = path
		

	def meta_data(self):
		file_ = open(self.path)
		data = json.load(file_)
		self.references = pd.DataFrame((data[self.name]['sources']))
		self.z = pd.DataFrame(data[self.name]['redshift']).value[0]
		
	def load_LightCurves(self):
			df = JSON_to_DataFrame(self.path)
			band_ref = df[['band', 'source']]
			pairs = []
			for row in band_ref.iterrows():
				if(pd.isnull(row[1]['band'])):
					continue
				element = (row[1]['band'], row[1]['source'])
				if(element not in pairs):
					pairs.append(element)
			Lightcurves = {}
			for x in pairs:
				data = df[df.band == x[0]]
				data = data[data.source == x[1]]
				label = str(x[0]) + '_' + str(x[1])
				keys = np.array(x[1].split(','), dtype=int)
				for i in range(len(keys)):
					keys[i] = int(keys[i])
				Lightcurves[label] = filter_lightcurve(data.time.values, data.magnitude.values, data.e_magnitude.values, str(x[0]), keys, self.path)
			self.Lightcurves = Lightcurves

	def serialize(self):
		pass


					
class filter_lightcurve(Supernovae):
	#Lightcurve object constructor
	
	def __init__(self, time, mag , mag_err, band, keys, path, is_mag=True):
		#store time and band
		super().__init__(path)
		super().meta_data()

		self.keys = keys
		self.time = time
		self.band = band
		#If data is passed as magnitudes, convert to flux
		if(is_mag):
			self.flux = self.mag_to_flux(mag)
			self.flux_err = self.mag_err_to_flux_err(mag_err, self.flux)
		else:
			self.flux = mag
			self.flux_err = mag_err
		#shift start times to start at zero 
		self.time = self.time - min(self.time)

	#necessary conversion functions
	@staticmethod
	def mag_to_flux(mag):
		return 10**(-2*mag / 5) 
	
	@staticmethod
	def mag_err_to_flux_err(mag_err, flux):
		const = np.log(10)/2.5
		return const * mag_err * flux

	#returns sources 
	def get_sources(self):
		return self.references.iloc[self.keys - 1, 2].values
		


	

	#Function to calculate RMSE, given a fit function
	def calc_Rchi2(self, fit, degree=0):
		flux_predictions = np.empty(self.flux.shape) * np.nan
		#loop to run 'leave one out' CV
		for ind, f in enumerate(self.flux):
			flux_del = np.delete(self.flux, ind)
			times_del = np.delete(self.time, ind)
			if(degree != 0):
				Coeffs = np.polyfit(times_del, flux_del, degree)
				f = np.poly1d(Coeffs)
				ypred = f(self.time[ind])
			else:
				Coeffs, Covar = curve_fit(fit, times_del, flux_del, self.kap_prior[self.band], bounds=self.kap_param_bounds)
				ypred = fit(self.time[ind], Coeffs[0], Coeffs[1], Coeffs[2], Coeffs[3], Coeffs[4], Coeffs[5])
			flux_predictions[ind] = ypred

		
		
		#Root Mean Square Error calculations
		dif = (flux_predictions - self.flux)/self.flux_err
		temp = np.sum(dif**2)
		temp = temp / (len(self.flux) - 6)
		Rchi2 = np.sqrt(temp)
		return Rchi2


	#create polynomial fit function given degree
	def polynomial_func(self, degree):
		Coeffs = np.polyfit(self.time, self.flux, degree, w=self.flux_err)
		f = np.poly1d(Coeffs)
		return f

	# N degree polynomial fit and return RMSE
	def polynomial_fit_plot(self, degree, plot=True):
		f = self.polynomial_func(degree)
		if(plot):
			bft = np.linspace(self.time[0], self.time[-1], 500)
			plt.plot(bft, f(bft), color='black', label= self.band)
			plt.errorbar(self.time, self.flux, yerr=self.flux_err, fmt='o', color='black', markersize=2.5, label='I band fit')
			ax = plt.gca()
			plt.legend(ncol=2)
			plt.title(str(self.name) + ' ' + str(self.band) + ' band ' + str(degree) + ' degree ' + 'polynomial fit')
			plt.xlabel('time (days)')
			plt.ylabel('relative flux')
			plt.show()
		return self.calc_Rchi2(f, degree=degree)
	
	#initialize kapernka functin paramater bounds, and priors
	kap_param_bounds = ([10*-5,10*-5,0,0,0,0], [1000,100,100,100,100,100])
	kap_prior = {
			'Rc' : [50, 20, 20, 50, 50, 50],
			'g' : [50, 20, 20, 50, 50, 50],
			'I' : [100, 20, 20, 50, 50, 50],
			'J' : [50, 20, 20, 50, 50, 50],
			'B' : [50, 20, 20, 50, 50, 50],
			'U' : [50, 20, 20, 50, 50, 50],
			'V' : [50, 20, 20, 50, 50, 50],
			'W1' : [50, 20, 20, 50, 50, 50],
			'Ic' : [50, 20, 20, 50, 50, 50],

		  }

	#Kapernka model
	def Kapernka_func(self, t, A, B, t_0, t_1, Tfall, Trise):
		
		first = A * (1 + (B * (t - t_1)*(t - t_1)))
		var = -(t - t_0)
		second = np.exp(var / Tfall)
		third = 1 + np.exp(var / Trise)
		return first * (second / third)

	#Plot kapernka best fit and return Rchi2
	def Kapernka_fit_plot(self, plot=True):
		if(plot):
			fitCoeffs, Covars = curve_fit(self.Kapernka_func, self.time, self.flux, self.kap_prior[self.band], sigma=self.flux_err, bounds=self.kap_param_bounds)
			bft = np.linspace(self.time[0], self.time[-1])
			bestfit_flux = self.Kapernka_func(bft, fitCoeffs[0], fitCoeffs[1], fitCoeffs[2], fitCoeffs[3], fitCoeffs[4],fitCoeffs[5])

			plt.errorbar(self.time, self.flux, yerr=self.flux_err, color='blue', label= self.band, fmt = 'o', markersize = 2.5)
			plt.plot(bft, bestfit_flux, color = 'blue', label ='best fit')
			plt.xlabel('time (days)')
			plt.ylabel('relative flux')
			plt.title(str(self.name) + str( self.band) + ' band Kapernka fit')
			plt.show()
		return self.calc_Rchi2(self.Kapernka_func, degree=0)

	#Bazin model
	def Bazin_func(self, t, A, t_0, Trise, Tfall, a1, a2):
		first = A * (1 + (a1 * (t - t_0)) + (a2 * (t - t_0)))
		var = - (t - t_0)
		second = np.exp(var / Tfall)
		third =  1 + np.exp(var / Trise)  
		return first * (second / third)

	#Plot Bazin best fit and return Rchi2
	def Bazin_fit_plot(self, plot=True):
		if(plot):
			fitCoeffs, Covars = curve_fit(self.Bazin_func, self.time, self.flux, self.kap_prior[self.band], sigma=self.flux_err,  bounds=self.kap_param_bounds)
			bft = np.linspace(self.time[0], self.time[-1])
			bestfit_flux = self.Bazin_func(bft, fitCoeffs[0], fitCoeffs[1], fitCoeffs[2], fitCoeffs[3], fitCoeffs[4],fitCoeffs[5])

			plt.errorbar(self.time, self.flux, yerr=self.flux_err, color='blue', label= self.band, fmt = 'o', markersize = 2.5)
			plt.plot(bft, bestfit_flux, color = 'blue', label ='best fit')
			plt.show()
		return self.calc_Rchi2(self.Bazin_func, degree=0)








