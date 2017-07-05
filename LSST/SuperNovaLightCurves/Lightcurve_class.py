#Sample Lightcurve class with Kapernka model 
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt



class Lightcurve:
	
	#Lightcurve object constructor
	def __init__(self, time, mag , mag_err, band, data_type):
		#If data is passed as magnitudes, convert to flux
		if(data_type == 'mag'):
			self.time = time
			self.flux = self.mag_to_flux(mag)
			self.flux_err = self.mag_err_to_flux_err(mag, mag_err, self.flux)
			self.band = band
		#If data is passed as flux, no conversion necessary
		elif(data_type == 'flux'):
			self.time = time
			self.flux = mag
			self.flux_err = mag_err
			self.band = band
		#Error thrown is type not specified correctly
		else:
			raise ValueError('data type must be either "mag" or "flux"')

		#shift start times to a zero point
		self.time = self.time - min(self.time)


	#necessary conversion functions
	@staticmethod
	def mag_to_flux(mag):
		return 10**(-2*mag / 5) 

	
	def mag_err_to_flux_err(self, mag, mag_err, flux):
		mag_max = mag + mag_err
		flux_max = self.mag_to_flux(mag_max)
		flux_error = flux_max - flux
		return flux_error
	

	#Function to calculate RMSE, given a fit function
	def calc_RMSE_func(self, flux, times, flux_errors, band, fit, degree=0):
		flux_predictions = []
		#loop to run 'leave one out' CV
		for ind, f in enumerate(flux):
			flux_del = np.delete(flux, ind)
			times_del = np.delete(times, ind)
			if(degree != 0):
				Coeffs = np.polyfit(times_del, flux_del, degree)
				f = np.poly1d(Coeffs)
				ypred = f(times[ind])
			else:
				Coeffs, Covar = curve_fit(fit, times_del, flux_del, self.kap_prior[self.band], bounds= self.kap_param_bounds)
				ypred = fit(times[ind], Coeffs[0], Coeffs[1], Coeffs[2], Coeffs[3], Coeffs[4], Coeffs[5])
			flux_predictions.append(ypred)

		flux_predictions = np.array(flux_predictions)
		
		#Root Mean Square Error calculations
		dif = (flux_predictions - flux)/flux_errors
		temp = np.sum((flux_predictions - flux)**2)
		temp = temp / (len(flux))
		RMSE = np.sqrt(temp)
		return RMSE


	#create polynomial function given degree
	def polynomial_func(self, degree):
		Coeffs = np.polyfit(self.time, self.flux, degree)
		f = np.poly1d(Coeffs)
		return f




	# N degree polynomial fit and return RMSE
	def polynomial_fit_plot(self, degree):
		f = self.polynomial_func(degree)
		bft = np.linspace(self.time[0], self.time[-1], 500)
		plt.plot(bft, f(bft), color='black', label= self.band)
		plt.errorbar(self.time, self.flux, yerr=self.flux_err, fmt='o', color='black', markersize=2.5, label='I band fit')
		ax = plt.gca()

		
		plt.legend(ncol=2)
		plt.title('SN2011fe light curves third degree polynomial fit')
		plt.xlabel('time (days)')
		plt.ylabel('relative flux')
		plt.show()
		return self.calc_RMSE_func(self.flux, self.time, self.flux_err, self.band, f, degree=degree)
	
	


	#initialize kapernka functin paramater bounds, and priors
	kap_param_bounds = ([10*-5,10*-5,0,0,0,0], [1000,100,100,100,100,100])
	kap_prior = {
			'R' : [50, 20, 20, 50, 50, 50],
			'g' : [40,20,10,40,1,100],
			'I' : [100, 20, 20, 50, 50, 50]
		  }

	#Kapernka function
	def Kapernka_func(self, t, A, B, t_0, t_1, Tfall, Trise):
		
		first = A * (1 + (B * (t - t_1)*(t - t_1)))
		var = -(t - t_0)
		second = np.exp(var / Tfall)
		third = 1 + np.exp(var / Trise)
		return first * (second / third)

	#Plot kapernka best fit and return RMSE
	def Kapernka_fit_plot(self):

		fitCoeffs, Covars = curve_fit(self.Kapernka_func, self.time, self.flux, self.kap_prior[self.band], bounds=self.kap_param_bounds)
		bft = np.linspace(self.time[0], self.time[-1])
		bestfit_flux = self.Kapernka_func(bft, fitCoeffs[0], fitCoeffs[1], fitCoeffs[2], fitCoeffs[3], fitCoeffs[4],fitCoeffs[5])

		plt.errorbar(self.time, self.flux, yerr=self.flux_err, color='blue', label= self.band, fmt = 'o', markersize = 2.5)
		plt.plot(bft, bestfit_flux, color = 'blue', label ='best fit')
		plt.show()
		return self.calc_RMSE_func(self.flux, self.time, self.flux_err, self.band, self.Kapernka_func)









