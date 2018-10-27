#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 11:29:57 2018

@author: virati
File for patient specific readout
"""


#DBSpace libraries and sublibraries here
from DBSpace.readout import BR_DataFrame as BRDF
from DBSpace.readout import ClinVect, DSV

# General python libraries
import scipy.signal as sig
import numpy as np

# Plotting Libraries
import matplotlib.pyplot as plt
import seaborn as sns
#Do some cleanup of the plotting space
plt.close('all')
sns.set_context('paper')
sns.set(font_scale=5)

#%%

test_scale = 'HDRS17'
do_detrend = 'None'

#%%
# Now we set up our DBSpace environment
ClinFrame = ClinVect.CFrame(norm_scales=True)
BRFrame = BRDF.BR_Data_Tree()

# Run our main sequence for populating the BRFrame
BRFrame.full_sequence(data_path='/home/virati/Chronic_Frame_july.npy')
BRFrame.check_empty_phases() # Check to see if there are any empty phases. This should be folded into full_sequence soon TODO


#%%
# This sets up the regression
analysis = DSV.ORegress(BRFrame,ClinFrame)
analysis.split_validation_set(do_split = True) #Split our entire dataset into a validation and training set
analysis.O_feat_extract() #Do a feature extraction of our entire datset


#%%

pt = '901'
model = 'RIDGE'
for pt in ['901','903','905','906','907','908']:
    print('Patient ' + pt + ' specific model')

    
    analysis.O_regress(method=model,doplot=False,avgweeks=True,ignore_flags=False,circ='day',scale=test_scale,lindetrend=do_detrend,train_pts=pt,pt_specific=True)
    coeff_runs = analysis.O_models(plot=False,models=[model])
    summ_stats_runs = analysis.Clinical_Summary(model,plot_indiv=False,ranson=True,doplot=False)
    
    analysis.plot_model_coeffs(model=model,pt=pt)
    # need to now work with the output model but in a reasonable way
    #want to plot the coefficients learned