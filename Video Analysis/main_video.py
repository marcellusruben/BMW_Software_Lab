# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 12:26:20 2017

@author: Marcellus Ruben Winastwan
"""

import os
import numpy as np

from ReadVideo import read_video
from identify_transitions import identify_transition
from ReadFrames import read_frame

'''
Before run the program, create a folder named 'IIHSO_TA' in the same directory as the other python files
'''
# CREATE THE PATH OF THE WORKING DIRECTORY -----------------------------------------------------------------------

addpath = os.path.dirname(os.path.abspath(__file__))

# READ THE VIDEO FILES WITH MP4 EXTENSION ------------------------------------------------------------------------
'''
Read the desired video inside the IIHSO_TA folder (in this case the format is .avi)
'''
video_analysis_flag = True
if video_analysis_flag == True:
    folder = os.getcwd()

    x                   = '*.mp4'
    sub_directory       = "IIHSO_TA\\"
    input_videos_folder = "\\".join((folder,sub_directory))
  
    
    for file in os.listdir(input_videos_folder):
        if file.endswith('avi'):
            video_files = os.path.join(input_videos_folder,file)

# GET THE BASE NAME OF VIDEO WITH AND WITHOUT EXTENSION ---------------------------------------------------------

    fin = os.path.basename(video_files)
    
    name = os.path.splitext(fin)[0]

# EXTRACT EVERY FRAME OF THE VIDEO AND DETERMINE THE MEAN GREY LEVELS IN EVERY FRAME ---------------------------------------------------------------------
    '''
    Then, we process the video and extract it into the frame image in read_video class
    '''
    my_frame = read_video(fin,input_videos_folder)
    my_frame.videoreader() 
    
# DETECT IF THE VIDEO CONTAINS TOP VIEW ----------------------------------------------------------------------
    
    '''
    After that, detect whether the video contains a transition or not with identify_transition class. If the video
    contains transition, then get the nmber of frame where the top view scene begin and ends. If not, simply print
    No transitions found
    '''
    
    if my_frame.getNoOfFrames()>1000:

#        if ReadVideo.getNoOfFrames() > 1000:
        transition = identify_transition(my_frame.getMeanGrayLevels(),my_frame.getNoOfFrames())
        transition.transition_identifier()
        trans = transition.getTransitions()
        print('Top view detected at frames = ', trans[:,0],'until',trans[:,1])    
    
    else:
        
        trans = np.zeros((1,2))
        print('No transition found')
# ----------------------------------------------------------------------------------------------------------------    
    '''
    Finally, process the image, get the desirable ROI, and observe the displacement of the sensor seen in the video
    using read_frames class
    '''
    my_frames = read_frame(fin,input_videos_folder,trans)
    my_frames.reading_frame()

           