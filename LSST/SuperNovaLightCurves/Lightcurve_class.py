#Sample Lightcurve class with Kapernka model 
from scipy.optimize import curve_fit, minimize
import numpy as np
import matplotlib.pyplot as plt
import os
from JSON_to_DF import JSON_to_DataFrame
import ntpath
import json
import pandas as pd
import celerite
import pickle 



#Create Kernels for Gaussian Process

#Real term parameter initialization
a = 1e-4
c = 1
#Matern term parameter initialization
sig = 1e-2
rho = 100

#Bounds on parameters 
bounds = dict(log_a = (-15,15), log_c = (-15,15))
bounds = dict(log_sigma = (-15, 15), log_rho = (-15, 15))

#Create Kernels
Real_Kernel = celerite.terms.RealTerm(log_a = np.log(a), log_c = np.log(c), bounds=bounds)
Matern_Kernel = celerite.terms.Matern32Term(log_sigma = np.log(sig), log_rho = np.log(rho))




def deserialize(path):
	pickle_in = open(path, "rb")
	return pickle.load(pickle_in)



class Supernovae:
	#Create Kernels for Gaussian Process

	#Real term parameter initialization
	a = 1e-4
	c = 1
	#Matern term parameter initialization
	sig = 1e-2
	rho = 100

	#Bounds on parameters 
	bounds = dict(log_a = (-15,15), log_c = (-15,15))
	bounds2 = dict(log_sigma = (-15, 15), log_rho = (-15, 15))

	#Create Kernels
	Real_Kernel = celerite.terms.RealTerm(log_a = np.log(a), log_c = np.log(c), bounds=bounds)
	Matern_Kernel = celerite.terms.Matern32Term(log_sigma = np.log(sig), log_rho = np.log(rho))


	
	def __init__(self, path):
		self.name = os.path.splitext(os.path.basename(path))[0]
		self.path = path
	
	def meta_data(self):
		file_ = open(self.path)
		data = json.load(file_)
		self.references = pd.DataFrame((data[self.name]['sources']))
		if('redshift' in data[self.name]):
			self.z = pd.DataFrame(data[self.name]['redshift']).value[0]
		else:
			self.z = False
		
	def load_LightCurves(self):
			df = JSON_to_DataFrame(self.path)
			Lightcurves = {}
			if(not isinstance(df, pd.DataFrame)):
				self.Lightcurves = Lightcurves
				return
			
			band_ref = df[['band', 'source']]
			pairs = []
			for row in band_ref.iterrows():
				if(pd.isnull(row[1]['band'])):
					continue
				element = (row[1]['band'], row[1]['source'])
				if(element not in pairs):
					pairs.append(element)
			
			for x in pairs:
				data = df[df.band == x[0]]
				data = data[data.source == x[1]]
				label = str(x[0]) + '_' + str(x[1])
				keys = np.array(x[1].split(','), dtype=int)
				for i in range(len(keys)):
					keys[i] = int(keys[i])
				
				if('e_magnitude' not in data):
					continue
				#rid data of points with nan values
				data = data[np.invert(np.isnan(data.e_magnitude.values))]
				data = data[np.invert(np.isnan(data.time.values))]
				data = data[np.invert(np.isnan(data.magnitude.values))]
				data = data[data.e_magnitude.values != 0]
				
				
				if(len(data.time.values) == 0):
					continue
				n_good_obs = len(data.time.values)
				Lightcurves[label] = filter_lightcurve(data.time.values, data.magnitude.values, data.e_magnitude.values, str(x[0]), keys, self.path, n_good_obs=n_good_obs)
			
			
			self.Lightcurves = Lightcurves


	def load_fit_data(self):
		for key in self.Lightcurves.keys():
			#Ensure there are a sufficient amount of data points to run fits
			if(self.Lightcurves[key].n_good_obs <= 6):
				continue
			print(self.name, key)
			#Run fits
			self.Lightcurves[key].polynomial_fit_plot(4, plot=False)
			self.Lightcurves[key].polynomial_fit_plot(6, plot=False)
			self.Lightcurves[key].polynomial_fit_plot(8, plot=False)
			self.Lightcurves[key].Kapernka_fit_plot(plot=False)
			self.Lightcurves[key].Bazin_fit_plot(plot=False)
			
			self.Lightcurves[key].Gaussian_process(Real_Kernel, plot=False)
			self.Lightcurves[key].Gaussian_process(Matern_Kernel, plot=False)
			print(self.Lightcurves[key].Rchi2, self.Lightcurves[key].medians)



	def serialize(self):
		pickle_out = open("../../../OSC_data/pickled_data/" + str(self.name) + ".pickle", "wb")
		pickle.dump(self, pickle_out)
		pickle_out.close()



		


					
