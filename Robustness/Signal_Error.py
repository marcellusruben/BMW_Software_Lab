# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 22:28:46 2017

@author: Marcellus Ruben Winastwan
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

class signal_error(object):
    
    def __init__(self,time_vector,local_samples,samples_error,max_error, name):
        self.time_vector = time_vector
        self.local_samples = local_samples
        self.samples_error = samples_error
        self.max_error = max_error
        self.name = name
        
    def compute_signal_error(self):
        '''
        First, we need to substract the shape of the original acceleration or rotational velocity
        '''
        self.s_size = self.local_samples.shape[0]
        self.comp = self.local_samples.shape[1]

        '''
        Then, initialize the new signal matrix based on the desired samples error and the shape of the original acceleration
        or rotational velocity
        '''
        self.new_signal = np.zeros ((self.samples_error,self.s_size,self.comp))
        self.new_signal[0,:,:] = self.local_samples[:,:]

        '''
        Create a loop to generate the new signal after inducing the error
        '''
        
        for i in range (0,self.comp):
            for j in range (1,self.samples_error):
                for k in range (0,self.s_size):
                    self.new_signal[j,k,i] = self.local_samples[k,i]+self.local_samples[k,i]*self.max_error*np.random.uniform(0,1)*np.random.random_integers(-1,1)

        return self.new_signal
        
    def getnewsignal(self):
        return self.new_signal

    def solver(self):
        self.compute_signal_error()
        self.getnewsignal()
      