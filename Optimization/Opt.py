 #-------------------------------------------------------------------------------------------------------------------
# Import required libraries
#-------------------------------------------------------------------------------------------------------------------
#from CurveData import CurveData
from scipy.optimize import differential_evolution
import numpy as np
import os

import time
from Rot_Matrix_DC import genRotMatrixDC
from Trajectory import Trajectory
import main_tra
import main_video
import math
##############################################################################################################################################################
####################################        INPUTS        ####################################################################################################
##############################################################################################################################################################
#-------------------------------------------------------------------------------------------------------------------
# User Defined Inputs
#-------------------------------------------------------------------------------------------------------------------
TotalSimulationTime      = 0.1
Num_CPUs                 = 6
PenaltyFactor            = 1e20



def ComputeError(tra_ref,tra_cur):
    
    TotalError_x =math.sqrt(np.sum(np.subtract(tra_cur[:,0],tra_ref[:,0])**2))/abs(np.mean(tra_ref[:,0]))
    TotalError_y =math.sqrt(np.sum(np.subtract(tra_cur[:,1],tra_ref[:,1])**2))/abs(np.mean(tra_ref[:,1]))
    TotalError_z =math.sqrt(np.sum(np.subtract(tra_cur[:,2],tra_ref[:,2])**2))/abs(np.mean(tra_ref[:,2]))
    
    ErrorTotal = TotalError_x + TotalError_y + TotalError_z
    
    return ErrorTotal

   
def StopOptimization(Xc,**ConDE):

# This function is used to define a custom termination criteria for the Differential Evolution process.
# The function is passed to the optimization solver in callback. It is a compulsory 'Requirement' that this function 
# must take 2 arguments Xk and **ConDE, which are passed by the solver differential_evolution(); although they are not used in this case for computing the termination criteria inside the function.
# If the Function is to return 'False' the Optimization process will be halted and the best solution until that point will be stored in self.x
# If polish=True that will be still be executed after the Optimization is halted.
# Please read Scypy Differential Evolution Documentation for more details of the requirements of callback function    

	# If Terminate_Flag = False the optimization will evolve 1 Generation more; if True Optimization is halted.
    Terminate_Flag  = False
    
	# Solver Own Convergence Criteria; if  ConDE['convergence'] > 1 --> Stop Optimization
    #------------------------------------------------------------------------------------------------------- 
    Convergence =  ConDE['convergence']
	
	# Improvement Based Termination Criteria
    #------------------------------------------------------------------------------------------------------- 
    # Check if minimum number of evaluations was met.
    # And if counter is bigger than the maximum allowed number of times that Minimum Error could remain with no improvement
    # better than 'Delta' terminate Optimization.    
    #------------------------------------------------------------------------------------------------------- 
    
    global MinErrorList
    
	# Generate a list that stores a value of '1' if there was a CHANGE in Minimum Error greater than 'Delta' otherwise store '0'
    binarychangelist = []
    for i in range(len(MinErrorList)-1):
        
        if abs((MinErrorList[i+1] - MinErrorList[i])/ MinErrorList[i+1]) > Delta:
            
            binarychangelist.extend([1])
        else:
            binarychangelist.extend([0])
    
    # Generate a list that checks how many times the Minimum Error has shown a change greater than 'Delta'
    NumMinErrorChanges = [1]
    counter            = 0
    for j in range(1,len(binarychangelist)):
        
        NumMinErrorChanges.extend([binarychangelist[j]+NumMinErrorChanges[j-1]])
    
    # Count how many times the Minimum Error has remained with no change 
    NumCostFunEvalwithNoChange = NumMinErrorChanges[-1]
    for errorChange in NumMinErrorChanges:
        
        if errorChange == NumCostFunEvalwithNoChange:
            
            counter += 1 
    
   # Time based Termination Criteria
   #-------------------------------------------------------------------------------------------------------
    TimeCheck       = time.time()
    ElapsedTime     = TimeCheck - start
    T_Limit_sec     = T_Limit_hours * 60 * 60
	
   #-------------------------------------------------------------------------------------------------------
   # Stop Optimization    
   #-------------------------------------------------------------------------------------------------------    
	
	# Improvement Based Criteria
    if ImprovementCheck == True and len(MinErrorList) >  MinFunEvaluations and counter > NoprogressAfter :
		
        Terminate_Flag = True
        Reason = 'No Improvement of ' + str(Delta) + ' after ' + str(NoprogressAfter) + ' consecutive Cost Function Evaluations'
        
        with open('DE_Opt_Summary.txt', 'w+') as DE_Summary:
            
            DE_Summary.write('Optimization Halted:                   ' + 'TRUE; ' + Reason + '\n')
			
	
	# Maximum Time Criteria
    elif TimeLimit == True and ElapsedTime > T_Limit_sec:
        
        Terminate_Flag = True
        Reason = 'Time Limit of ' + str(T_Limit_hours) + ' h' + ' exceeded'
		
        with open('DE_Opt_Summary.txt', 'w+') as DE_Summary:
    			
            DE_Summary.write('Optimization Halted:                   ' + 'TRUE; ' + Reason + '\n')
	
    return Terminate_Flag 
