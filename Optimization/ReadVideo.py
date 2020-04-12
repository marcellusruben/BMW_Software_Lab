# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 14:39:43 2017

@author: Marcellus Ruben Winastwan
"""
import os
import cv2
import numpy as np

class read_video(object):
    
    def __init__(self,fin,input_videos_folder):
        self.fin = fin
        self.input_videos_folder = input_videos_folder
    
    def videoreader(self):
        
        '''
        First, we need to determine the video that we need to read by searching the working directory where
        the video belongs
        '''
        
        # GET THE PATH WHERE THE VIDEO BELONGS ------------------------------------------------------------------
        
        self.MovieFullName = os.path.join(self.input_videos_folder,self.fin)
        print(self.MovieFullName)
        
        '''
        After that, we can get the information about the property of the video that we need, such as the
        number of frames, the width, and the height of the video
        '''
        
        # DETERMINE THE NUMBER OF FRAME OF THE VIDEO -----------------------------------------------------------
        
        self.VideoObject    = cv2.VideoCapture(self.MovieFullName)
        self.numberOfFrames = int(self.VideoObject.get(cv2.CAP_PROP_FRAME_COUNT))
        self.vidHeight      = int(self.VideoObject.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.vidWidth       = int(self.VideoObject.get(cv2.CAP_PROP_FRAME_WIDTH))
        
        '''
        Then, we initialize the mean gray levels vector. These vectors are useful to find out which frame 
        of the video has the highest mean gray levels
        '''
        # INITIALIZE THE MEAN GRAY AND RGB LEVELS --------------------------------------------------------------
        
        self.meanGrayLevels     = np.zeros((self.numberOfFrames,1))
        self.meanRedLevels      = np.zeros((self.numberOfFrames,1))
        self.meanGreenLevels    = np.zeros((self.numberOfFrames,1))
        self.meanBlueLevels     = np.zeros((self.numberOfFrames,1))
        #print(self.meanGrayLevels)
        
        self.NumberofFramesWritten = 0
        
        '''
        After that, read every frame of the video
        '''
        
        # READ EVERY FRAME OF THE VIDEO ------------------------------------------------------------------------
        
        success, self.thisFrame = self.VideoObject.read()
        success = True
        self.frame_counter = 0
        while (success):
            
            success, self.thisFrame = self.VideoObject.read()

            if success: 
                '''
                In every frame, we need to convert the original image in RGB into grayscale image so that
                the frame which has the average gray levels can be identified
                
                This average gray level in each frame is very important to detect whether the video contains
                a transition or not and also to identify the top view scene of video if a has transitions
                '''
#           # CALCULATE MEAN GRAY LEVELS -----------------------------------------------------------------------
#               
                self.grayImage = cv2.cvtColor(self.thisFrame,cv2.COLOR_BGR2GRAY)
                self.meanGrayLevels[self.frame_counter,:] = np.mean(self.grayImage[:])

                '''
                Aside from the gray levels, we also could calculate the average red, blue, and green
                color, although for this project, this feature will not be used
                '''
                
#           #  CALCULATE RGB LEVELS ----------------------------------------------------------------------------
#                
                self.meanRedLevels[self.frame_counter,:]    = np.mean(np.mean(self.thisFrame[:,:,0]))
                self.meanGreenLevels[self.frame_counter,:]  = np.mean(np.mean(self.thisFrame[:,:,1]))
                self.meanBlueLevels[self.frame_counter,:]   = np.mean(np.mean(self.thisFrame[:,:,2]))
                

            self.frame_counter +=1
            
            '''
            Then, we create a so called a getter function so that we can use the data from this class
            (in this case the number of frames and the mean gray levels vector) into another class
            (identify_transitions class)
            '''
        
    def getNoOfFrames(self):
        return self.numberOfFrames
        
    def getMeanGrayLevels(self):
        return self.meanGrayLevels
    
    def solver(self):
        self.videoreader()
        self.getNoOfFrames()
        self.getMeanGrayLevels()
        