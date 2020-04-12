# -*- coding: utf-8 -*-
"""
Created on Tue May 30 21:32:47 2017

@author: Marcellus Ruben Winastwan
"""

import numpy as np
from math import cos, sin


class genRotMatrixDC(object):
    
    def __init__ (self, anglesRad, pVector):
        self.anglesRad = anglesRad
        self.pVector = pVector
        
    
    def RotationMatrixDC(self):
        
        self.RotMatrix = np.zeros((3,3))
        self.c = cos(self.anglesRad)
        self.s = sin(self.anglesRad)
        
        self.RotMatrix[0,0]= 1.0
        self.RotMatrix[1,1]= 1.0
        self.RotMatrix[2,2]= 1.0

        if abs(self.anglesRad-3.14159265359)<1e-7:
            self.RotMatrix[0,0]= -1.0
            self.RotMatrix[1,1]= 1.0
            self.RotMatrix[2,2]= -1.0

        elif abs(self.anglesRad)>0.0:
            self.ux =(-self.pVector[0]/np.linalg.norm(self.pVector))
            self.uy =(-self.pVector[1]/np.linalg.norm(self.pVector))
            self.uz =(-self.pVector[2]/np.linalg.norm(self.pVector))
        
            self.RotMatrix[0,0]= self.c+(self.ux**2.0)*(1.0-self.c)
            self.RotMatrix[0,1]= self.ux*self.uy*(1.0-self.c)-self.uz*self.s
            self.RotMatrix[0,2]= self.ux*self.uz*(1.0-self.c)+self.uy*self.s

            self.RotMatrix[1,0]= self.uy*self.ux*(1.0-self.c)+self.uz*self.s
            self.RotMatrix[1,1]= self.c+(self.uy**2.0)*(1.0-self.c)
            self.RotMatrix[1,2]= self.uy*self.uz*(1.0-self.c)-self.ux*self.s

            self.RotMatrix[2,0]= self.uz*self.ux*(1.0-self.c)-self.uy*self.s
            self.RotMatrix[2,1]= self.uz*self.uy*(1.0-self.c)+self.ux*self.s
            self.RotMatrix[2,2]= self.c+(self.uz**2.0)*(1.0-self.c)
        
        for i in range (0,3):
            for j in range (0,3):
                if abs(self.RotMatrix[i,j])<0.00001:
                    self.RotMatrix[i,j] = 0.0

        return self.RotMatrix