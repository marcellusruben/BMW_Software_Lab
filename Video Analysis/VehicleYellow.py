# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 15:12:57 2017

@author: Marcellus Ruben Winastwan
"""

import numpy as np


class getVehicleYellow(object):
    
    def __init__(self,frame_file,rec_barrier,treshold_yellow):
        self.frame_file = frame_file
        self.rec_barrier = rec_barrier
        self.treshold_yellow = treshold_yellow
        
    def VehicleYellow(self):

        '''
        First, we need to observe whether the video contains a barrier or not. If there is no barrier found, then simply
        copy the frame file. If there is a barrier, then copy the frame file, but with a little modification with turning
        the barrier region into completely black, so that the algorithm wouldn't detect undesirable region in the image
        '''
##DETECT IF THE BARRIER IS FOUND OR NOT----------------------------------------------------------------------------------------------------------------------------------------------
        
        if self.rec_barrier== [0,0,0,0]:
            
            self.frame_file_without_barrier = self.frame_file.copy()
            
        else:
            self.frame_file_without_barrier = self.frame_file.copy()
            self.frame_file_without_barrier[self.rec_barrier[1]-10:self.rec_barrier[3]+10,self.rec_barrier[0]-810:self.rec_barrier[2]+10,:]=0

        '''
        Then, mask the image into black and white image, with the region of interest having a white color, and the rest is black
        '''       
## MASK THE FRAME BASED ON ALREADY DEFINED THRESHOLD IN READFRAMES CLASS --------------------------------------------------------------------------------------------------------------

        self.mask_b_yellow         = np.logical_and(self.frame_file_without_barrier[:,:,0] > self.treshold_yellow[0][0],self.frame_file_without_barrier[:,:,0] < self.treshold_yellow[0][1])
        self.mask_g_yellow         = np.logical_and(self.frame_file_without_barrier[:,:,1] > self.treshold_yellow[1][0], self.frame_file_without_barrier[:,:,1] < self.treshold_yellow[1][1])
        self.mask_r_yellow         = np.logical_and(self.frame_file_without_barrier[:,:,2] > self.treshold_yellow[2][0], self.frame_file_without_barrier[:,:,2] < self.treshold_yellow[2][1])
        self.mask_bg_yellow        = np.multiply(self.mask_b_yellow,self.mask_g_yellow)
        self.mask_overall_yellow   = np.multiply(self.mask_r_yellow,self.mask_bg_yellow)

        '''
        Then, we minimize the frame by cropping the matrix so that the matrix only contains the region of interest.
        '''
##MINIMIZE THE MATRIX INTO ONLY THE MATRIX IN THE REGION OF INTEREST --------------------------------------------------------------------------------------------------------------------

        self.nonzero_mask_yellow = np.argwhere(self.mask_overall_yellow)
        (self.y_start_yellow,self.x_start_yellow),(self.y_stop_yellow,self.x_stop_yellow) = self.nonzero_mask_yellow.min(0),self.nonzero_mask_yellow.max(0)+1

        '''
        After the cropping, the coordinate of the top left corner and bottom right corner of the bounding box can be determined
        '''
##DETERMINE THE COORDINATE OF THE RECTANGLE OF YELLOW TARGET -----------------------------------------------------------------------------------------------

        if self.rec_barrier== [0,0,0,0]:
            self.y_start_yellow         = self.y_start_yellow
            self.rec_yellow_vehicle     = self.mask_overall_yellow[self.y_start_yellow:self.y_stop_yellow,self.x_start_yellow:self.x_stop_yellow]
            
        else:
            self.y_start_yellow = self.y_start_yellow-10
            self.rec_yellow_vehicle     = self.mask_overall_yellow[self.y_start_yellow:self.y_stop_yellow,self.x_start_yellow:self.x_stop_yellow]
        '''
        Save the coordinate of the bounding box
        '''
##SAVE THE COORDINATE OF THE RECTANGLE ------------------------------------------------------------------------------------------------------------------------        
        self.coord_vehicle_yellow = [self.x_start_yellow,self.y_start_yellow,self.x_stop_yellow,self.y_stop_yellow]
    
        '''
        Generate a black and white image to identify the pattern of the region of interest and the center circle of the target (in this case the 
        yellow color will have a white color)
        '''
##CREATE THE CONTRAST IN THE FRAME IN ORDER TO IDENTIFY THE CENTER CIRCLE OF THE TARGET -----------------------------------------------------------------------
        self.pattern_rows       = abs(np.gradient(self.rec_yellow_vehicle*1,axis=0))
        self.pattern_columns    = abs(np.gradient(self.rec_yellow_vehicle*1,axis=1))

        self.pattern_overall = np.logical_or(self.pattern_columns,self.pattern_rows)


    def getCoordVehYellow(self):
        return self.coord_vehicle_yellow
        
    def getPattern(self):
        return self.pattern_overall
        
