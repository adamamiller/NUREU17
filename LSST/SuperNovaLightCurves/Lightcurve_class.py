from scipy.optimize import curve_fit
#Sample Lightcurve class with Kapernka model 
class Lightcurve:

	kap_param_bounds = ([10*-5,10*-5,0,0,0,0], [1000,100,100,100,100,100])
	kap_prior = []

	def __init__(self, time, mag , mag_err, band):
		self.time = time
		self.flux = mag_to_flux(mag)
		self.flux_err = mag_err_to_flux_err(mag, mag_err, flux)
		self.band = band

	def mag_to_flux(mag):
    	return 10**(-2*mag / 5) 

    def mag_err_to_flux_err(mag, mag_err, flux):
        
        mag_max = mag + err
        flux_max = mag_to_flux(mag_max)
        flux_error = flux_max - flux
        return flux_error
	

	kap_param_bounds = ([10*-5,10*-5,0,0,0,0], [1000,100,100,100,100,100])
	kap_prior = 

	def Kapernka_func(t, A, B, t_0, t_1, Tfall, Trise):
		first = A * (1 + (B * (t - t_1)*(t - t_1)))
		var = -(t - t_0)
		second = np.exp(var / Tfall)
		third = 1 + np.exp(var / Trise)
		return first * (second / third)

	def Kapernka_model(self):
		fitCoeffs, Covars = curve_fit(Kapernka_func, self.time, self.flux, prior, kap_prior, kap_param_bounds)
		self.kap_coeffs = fitCoeffs
		self.kap_Covars = Covars

