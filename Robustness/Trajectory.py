# -*- coding: utf-8 -*-
"""
Created on Tue May 30 21:39:39 2017

@author: Marcellus Ruben Winastwan
"""
import numpy as np

from scipy import integrate
from Rot_Matrix_AA import genRotMatrixAA
from Rot_Matrix_DC import genRotMatrixDC


class Trajectory(object):
    
    def __init__ (self, variables):
        self.time_vector = variables[0]
        self.local_acceleration = variables[1]
        self.rotational_velocity= variables[2]
        self.initial_position = variables[3]
        self.initial_orientation= variables[4]
        self.initial_velocity = variables[5]
        self.cosin = []
		# Initialize vectors:
        self.totaltimesteps()
        self.globalcoordsystem()
        self.dtvector()
        self.globalvectors()
        self.localiniorientation()
        self.localangles()
    
#-------------------------------------------------------------------------------------
	# Initialize vectors:
    # Initiate the number of time steps
#-------------------------------------------------------------------------------------
    def totaltimesteps(self):
        self.nts = len(self.time_vector)
    
    # Initialize the global coordinate system
    def globalcoordsystem(self):
        self.Xv = np.array([[1.0],[0.0],[0.0]]).reshape(1,3)
        self.Yv = np.array([[0.0],[1.0],[0.0]]).reshape(1,3)
        self.Zv = np.array([[0.0],[0.0],[1.0]]).reshape(1,3)
    
	# Initialize the dt vector
    def dtvector(self):
        self.dt     = np.zeros((self.nts))
        self.dt[1:] = np.diff(self.time_vector)
        self.dt[0]  = 0.0   
    
    # Initialize the global vectors
    def globalvectors(self):
        self.g_acce = np.zeros((self.nts,3))
        self.g_velo = np.zeros((self.nts,3))
        self.g_posi = np.zeros((self.nts,3))
        self.g_angl = np.zeros((self.nts,3))
	
	# Initialize the local orientations
    def localiniorientation(self):
        self.ks=np.zeros((self.nts,9))
        self.ks[0,0:3] = self.initial_orientation[0,0:3]
        self.ks[0,0:3] = self.ks[0,0:3]/np.linalg.norm(self.ks[0,0:3])
        self.ks[0,3:6] = self.initial_orientation[1,0:3]
        self.ks[0,3:6] = self.ks[0,3:6]/np.linalg.norm(self.ks[0,3:6])
        self.ks[0,6:9] = np.cross(self.ks[0,0:3],self.ks[0,3:6])
        self.ks[0,6:9] = self.ks[0,6:9]/np.linalg.norm(self.ks[0,6:9])

	# Initialize local angles vectors
    def localangles(self):
        self.l_angles      = np.zeros((self.nts,3))
        self.l_angles[:,0] = self.rotational_velocity[:,0]*self.dt
        self.l_angles[:,1] = self.rotational_velocity[:,1]*self.dt
        self.l_angles[:,2] = self.rotational_velocity[:,2]*self.dt
	#-------------------------------------------------------------------------------------
	# Calculate global accelerations, angles and coordinate system
    def cycleovertimestep(self):	   
		# Calculate global accelerations, angles and coordinate system
        for i in range (0,self.nts-1):
			# Calculate directional cosines
            cxx = np.dot(self.Xv,self.ks[i,0:3])
            cyx = np.dot(self.Yv,self.ks[i,0:3])
            czx = np.dot(self.Zv,self.ks[i,0:3])
            cxy = np.dot(self.Xv,self.ks[i,3:6])
            cyy = np.dot(self.Yv,self.ks[i,3:6])
            czy = np.dot(self.Zv,self.ks[i,3:6])
            cxz = np.dot(self.Xv,self.ks[i,6:9])
            cyz = np.dot(self.Yv,self.ks[i,6:9])
            czz = np.dot(self.Zv,self.ks[i,6:9])
            
			# Generate rotational matrix
            self.RM = genRotMatrixAA(cxx, cyx, czx, cxy, cyy, czy, cxz, cyz, czz)
			# Rotate local acceleration
            self.g_acce[i,0:3]= np.dot(self.RM.RotationMatrixAA(),np.matrix.transpose(self.local_acceleration[i,0:3]))

			# Rotate local velocity
            self.g_angl[i,0:3]= np.dot(self.RM.RotationMatrixAA(),np.matrix.transpose(self.l_angles[i,0:3]))

			# Calculate angle for simultaneous orthogonal rotations
            self.phi= self.l_angles[i,0:3]
            pVector = self.phi/ np.linalg.norm(self.phi)
            anglesRad = np.linalg.norm (self.phi)

			# Calculate rotational matrix
            self.RotMatrix_l = genRotMatrixDC(anglesRad,pVector)
            
            if i>0:
               self.cosin.append(self.g_angl[i,0:3])
            else:
               self.cosin.append(self.g_angl[i,0:3]+self.g_angl[i-1,0:3])
               
			# Rotate coordinate system
            if i+1 < self.nts:
                self.ks[i+1,0:3] = np.dot(self.RotMatrix_l.RotationMatrixDC(),np.matrix.transpose(self.ks[i,0:3]))
                self.ks[i+1,3:6] = np.dot(self.RotMatrix_l.RotationMatrixDC(),np.matrix.transpose(self.ks[i,3:6]))
                self.ks[i+1,6:9] = np.dot(self.RotMatrix_l.RotationMatrixDC(),np.matrix.transpose(self.ks[i,6:9]))
        
		
		# Save last value of coordinate system
        self.ks[-1,0:3] = self.ks [-2,0:3]
        self.ks[-1,3:6] = self.ks [-2,3:6]
        self.ks[-1,6:9] = self.ks [-2,6:9]
	
	# Calculate global velocites and positions
    def globalvalue(self):
       
        self.g_velo[:,0] = integrate.cumtrapz(self.g_acce[:,0],self.time_vector,initial=0)+self.initial_velocity[0][0]
        self.g_velo[:,1] = integrate.cumtrapz(self.g_acce[:,1],self.time_vector,initial=0)+self.initial_velocity[0][1]
        self.g_velo[:,2] = integrate.cumtrapz(self.g_acce[:,2],self.time_vector,initial=0)+self.initial_velocity[0][2]
        
        self.g_posi[:,0] = integrate.cumtrapz(self.g_velo[:,0],self.time_vector,initial=0)+self.initial_position[0][0]
        self.g_posi[:,1] = integrate.cumtrapz(self.g_velo[:,1],self.time_vector,initial=0)+self.initial_position[0][1]
        self.g_posi[:,2] = integrate.cumtrapz(self.g_velo[:,2],self.time_vector,initial=0)+self.initial_position[0][2]
        
        self.g_angl[:,0] = integrate.cumtrapz(self.g_angl[:,0],initial=0)
        self.g_angl[:,1] = integrate.cumtrapz(self.g_angl[:,1],initial=0)
        self.g_angl[:,2] = integrate.cumtrapz(self.g_angl[:,2],initial=0)
		
		
		# Calculate displacements
        self.g_disp=np.zeros((self.nts,3))
        self.g_disp[:,0] = self.g_posi[:,0]-self.initial_position[0][0]
        self.g_disp[:,1] = self.g_posi[:,1]-self.initial_position[0][1]
        self.g_disp[:,2] = self.g_posi[:,2]-self.initial_position[0][2]
    #-------------------------------------------------------------------------------------    
        
	#-------------------------------------------------------------------------------------
    #Create the Getter Functions
    def getacce(self):
        return self.g_acce
    
    def getvelo(self):
        return self.g_velo
    
    def getangl(self):
        return self.g_angl
    
    def getposi(self):
        return self.g_posi
    
    def getks(self):
        return self.ks
    
    def getCosin(self):
        return self.cosin

    #-------------------------------------------------------------------------------------    
    #Print the Results and Export Them into CSV Files    
    def printer(self):
		# Delimiter for all the files
        self.delim = ';'
		# Save global accelerations
        self.time_units  = '[s]'
        self.time_symbol = 't'
        self.acce_units  = '[m/s^2]'
        self.acce_symbol = 'ax','ay','az'
        self.acce_file   = 'global_acc.csv'
        self.acce_header = [self.time_symbol+self.time_units,self.acce_symbol[0]+self.acce_units,self.acce_symbol[1]+self.acce_units,self.acce_symbol[2]+self.acce_units]
        self.g_acce_w_time       = np.zeros((self.nts,4))
        self.g_acce_w_time[:,0]  = self.time_vector
        self.g_acce_w_time[:,1:] = self.g_acce
        np.savetxt(self.acce_file,self.g_acce_w_time,delimiter =self.delim,header=self.delim.join(self.acce_header),fmt='%.5f')

		# Save global positions
        self.posi_units  = '[m]'
        self.posi_symbol = 'x','y','z'
        self.posi_file   = 'global_posi.csv'
        self.acce_header = [self.time_symbol+self.time_units,self.posi_symbol[0]+self.posi_units,self.posi_symbol[1]+self.posi_units,self.posi_symbol[2]+self.posi_units]
        self.g_posi_w_time       = np.zeros((self.nts,4))
        self.g_posi_w_time[:,0]  = self.time_vector
        self.g_posi_w_time[:,1:] = self.g_posi
        np.savetxt(self.posi_file,self.g_posi_w_time,delimiter =self.delim,header=self.delim.join(self.acce_header),fmt='%.5f')
		
		# Save global angles
        self.angl_units  = '[rad]'
        self.angl_symbol = 'tx','ty','tz'
        self.angl_file   = 'global_angle.csv'
        self.acce_header = [self.time_symbol+self.time_units,self.angl_symbol[0]+self.angl_units,self.angl_symbol[0]+self.angl_units,self.angl_symbol[0]+self.angl_units]
        self.g_angl_w_time       = np.zeros((self.nts,4))
        self.g_angl_w_time[:,0]  = self.time_vector
        self.g_angl_w_time[:,1:] = self.g_angl
        np.savetxt(self.angl_file,self.g_angl_w_time,delimiter =self.delim,header=self.delim.join(self.acce_header),fmt='%.5f')


    def solver(self):

        self.cycleovertimestep()
        self.globalvalue()
        self.printer()
        self.getacce()
        self.getangl()
        self.getposi()
        self.getks()




        