class filter_lightcurve(Supernovae):
	#Lightcurve object constructor
	
	def __init__(self, time, mag , mag_err, band, keys, path, is_mag=True, n_good_obs=0):
		#store time and band
		super().__init__(path)
		super().meta_data()
		self.Rchi2 = {}

		self.medians = {}
		self.keys = keys
		self.time = time
		self.band = band
		self.n_good_obs = n_good_obs
		
		#If data is passed as magnitudes, convert to flux
		if(is_mag):
			max_flux = np.max(self.mag_to_flux(mag))
			#Normalize by maximum flux
			self.flux = self.mag_to_flux(mag) / max_flux 
			
			self.flux_err = self.mag_err_to_flux_err(mag_err, self.flux)
		else:
			max_flux = np.max(mag)
			self.flux = mag / max_flux
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
	def calc_Rchi2_poly(self, degree):
		flux_predictions = np.empty(self.flux.shape) 
		#loop to run 'leave one out' CV
		for ind, c in enumerate(self.flux):
			flux_del = np.delete(self.flux, ind)
			time_del = np.delete(self.time, ind)
			flux_err_del = np.delete(self.flux_err, ind)
			Coeffs = np.polyfit(time_del, flux_del, degree, w=flux_err_del)
			f = np.poly1d(Coeffs)
			ypred = f(self.time[ind])
			flux_predictions[ind] = ypred
		
		#Root Mean Square Error calculations
		dif = (flux_predictions - self.flux)/self.flux_err
		
		temp = np.sum(dif**2)
		temp = temp / (len(self.flux))
		Rchi2 = np.sqrt(temp)
		self.Rchi2['polynomial_' + str(degree)] = Rchi2
		
		#median calculations
		median = np.median(abs(dif))
		self.medians['poly_' + str(degree)] = median
		return Rchi2

	

	def calc_Rchi2_func(self, fit, name):
		flux_predictions = np.empty(self.flux.shape) 
		#loop to run 'leave one out' CV
		for ind, f in enumerate(self.flux):
			flux_del = np.delete(self.flux, ind)
			time_del = np.delete(self.time, ind)
			flux_err_del = np.delete(self.flux_err, ind)
			Coeffs, Covar = curve_fit(fit, time_del, flux_del, sigma=flux_err_del, bounds = self.kap_param_bounds, maxfev=1000000)
			
			ypred = fit(self.time[ind], Coeffs[0], Coeffs[1], Coeffs[2], Coeffs[3], Coeffs[4], Coeffs[5])
			flux_predictions[ind] = ypred
		
		#Root Mean Square Error calculations

		dif = (flux_predictions - self.flux)/self.flux_err
		
		
		temp = np.sum(dif**2)
		temp = temp / (len(self.flux))
		Rchi2 = np.sqrt(temp)
		self.Rchi2[name] = Rchi2


		#median calculations
		median = np.median(abs(dif))
		self.medians[name] = median

		return Rchi2

	def calc_Rchi2_GP(self, gp):
		flux_predictions = np.empty(self.flux.shape)
		#loop to run 'leave one out' CV
		if(type(gp.kernel) == celerite.terms.RealTerm):
			name = 'Real'
		elif(type(gp.kernel) == celerite.terms.Matern32Term):
			name = 'Matern'
		print(name)
		for ind, f in enumerate(self.flux):
			flux_del = np.delete(self.flux, ind)
			time_del = np.delete(self.time, ind)
			flux_err_del = np.delete(self.flux_err, ind)
			gp.compute(time_del, flux_err_del)
			initial_params = gp.get_parameter_vector()
			bounds = gp.get_parameter_bounds()
			r = minimize(self.neg_log_like, initial_params, method="L-BFGS-B", bounds=bounds, args=((flux_del, gp)))
			gp.set_parameter_vector(r.x)
			ypred, pred_var = gp.predict(flux_del, self.time[ind], return_var=True)
			flux_predictions[ind] = ypred
		print(flux_predictions)
		#Root Mean Square Error calculations
		dif = (flux_predictions - self.flux)/self.flux_err
		median = np.median(abs(dif))
		temp = np.sum(dif**2)
		temp = temp / (len(self.flux))
		Rchi2 = np.sqrt(temp)
		
		self.Rchi2['GP' + '_' + name] = Rchi2
	
		#median calculations
		median = np.median(abs(dif))
		self.medians['GP' + '_' + name] = median
		
		

			
			

	#create polynomial fit function given degree
	def polynomial_func(self, degree):
		Coeffs = np.polyfit(self.time, self.flux, degree, w=self.flux_err)
		f = np.poly1d(Coeffs)
		return f

	# N degree polynomial fit and return RMSE
	def polynomial_fit_plot(self, degree, plot=False):
		f = self.polynomial_func(degree)
		if(plot):
			bft = np.linspace(self.time[0], self.time[-1], 500)
			plt.plot(bft, f(bft), color='black', label= self.band)
			plt.errorbar(self.time, self.flux, yerr=self.flux_err, fmt='o', color='black', markersize=2.5, label='I band fit')
			ax = plt.gca()
			plt.legend(ncol=2)
			
			plt.xlim(0 - self.time[2], np.max(self.time) + 10)
			plt.title(str(self.name) + ' ' + str(self.band) + ' band ' + str(degree) + ' degree ' + 'polynomial fit')
			plt.xlabel('time (days)')
			plt.ylabel('relative flux')
			plt.show()
		
		return self.calc_Rchi2_poly(degree)
	
	#initialize kapernka functin paramater bounds, and priors
	kap_param_bounds = ([10*-5,10*-5,0,0,0,0], [1000,100,100,100,100,100])
	kap_prior = [50, 20, 20, 50, 50, 50]
			

	#Kapernka model
	def Kapernka_func(self, t, A, B, t_0, t_1, Tfall, Trise):
		
		first = A * (1 + (B * (t - t_1)*(t - t_1)))
		var = -(t - t_0)
		second = np.exp(var / Tfall)
		third = 1 + np.exp(var / Trise)
		return first * (second / third)

	#Plot kapernka best fit and return Rchi2
	def Kapernka_fit_plot(self, plot=False):
		name = 'Kapernka'
		if(plot):
			fitCoeffs, Covars = curve_fit(self.Kapernka_func, self.time, self.flux,  sigma=self.flux_err, maxfev=1000000)
			bft = np.linspace(self.time[0], self.time[-1])
			bestfit_flux = self.Kapernka_func(bft, fitCoeffs[0], fitCoeffs[1], fitCoeffs[2], fitCoeffs[3], fitCoeffs[4],fitCoeffs[5])
	
			plt.errorbar(self.time, self.flux, yerr=self.flux_err, color='blue', label= self.band, fmt = 'o', markersize = 2.5)
			plt.plot(bft, bestfit_flux, color = 'blue', label ='best fit')
			plt.xlabel('time (days)')
			plt.ylabel('relative flux')
			plt.legend()
			plt.xlim(0 - self.time[2], np.max(self.time) + 10)
			plt.title(str(self.name) + " " + str( self.band) + ' band Kapernka fit')
			plt.show()
		return self.calc_Rchi2_func(self.Kapernka_func, name)

	#Bazin model
	def Bazin_func(self, t, A, t_0, Trise, Tfall, a1, a2):
		first = A * (1 + (a1 * (t - t_0)) + (a2 * (t - t_0)))
		var = - (t - t_0)
		second = np.exp(var / Tfall)
		third =  1 + np.exp(var / Trise)  
		return first * (second / third)

	#Plot Bazin best fit and return Rchi2
	def Bazin_fit_plot(self, plot=False):
		name = 'Bazin'
		if(plot): 
			fitCoeffs, Covars = curve_fit(self.Bazin_func, self.time, self.flux, sigma=self.flux_err,  bounds=self.kap_param_bounds, maxfev=1000000)
			bft = np.linspace(self.time[0], self.time[-1])
			bestfit_flux = self.Bazin_func(bft, fitCoeffs[0], fitCoeffs[1], fitCoeffs[2], fitCoeffs[3], fitCoeffs[4],fitCoeffs[5])
			max_flux = np.max(bestfit_flux)
			bestfit_flux = bestfit_flux/max_flux
			plt.errorbar(self.time, self.flux, yerr=self.flux_err, color='blue', label= self.band, fmt = 'o', markersize = 2.5)
			
			plt.xlim(0 - self.time[2], np.max(self.time))
			plt.plot(bft, bestfit_flux, color = 'blue', label ='best fit')

			plt.show()
		return self.calc_Rchi2_func(self.Bazin_func, name)

	def neg_log_like(self, params, flux, gp):
			gp.set_parameter_vector(params)
			return -gp.log_likelihood(flux)

	


	def Gaussian_process(self, kernel, plot=False):
		mean = np.mean(self.flux)
		
		gp = celerite.GP(kernel, mean=mean)
		
		gp.compute(self.time, self.flux_err)

		initial_params = gp.get_parameter_vector()
		bounds = gp.get_parameter_bounds()
		r = minimize(self.neg_log_like, initial_params, method="L-BFGS-B", bounds=bounds, args=(self.flux, gp))
		gp.set_parameter_vector(r.x)
		#pred_mean, pred_var = gp.predict(self.flux, self.time, return_var=True)


		if(plot):
			x = np.linspace(self.time[0], self.time[-1], 1000)
			pred_mean, pred_var = gp.predict(self.flux, x, return_var=True)
			pred_std = np.sqrt(pred_var)
			color = "#ff7f0e"
			
			plt.plot(x, pred_mean, label='GP model')
			plt.errorbar(self.time, self.flux, fmt='o', yerr=self.flux_err, label= self.band + ' band', markersize= 2.5)
			plt.fill_between(x, pred_mean+pred_std, pred_mean-pred_std, color=color, alpha=0.3,
							 edgecolor="none")
			plt.legend()
			plt.title('')
			plt.xlabel('time (days)')
			plt.ylabel('relative flux')
			
			plt.ylim(min(pred_mean), max(pred_mean))

			plt.xlim(0 - self.time[2], np.max(self.time) + 10)
			plt.title(self.name + ' ' + self.band + ' data')
			plt.show()
		return self.calc_Rchi2_GP(gp)

	
		
		











