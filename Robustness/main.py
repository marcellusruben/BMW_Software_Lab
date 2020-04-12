# -*- coding: utf-8 -*-
"""
Created on Tue May 30 21:46:24 2017

@author: Marcellus Ruben Winastwan
"""
#------------------------------------------------------------------------------------------------------
# IMPORT libraries:
import numpy as np
from Trajectory import Trajectory
from Possible_IO import genPossibleIO
from Visualize_IO import visualizeIO
from Signal_Error import signal_error



'''
NOTE: Change the ffmpeg_path according to the directory/path where the ffmpeg path belongs in your directory
'''
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
initial_orientation = np.array([[-1.0,-0.000194820380622269, 0.0],[0.0,1.0,0.0]])
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


'''
Define the desired output directory of the trajectory video
''' 
#------------------------------------------------------------------------------------------------------
# CONFIGURATION VARIABLES:
#------------------------------------------------------------------------------------------------------
#Change the output directory into the desired directory in your computer
output_dir          = 'D:\\trajectory_animation.mp4'

'''
Define the timestep required to animate the trajectory result
'''
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

'''
Calculation of the trajectory based on the input variables defined above and pass it into trajectory class
'''  
# Calculate trajectory
variables      = [t,acceleration,rotvel,initial_position,initial_orientation,initial_velocity]
my_trajectory  = Trajectory(variables)
my_trajectory.solver()
# Save trajectory data: displacements
#trajectoryData = []
##Save trajectory positions of sensor
#SensorPosition= []
#
##pass to next functions the arguments directly
##------------------------------------------------------------------------------------------------------
## ANIMATION.
##------------------------------------------------------------------------------------------------------
#my_animator   = animator(frame_size, index_size, inputFileName, my_trajectory.g_disp, my_trajectory.g_posi,my_trajectory.cosin, initial_position, ffmpeg_path, output_dir,validation_files)
#my_animator.drawAnimation()

'''
Start of the sensitivity study
'''

#START OF THE SENSITIVITY STUDY------------------------------------------------------------------------------
'''
Fisrt, create a variation of possible initial orientation based on the initial orientation with the Possible_IO class
'''
e_tol = 2.0
s_tol = 2

possible_initial_orientations = genPossibleIO(e_tol,s_tol,initial_orientation)        

nvs = possible_initial_orientations.PossibleIO().shape[0]
#------------------------------------------------------------------------------
'''
Then, we visualize the possible initial orientation that we already created in Possible_IO class using visualize_IO class
'''
#Visualize Orientations

visual_orientations = visualizeIO(possible_initial_orientations.PossibleIO(),initial_orientation)
visual_orientations.visualize_IO()

'''
We also need to include the error in the signal, because the acceleration and rotational velocity signal are most likely having a certain error. Hence, we
define the error in the signal_error class with certain tolerance
'''
#Add the error in the accelerometer and velocity signal

max_error_acc = 0.01
max_error_rotvel = 0.01
samples_error = 2

acce_ae = signal_error(t,acceleration,samples_error,max_error_acc,'Local Acceleration')
rotvel_ae = signal_error(t,rotvel,samples_error,max_error_rotvel,'Local Rotational Velocity')

acce_ae.solver()
rotvel_ae.solver()

#------------------------------------------------------------------------------
'''
Create/initialize the global vectors with rows = number of timestep and columns = samples_error * number
of possible initial orientation generated
'''

#Initialize Global Vectors

g_acce_Tx = np.zeros((len(t),nvs*samples_error))
g_acce_Ty = np.zeros((len(t),nvs*samples_error))
g_acce_Tz = np.zeros((len(t),nvs*samples_error))
g_angl_Tx = np.zeros((len(t),nvs*samples_error))
g_angl_Ty = np.zeros((len(t),nvs*samples_error))
g_angl_Tz = np.zeros((len(t),nvs*samples_error))
g_posi_Tx = np.zeros((len(t),nvs*samples_error))
g_posi_Ty = np.zeros((len(t),nvs*samples_error))
g_posi_Tz = np.zeros((len(t),nvs*samples_error))

g_ks_x1 = np.zeros((len(t),nvs*samples_error))
g_ks_x2 = np.zeros((len(t),nvs*samples_error))
g_ks_x3 = np.zeros((len(t),nvs*samples_error))
g_ks_y1 = np.zeros((len(t),nvs*samples_error))
g_ks_y2 = np.zeros((len(t),nvs*samples_error))
g_ks_y3 = np.zeros((len(t),nvs*samples_error))
g_ks_z1 = np.zeros((len(t),nvs*samples_error))
g_ks_z2 = np.zeros((len(t),nvs*samples_error))
g_ks_z3 = np.zeros((len(t),nvs*samples_error))

#------------------------------------------------------------------------------
time_vector = t
#local_acceleration = acceleration
#rotational_velocity = rotvel

#------------------------------------------------------------------------------
ts = time_vector.shape[0]
k = 0

'''
Initiate the loop for the robustness analysis
'''
     
for i in range (0,samples_error):
    
    '''
    Here we are not using the original local orientation and rotational velocity anymore, but using the local acceleration
    and rotational velocity after considering the error
    '''
    local_acceleration = acce_ae.compute_signal_error()[i,:,:].reshape(ts,3)
    rotational_velocity = rotvel_ae.compute_signal_error()[i,:,:].reshape(ts,3)

    for j in range (0,nvs):
        
        '''
        Here we are also using the current initial orientation generated from the Possible_IO class
        '''
        current_initial_orientation = np.array([[possible_initial_orientations.getPIO()[j,0:3]],[possible_initial_orientations.getPIO()[j,3:6]]]).reshape(2,3)
    
        '''
        Run the trajectory class over the loop using the current initial orientation
        '''
        
        variables = [time_vector,local_acceleration,rotational_velocity,initial_position,current_initial_orientation,initial_velocity]
        my_trajectory = Trajectory(variables)
        my_trajectory.solver()
        
        '''
        Fill the global vector with the desired variables in each iteration
        '''
        
        g_acce_Tx[:,k] = my_trajectory.getacce()[:,0]
        g_acce_Ty[:,k] = my_trajectory.getacce()[:,1]
        g_acce_Tz[:,k] = my_trajectory.getacce()[:,2]
        g_angl_Tx[:,k] = my_trajectory.getangl()[:,0]
        g_angl_Ty[:,k] = my_trajectory.getangl()[:,1]
        g_angl_Tz[:,k] = my_trajectory.getangl()[:,2]
        g_posi_Tx[:,k] = my_trajectory.getposi()[:,0]
        g_posi_Ty[:,k] = my_trajectory.getposi()[:,1]
        g_posi_Tz[:,k] = my_trajectory.getposi()[:,2]

        g_ks_x1[:,k] = my_trajectory.getks()[:,0]
        g_ks_x2[:,k] = my_trajectory.getks()[:,1]
        g_ks_x3[:,k] = my_trajectory.getks()[:,2]
        g_ks_y1[:,k] = my_trajectory.getks()[:,3]
        g_ks_y2[:,k] = my_trajectory.getks()[:,4]
        g_ks_y3[:,k] = my_trajectory.getks()[:,5]
        g_ks_z1[:,k] = my_trajectory.getks()[:,6]
        g_ks_z2[:,k] = my_trajectory.getks()[:,7]
        g_ks_z3[:,k] = my_trajectory.getks()[:,8]
            
        k = k+1
    
     
Tx_min = min(g_posi_Tx[-1,:])
Ty_min = min(g_posi_Ty[-1,:])
Tz_min = min(g_posi_Tz[-1,:])
