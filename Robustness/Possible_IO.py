# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 20:15:06 2017

@author: Marcellus Ruben Winastwan
"""

import numpy as np
import math as mt
from Rot_Matrix_DC import genRotMatrixDC

class genPossibleIO(object):
    
    def __init__(self, e_tol, s_tol, initial_orientation):
        self.e_tol = e_tol
        self.s_tol = s_tol
        self.initial_orientation = initial_orientation
        
    def PossibleIO(self):
        
        '''
        First, we define the rotation vector
        '''
        
        self.VG = np.array([[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0],[1.0,1.0,1.0],[-1.0,-1.0,1.0],[1.0,-1.0,0.0]])
        
        '''
        Then, transform the tolerance into radiant
        '''
        
        self.rad_e_tol = self.e_tol*mt.pi/180.0
        
        '''
        Create a linear distribution based on the tolerance with the number of distribution = self.s_tol defined in main file
        '''
        self.r = np.linspace(self.rad_e_tol*-1,self.rad_e_tol,self.s_tol)
        
        self.vsets = self.VG.shape[0] 

        '''
        Initialize the possible initial orientation matrix
        '''
        self.PIO = np.zeros((self.vsets*self.s_tol,6)) 
        self.l = 0
        
        '''
        Create the Possible initial orientation over the loop
        '''
        for i in range (0,self.vsets):
            for j in range (0,self.s_tol):
                
                '''
                Here we are rotating the angle using rotation vectors defined with self.VG and self.r in order to get the
                new possible initial orientation
                '''
                self.RM = genRotMatrixDC(self.r[j],self.VG[i,:])
                
                '''
                Get the new possible initial orientation
                '''
                self.PIO[self.l,0:3] = np.matrix.transpose(np.dot(self.RM.RotationMatrixDC(),np.matrix.transpose(self.initial_orientation[0,:])))
                self.PIO[self.l,3:6] = np.matrix.transpose(np.dot(self.RM.RotationMatrixDC(),np.matrix.transpose(self.initial_orientation[1,:])))
                self.l = self.l+1
                
        return self.PIO
    
    def getPIO(self):
        return self.PIO
        
    def maxvalue(self):
        self.max_v = np.amax(self.PIO)
        
    def minvalue(self):
        self.min_v = np.amin(self.PIO)
    
    def solver(self):
        self.PossibleIO()
        self.maxvalue()
        self.minvalue()
        self.getPIO()
                
                