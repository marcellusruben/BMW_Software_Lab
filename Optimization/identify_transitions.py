# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 22:01:01 2017

@author: Marcellus Ruben Winastwan
"""
import numpy as np

class identify_transition(object):
    
    def __init__(self,meanGrayLevels,noOfFrames):
        self.meanGrayLevels = meanGrayLevels
        self.noOfFrames     = noOfFrames
    
    def transition_identifier(self):
        
        '''
        In this class, the first step is to collect the mean gray levels data that we already get from 
        ReadVideo class.
        
        Then, we create the vectors so called diff_meangray in order to calculate the difference or the
        gradient between mean gray levels in each frame with the previous frame. This vector is important
        since the transition from any other view to top view scene of crash test video commonly has the 
        highest difference in mean gray levels compared to other transitions.
        '''
        
        # SET THE MEAN GRAY DIFFERENCE TO IDENTIFY FRAME TRANSITIONS----------------------------------------------------------------
        
        self.new_meanGrayLevels = self.meanGrayLevels.reshape(self.noOfFrames,)
        self.diff_meangray      = np.zeros((self.noOfFrames,))
        
        self.diff_meangray[1:]  = np.diff(self.new_meanGrayLevels[0:])
        self.diff_meangray[0]   = 0.0
        
        '''
        Then, we initialize the vector and array that we will need to detect the transition to top view 
        scene in the video.
        
        The size of the arrays will be equal to 20 (self.n -> we can change it randomly) x the size of mean 
        gray levels vector (self.s).
        '''

# INITIALIZE TRANSITIONS ARRAY -------------------------------------------------------------------------
        
        self.s              = self.meanGrayLevels.shape[1]

        self.n              = 20
        
        self.transitions    = np.zeros((self.n,self.s))
        self.values         = np.zeros((self.n,self.s))
        self.transitions_r  = np.zeros((self.n,self.s))
        self.values_r       = np.zeros((self.n,self.s))

        self.t_r            = np.zeros((self.s,2))
        self.v_r            = np.zeros((self.s,2))

        '''
        As mentioned above, we already calculate the difference or the gradient of mean gray levels between
        one frame to the previous frame. However, the result is still original and we need to sort the vector
        in descending order, i.e the highest value will be in the first position of the vector.
        '''
        
# DETECT THE FRAME TRANSITIONS IN THE VIDEO FROM THE DIFFERENCE ON MEAN GRAY LEVELS OF EACH FRAME------------------------------------------------------------

        self.v              = np.sort(self.diff_meangray[0:-2])[::-1]
        self.t              = np.argsort(self.diff_meangray[0:-2])[::-1]

        '''
        While we are sorting the value, we also collect the indices/ number of frame of which
        the highest difference of mean gray value belongs (defined in self.t)
         
        After that, we are reducing the scale of the computation by just sorting the top 20 frames
        which has the highest difference of mean gray value
        '''
# SORTING THE TOP 20 FRAMES WITH HIGHEST DIFFERENCE IN MEAN GRAY LEVELS ---------------------------------------------
        
        self.transitions   = np.sort(self.t[0:self.n])
        
        '''
        Sometimes, the video has an intro or ending which display the same content for couple of seconds.
        This intro or ending commonly also has a very high value of mean gray difference. 
        
        To avoid the algorithm will find this intro or ending rather than the top view scene that we wanted,
        we create algorithm that whenever the difference between the transition frame and the next two frame
        is less than 0.01, then the value will be considered as 0 or ignored. Else, the value of mean gray 
        levels from the frame which has the highest difference in mean gray value level will be stored in
        self.values
        '''
           
        for j in range (0,self.n):
                if abs(self.diff_meangray[self.transitions[j]+2]) < 0.01:
                    self.values[j] = 0.0
                else:
                    self.values[j] = self.meanGrayLevels[self.transitions[j]]
        
        '''
        Then, we can define the number of frame in which the top view scene begin (defined by self.t_r[:,0])
        
        But first, we need to sort the mean gray values stored in self.values in descending order once again as 
        well as collecting the indices/number of frame which has highest mean gray value defined in self.index_s_v
        '''
# GET THE FIRST FRAME OF TOP VIEW SCENE FROM THE VIDEO ----------------------------------------------
        
        self.values_r   = sorted(self.values,reverse=True)
        self.index_s_v  = sorted(range(len(self.values)),key = self.values.__getitem__,reverse=True)
        
        for j in range (0,self.n):
            self.transitions_r[j] = self.transitions[self.index_s_v[j]]

        '''
        Get the number of frame where the top view scene begin
        '''
        self.v_r[:,0] = self.values_r[0]
        self.t_r[:,0] = self.transitions_r[0]

        self.test_i = self.t_r[:,0].astype(int)
        self.a      = 0
        
        '''
        After we have the number of frame in which the top view begin, then we also need to determine how
        many frames the top view scene takes place. In order to do that, the while loop function is used.
        
        Typically, as long as the difference between one frame and the previous frame is smaller than 0.5,
        then no transition occurs, and if it's bigger than 0.5, then the frame transition occurs.
        '''
# DETECT THE NUMBER OF FRAME IN TOP VIEW SCENE---------------------------------------------------------------------------
        
        while (self.a == 0):
            if abs(self.meanGrayLevels[self.test_i+1]-self.meanGrayLevels[self.test_i,:])/self.meanGrayLevels[self.test_i+1,:]>0.5:
                self.a  += 1
            self.test_i += 1
        
        '''
        After that, get the number of frame where the top view scene ends (defined in self.t_r[:,1])
        '''
        self.t_r[:,1]   = self.test_i-1
        self.int_t_r    = self.t_r[:,1].astype(int)

        self.v_r[:,1]   = self.meanGrayLevels[self.int_t_r]
        self.int_t_r    = self.t_r.astype(int)

        '''
        Final step, define the getter function to grab the number of frame in which the top view scene begin
        and end so that we can use it in the main file
        '''
# GET THE FIRST AND THE LAST FRAME OF THE TOP VIEW SCENE ------------------------------------------------------------
        
    def getTransitions(self):
        return(self.int_t_r)

    def solver(self):
        self.transition_identifier()
        self.getTransitions()
        
        