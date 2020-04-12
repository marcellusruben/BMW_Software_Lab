# -*- coding: utf-8 -*-
"""
Created on Tue May 30 21:30:51 2017

@author: Marcellus Ruben Winastwan
"""

import numpy as np

class genRotMatrixAA(object):
    
    def __init__(self, cxx, cyx, czx, cxy, cyy, czy, cxz, cyz, czz):
        self.cxx = cxx
        self.cyx = cyx
        self.czx = czx
        self.cxy = cxy
        self.cyy = cyy
        self.czy = czy
        self.cxz = cxz
        self.cyz = cyz
        self.czz = czz
        
    def RotationMatrixAA(self):
        
        '''
        Initialize directional cosines matrix
        '''
        self.T = np.zeros((3,3))
        self.co = 0
        self.ro = 0
        
        '''
        Fill the directional cosines matrix
        '''
        
        self.T[self.ro, self.co]=self.cxx
        self.T[self.ro, self.co+1]=self.cyx
        self.T[self.ro, self.co+2]=self.czx
        self.T[self.ro+1, self.co]=self.cxy
        self.T[self.ro+1, self.co+1]=self.cyy
        self.T[self.ro+1, self.co+2]=self.czy
        self.T[self.ro+2, self.co]=self.cxz
        self.T[self.ro+2, self.co+1]=self.cyz
        self.T[self.ro+2, self.co+2]=self.czz

        for i in range (3):
            for j in range (3):
                if abs(self.T[i,j]) < 0.00001:
                    self.T[i,j] = 0.0
        return self.T

    def solverMatrixAA(self):
        
        self.RotationMatrixAA()