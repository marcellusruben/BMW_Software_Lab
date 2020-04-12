# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 13:15:25 2017

@author: Marcellus Ruben Winastwan
"""

import numpy as np
import matplotlib.pyplot as plt



class visualizeIO(object):
    
    def __init__(self,possible_initial_orientations, initial_orientation):
        self.possible_initial_orientations = possible_initial_orientations
        self.initial_orientation = initial_orientation
        
    def visualize_IO(self):
        
        '''
        First, initialize the global vectors with the size equal to the number of possible initial orientation generated as
        the rows and the initial orientation vectors as the columns
        '''
        self.nvs = self.possible_initial_orientations.shape[0]
        self.ks = np.zeros((self.nvs,9))
        
        '''
        Define the scaling factor a. Here we choose 10 so that the difference between each possible initial orientation
        can be seen
        '''
        self.a  = 10

        '''
        Setup another global vectors to store the value of the original initial orientation so that we can visualize it in a graph
        '''
        
        self.ks_0 = np.zeros((1,9))
        self.ks_0[0,0:3] = self.initial_orientation[0,0:3]
        self.ks_0[0,0:3] = self.ks_0[0,0:3]/np.linalg.norm(self.ks_0[0,0:3])
        self.ks_0[0,3:6] = self.initial_orientation[1,0:3]
        self.ks_0[0,3:6] = self.ks_0[0,3:6]/np.linalg.norm(self.ks_0[0,3:6])
        self.ks_0[0,6:9] = np.cross(self.ks_0[0,0:3],self.ks_0[0,3:6])
        self.ks_0[0,6:9] = self.ks_0[0,6:9]/np.linalg.norm(self.ks_0[0,6:9])
        
        '''
        Multiply the original initial orientation with the scaling factor
        '''
        self.x_1 = self.ks_0[0,0:3]*self.a
        self.x_2 = self.ks_0[0,3:6]*self.a
        self.x_3 = self.ks_0[0,6:9]*self.a

        '''
        Plot the original initial orientation and save it in png format
        '''
        
        fig = plt.figure(figsize = (8,6),dpi=200)
        ax = fig.add_subplot(111,projection ='3d')
        ax.set_xlim(-self.a*1.1,self.a*1.1)
        ax.set_ylim(-self.a*1.1,self.a*1.1)
        ax.set_zlim(-self.a*1.1,self.a*1.1)
        ax.plot([0.0,self.x_1[0]],[0.0,self.x_1[1]],[0.0,self.x_1[2]],color ='k',linewidth= 2.0)
        ax.plot([0.0,self.x_2[0]],[0.0,self.x_2[1]],[0.0,self.x_2[2]],color ='k',linewidth= 2.0)
        ax.plot([0.0,self.x_3[0]],[0.0,self.x_3[1]],[0.0,self.x_3[2]],color ='k',linewidth= 2.0)
        ax.set_xlabel('X', fontsize = 15)
        ax.set_ylabel('Y', fontsize = 15)
        ax.set_zlabel('Z', fontsize = 15)
        ax.set_title('Initial Orientation', fontsize = 20)
        plt.savefig('Original Initial Orientation.png')
        
        '''
        Here we plot the possible initial orientation generated from Possible_IO class and save it into png format
        '''
        
        fig = plt.figure(figsize = (10,8),dpi=200)
        ax = fig.add_subplot(111,projection ='3d')
        
        '''
        Loop over the number of generated possible initial orientation
        '''
        for i in range (0,self.nvs):
            self.initial_orientation_ = np.array([[self.possible_initial_orientations[i,0:3]],[self.possible_initial_orientations[i,3:6]]]).reshape(2,3)
            
            '''
            Fill the global vectors with each of the possible initial orientation in every iteration
            '''
            
            self.ks[i,0:3] = self.initial_orientation_[0,0:3]
            self.ks[i,0:3] = self.ks[i,0:3]/np.linalg.norm(self.ks[i,0:3])
            self.ks[i,3:6] = self.initial_orientation_[1,0:3]
            self.ks[i,3:6] = self.ks[i,3:6]/np.linalg.norm(self.ks[i,3:6])
            self.ks[i,6:9] = np.cross(self.ks[i,0:3],self.ks[i,3:6])
            self.ks[i,6:9] = self.ks[i,6:9]/np.linalg.norm(self.ks[i,6:9])
            
            '''
            Multiply the global vectors with the scaling factors so that the difference between each possible initial 
            orientation can be seen
            '''

            self.x_1 = self.ks[i,0:3]*self.a
            self.x_2 = self.ks[i,3:6]*self.a
            self.x_3 = self.ks[i,6:9]*self.a
                    
            ax.set_xlim(-self.a*1.1,self.a*1.1)
            ax.set_ylim(-self.a*1.1,self.a*1.1)
            ax.set_zlim(-self.a*1.1,self.a*1.1)
                    
            ax.plot([0.0,self.x_1[0]],[0.0,self.x_1[1]],[0.0,self.x_1[2]],color ='b',linewidth = 2.0)
            ax.plot([0.0,self.x_2[0]],[0.0,self.x_2[1]],[0.0,self.x_2[2]],color ='y',linewidth = 2.0)
            ax.plot([0.0,self.x_3[0]],[0.0,self.x_3[1]],[0.0,self.x_3[2]],color ='r',linewidth = 2.0)
            plt.draw()
            plt.pause(0.1)
            
        ax.set_xlabel('X', fontsize = 15)
        ax.set_ylabel('Y', fontsize = 15)
        ax.set_zlabel('Z', fontsize = 15)
        ax.set_title('Variations of Different Possible Orientations', fontsize = 20)
        plt.savefig('Variations of Different Possible Orientations.png')
        
        return self.ks
        