# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 19:05:14 2017

@author: ASUS
"""

import numpy as np


class getBarrierInfo(object):
    
    def __init__(self,frame_file,treshold):
        self.frame_file = frame_file
        self.treshold = treshold
        
    def BarrierInfo(self):

        '''
        First, create a masked image using the threshold defined in read_frame class to identify the region of interest
        (the barrier)
        '''        
##CREATE A MASK BASED ON THE ALREADY DEFINED THRESHOLD ---------------------------------------------------------------------------------

        self.mask_b         = np.logical_and(self.frame_file[:,:,0] > self.treshold[0][0],self.frame_file[:,:,0] < self.treshold[0][1])
        self.mask_g         = np.logical_and(self.frame_file[:,:,1] > self.treshold[1][0], self.frame_file[:,:,1] < self.treshold[1][1])
        self.mask_r         = np.logical_and(self.frame_file[:,:,2] > self.treshold[2][0], self.frame_file[:,:,2] < self.treshold[2][1])
        self.mask_bg        = np.multiply(self.mask_b,self.mask_g)
        self.mask_overall   = np.multiply(self.mask_r,self.mask_bg)
   
        
##CREATE THE BOUNDING RECTANGLE OF THE BARRIER ---------------------------------------------------------------------------------------

        self.nonzero_mask   = np.argwhere(self.mask_overall)
        
        '''
        If self.nonzero mask is empty (which means there is no barrier found in the video), then simply print No
        barrier found with the bounding box coordinate = [0,0,0]
        
        If self.nonzero mask is not empty, then crop the matrix into the matrix only containing the region of interest
        '''

##DEFINE THE COORDINATE OF THE RECTANGLE OF THE BARRIER ------------------------------------------------------------------------------     
   
        if self.nonzero_mask.shape < (5,5):
            print('No Barrier Found')
            self.coord_barrier = [0,0,0,0]

        else:
            (self.y_start,self.x_start),(self.y_stop,self.x_stop) = self.nonzero_mask.min(0),self.nonzero_mask.max(0)+1

##SAVE THE COORDINATE OF THE RECTANGLE OF THE BARRIER ------------------------------------------------------------------------------------

            '''
            Save the the coordinate of the bounding box of the barrier
            '''
            self.coord_barrier = [self.x_start,self.y_start,self.x_stop,self.y_stop]
            print(self.coord_barrier)
    
    def getCoordBarrier(self):
        return self.coord_barrier