#-------------------------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
##############################################################################################################################################################
####################################        Cost Function Definition        ##################################################################################
##############################################################################################################################################################

# Create an empty list to keep track of the Minimum Error evolution during the Optimization process.
MinErrorList = []
best_IO = []

def create_rotation_vector(elevation,azimuth):
    
    r = 1.0
    
    elev_rad = (elevation*math.pi)/180.0
    azim_rad = (azimuth*math.pi)/180.0
    x = r * np.cos(elev_rad) * np.cos(azim_rad)
    y = r * np.cos(elev_rad) * np.sin(azim_rad)
    z = r * np.sin(elev_rad)
    
    return [x,y,z]
    
    
def create_initial_orientation(X,original_initial_orientation):
    

#    alpha1  = X[0]
#    alpha2  = X[1]
    phi     = X[0]

    alpha1  = 0.
    alpha2  = 0.
    phi_rad = phi*math.pi/180.0
    
    rotation_vector = create_rotation_vector(alpha1,alpha2)
    rotation_matrix = genRotMatrixDC(phi_rad,rotation_vector)
    
    current_initial_orientation = np.zeros((2,3))
    current_initial_orientation[0,:] = np.matrix.transpose(np.dot(rotation_matrix.RotationMatrixDC(),np.transpose(original_initial_orientation[0,:])))
    current_initial_orientation[1,:] = np.matrix.transpose(np.dot(rotation_matrix.RotationMatrixDC(),np.transpose(original_initial_orientation[1,:])))
    
    return current_initial_orientation
    

def CostFunction(X):
    

#    original_initial_orientation   = np.array([[-1.0,-0.000194820380622269,0.0],[0.0,1.0,0.0]])    
    original_initial_orientation   = np.array([[1.0,0.0,0.0],[0.0,1.0,0.0]]) 
    current_initial_orientation    = create_initial_orientation(X,original_initial_orientation)
#    print('current initial orientation: ',current_initial_orientation )
    
    variables = [main_tra.t,main_tra.acceleration,main_tra.rotvel,main_tra.initial_position,current_initial_orientation,main_tra.initial_velocity]
    current_trajectory = Trajectory(variables)
    current_trajectory.solver()
    
    tra_cur = current_trajectory.getdisp()
        
    np.savetxt('tra_cur.csv',tra_cur, fmt='%.5f',delimiter = ',')

    #-----------------------------------------------------------------------------------------------------------------------
    # Compute Error between Reference and current using the Selected method in ErrorType and generate MinErrorList
    #-----------------------------------------------------------------------------------------------------------------------

    ErrorTotal = ComputeError(tra_ref,tra_cur)
    
	# MinErrorList will be written in DE_Log.txt to keep track of the evolution of the  computed Minimum Error.
	# Last entry of MinErrorList corresponds to minimum error found up that point in the Optimization run.
    global best_IO
    
    global MinErrorList
    
    if MinErrorList == [] :
        MinErrorList.extend([ErrorTotal])
        best_IO.extend([current_initial_orientation])
	
    elif ErrorTotal < MinErrorList[-1]:
        MinErrorList.extend([ErrorTotal])
        best_IO.extend([current_initial_orientation])
        
	
    else:	
        MinErrorList.extend([MinErrorList[-1]])
        best_IO.extend([best_IO[-1]])
        
		
    #-------------------------------------------------------------------------------------------------------------------
	# Create a log File to keep track evolution
	#-------------------------------------------------------------------------------------------------------------------
    Log_file 			= 'DE_Log.txt'
    variables = ['alpha1','alpha2','phi']
    FileDelimiter = ','
    OptParameterNames   = [variables[i] for i in range(len(X))]
    if not os.path.isfile(Log_file):
        with open(Log_file, 'w+') as Log:
            for names in OptParameterNames:
                print(names)
                Log.write(names + FileDelimiter)
			
            Log.write('Error' + FileDelimiter)
            Log.write('Min_Error' + '\n')
			
    OptParameterValues = [ X[i] for i in range(len(X))]
    with open(Log_file, 'a') as Log_1:
        for Vals in OptParameterValues:
            Log_1.write(str(Vals) + FileDelimiter)
				
        Log_1.write(str(ErrorTotal) + FileDelimiter)
        Log_1.write(str(MinErrorList[-1]) + '\n')
        
    print('MinErTotal', MinErrorList[-1], 'CIO',best_IO[-1][0,:], best_IO[-1][1,:])
