# -*- coding: utf-8 -*-
"""
Created on Tue May 30 21:46:24 2017

@author: Marcellus Ruben Winastwan
"""
#------------------------------------------------------------------------------------------------------
# IMPORT libraries:
import numpy as np
from Trajectory import Trajectory
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3

'''
NOTE: Change the ffmpeg_path according to the directory/path where the ffmpeg path belongs in your directory
'''

#Change the ffmpeg_path according to the directory/path where the ffmpeg path belongs in your directory
ffmpeg_path = 'D:\\ffmpeg.exe'

'''
Define two sets of input to validate the trajectory result, each input has different local acceleration and 
rotational velocity data
'''
#------------------------------------------------------------------------------------------------------
# INPUT:Set 1
#------------------------------------------------------------------------------------------------------

filename_acc        = "19035_acc.csv"
filename_rvl        = "19035_gyr.csv"
# Sensor position
#initial_position    = np.array([[1434.266303,-355.1984118,921.7600248]])
initial_position    = np.array([[1704.84,407.44,949.253]])
# Initial orientation
initial_orientation = np.array([[1.0,0.0, 0.0],[0.0,0.0,1.0]])
# Initial velocity
initial_velocity    = np.array([[0.0,0.0,0.0]])
# Mesh file for rigid body motion:
inputFileName       = "19035_HEAD_T0.inp"
validation_files    = ["19035_HEAD_T0900.inp","19035_HEAD_T1200.inp","19035_HEAD_T1400.inp"]

#---------------------------------------------------------------------------------------------------
#Input: Set2
#---------------------------------------------------------------------------------------------------
'''
filename_acc        = "AL_F60_Header_FarSide_Sled_B_v89a_incl.csv"
filename_rvl        = "RVL_F60_Header_FarSide_Sled_B_v89a_incl.csv"
initial_position    = np.array([[1435.16,-352.9,926.594]])
initial_orientation = np.array([[-0.99801,0.0,-0.0836975],[0.0, -1.0, 0.0],[0.0, 0.0, 1.0]])
initial_velocity    = np.array([[0.0,0.0,0.0]])
inputFileName       = "F60_Head_FarSide_89a_T000.inp"
validation_files    = ["F60_Head_FarSide_89a_T080.inp","F60_Head_FarSide_89a_T120.inp","F60_Head_FarSide_89a_T140.inp"]
'''
#------------------------------------------------------------------------------------------------------
# CONFIGURATION VARIABLES:
#------------------------------------------------------------------------------------------------------
#Change the output directory into the desired directory in your computer
output_dir          = 'D:\\trajectory_animation.mp4'

##Set the required timestep (including 0 i.e frame_size 11 means 0 to 10)
frame_size          = 10
index_size          = 140
               
#------------------------------------------------------------------------------------------------------
# TRAJECTORY CALCULATION
#Read time acceleration and velocity from file
#Use semicolon (;) as delimiter for Input Set 2
#------------------------------------------------------------------------------------------------------
'''
Read the timestep, acceleration data, and rotational velocity from given csv files
'''
t              = np.genfromtxt(filename_acc, usecols= (0), delimiter=',', skip_header = 1, dtype=float)
acceleration   = np.genfromtxt(filename_acc, usecols= (1,2,3), skip_header = 1, delimiter=',', dtype=float)
rotvel         = np.genfromtxt(filename_rvl, usecols= (1,2,3), skip_header = 1, delimiter=',', dtype=float) 
# Calculate trajectory
variables      = [t,acceleration,rotvel,initial_position,initial_orientation,initial_velocity]
my_trajectory  = Trajectory(variables)
my_trajectory.solver()


