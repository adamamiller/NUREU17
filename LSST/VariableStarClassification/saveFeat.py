def saveFeat (lc, tName, cur, conn): #pass in lightcurve table and cursor
    feats_to_use = [
                'amplitude',
                'flux_percentile_ratio_mid20', 
                'flux_percentile_ratio_mid35', 
                'flux_percentile_ratio_mid50', 
                'flux_percentile_ratio_mid65', 
                'flux_percentile_ratio_mid80', 
                'max_slope', 
                'maximum', 
                'median',
                'median_absolute_deviation', 
                'minimum',
                'percent_amplitude',
                'percent_beyond_1_std', 
                'percent_close_to_median', 
                'percent_difference_flux_percentile',
                'period_fast', 
                'qso_log_chi2_qsonu',
                'qso_log_chi2nuNULL_chi2nu',
                'skew',
                'std',
                'stetson_j',
                'stetson_k',
                'weighted_average',
                'fold2P_slope_10percentile',
                'fold2P_slope_90percentile',
                'freq1_amplitude1',
                'freq1_amplitude2',
                'freq1_amplitude3',
                'freq1_amplitude4',
                'freq1_freq',
                'freq1_lambda',
                'freq1_rel_phase2',
                'freq1_rel_phase3',
                'freq1_rel_phase4',
                'freq1_signif',
                'freq2_amplitude1',
                'freq2_amplitude2',
                'freq2_amplitude3',
                'freq2_amplitude4',
                'freq2_freq',
                'freq2_rel_phase2',
                'freq2_rel_phase3',
                'freq2_rel_phase4',
                'freq3_amplitude1',
                'freq3_amplitude2',
                'freq3_amplitude3',
                'freq3_amplitude4',
                'freq3_freq',
                'freq3_rel_phase2',
                'freq3_rel_phase3',
                'freq3_rel_phase4',
                'freq_amplitude_ratio_21',
                'freq_amplitude_ratio_31',
                'freq_frequency_ratio_21',
                'freq_frequency_ratio_31',
                'freq_model_max_delta_mags',
                'freq_model_min_delta_mags',
                'freq_model_phi1_phi2',
                'freq_n_alias',
                'freq_signif_ratio_21',
                'freq_signif_ratio_31',
                'freq_varrat',
                'freq_y_offset',
                'linear_trend',
                'medperc90_2p_p',
                'p2p_scatter_2praw',
                'p2p_scatter_over_mad',
                'p2p_scatter_pfold_over_mad',
                'p2p_ssqr_diff_over_var',
                'scatter_res_raw'
               ]
    string = "insert into " + tName + """ values (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    cur.execute("""select oid from {:}""".format(tName))
    check = cur.fetchall()

    for oid in np.unique(lc['oid']):
        if (oid not in check):
            mask = np.logical_and(lc['oid'] == oid, lc['mag_autocorr'] > 0)

            fset = featurize.featurize_time_series(lc[mask]['obsmjd'], lc[mask]['mag_autocorr'], lc[mask]['magerr_auto'],
                                            meta_features = {'oid': str(oid)}, features_to_use = feats_to_use)
 
            cur.execute(string, fset.get_values()[0])
        else:
            print('Database already contains a ', oid)
    conn.commit()