#    print('MinErTotal',MinErrorList[-1])

   
    return ErrorTotal

    

	
##############################################################################################################################################################
####################################        Optimization        ##############################################################################################
##############################################################################################################################################################
# Differential Evolution Parameters
#-------------------------------------------------------------------------------------------------------------------
PopulationNumber 	= 20     # --> Due to rounding of integers it could either be the exact specified number or (PopulationNumber-1)
MaxGenerations   	= 5000   # --> DE solver min Generations number is len(X)+1 generations; X --> optimization parameters
Strategy         	= 'best2bin'
F                	= (0.5,1.0)
CR               	= 0.8

#Run a Gradient based Optimization using the best solution from DE as starting point 
#-------------------------------------------------------------------------------------------------------
SwitchtoGradients   = False

# Record Optimization run time
start 				= time.time()

#-------------------------------------------------------------------------------------------------------
#Stopping Optimization Criteria --> Set boolean to True to activate stopping criteria
#-------------------------------------------------------------------------------------------------------

# Optimization Time Based Stopping Criteria

TimeLimit           = True
T_Limit_hours       = 0.1

# Optimization Improvement Based Stopping Criteria

ImprovementCheck    = False
MinFunEvaluations   = 600
Delta               = 0.00000001
NoprogressAfter     = 50


#-------------------------------------------------------------------------------------------------------
# Prepare Bounds and NP factor based on input parameters
Np = PopulationNumber
#bounds = [[0,360],[0,360],[0,360]]
bounds = [[0,360]]
#-------------------------------------------------------------------------------------------------------
#Define global reference:
    
#ref_trajectory = read_frame(main_video.fin,main_video.input_videos_folder,main_video.trans)#Reference_displacements #Numpy array ntsx3
#tra_ref = ref_trajectory.reading_frame()

variables_ref = [main_tra.t,main_tra.acceleration,main_tra.rotvel,main_tra.initial_position,main_tra.initial_orientation,main_tra.initial_velocity]
ref_trajectory = Trajectory(variables_ref)
ref_trajectory.solver()

tra_ref = ref_trajectory.getdisp()

np.savetxt('tra_ref.csv',tra_ref,fmt='%f',delimiter = ',')

#Optimization = CostFunction([45.,45.,180.])
#print('TotalError: ',Optimization)
#-------------------------------------------------------------------------------------------------------------------
# Optimization
#------------------------------------------------------------------------------------------------------------------- 
Opt_SimplifiedModel = differential_evolution(CostFunction, bounds, strategy = Strategy, maxiter = MaxGenerations, popsize = Np, tol=0.01, mutation = F, recombination = CR, polish = SwitchtoGradients, init = 'latinhypercube', callback = StopOptimization)

np.savetxt('ErrorTotal.csv',MinErrorList,fmt='%f',delimiter = ',')
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
#Create a Summary file for the Optimization Process
end = time.time()
Duration = (end - start) / 60. / 60.