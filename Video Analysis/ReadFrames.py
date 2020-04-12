# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 23:16:07 2017

@author: Marcellus Ruben Winastwan
"""
import os
import cv2 
import csv
import numpy as np

from BarrierInfo import getBarrierInfo
from VehicleYellow import getVehicleYellow


class read_frame(object):
    
    def __init__(self,fin,input_videos_folder,trans):
#        self.ext                    = ext
        self.fin                    = fin
        self.input_videos_folder    = input_videos_folder
        self.trans                  = trans
#        self.spatial_filter_manual  = spatial_filter_manual

    
    def reading_frame(self):
        
        '''
        setup the video path or working directory and capture the video to get the information of the number of
        frame, width, and height of the video
        '''
#SETUP RESULTING VIDEO FORMAT
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter('Video_Analysis.avi',fourcc, 10.0,(1872,800))
        
#SETUP THE VIDEO PATH AND CAPTURE THE VIDEO ------------------------------------------------------------

        self.KQ_str = 0
        self.MovieFullName  = os.path.join(self.input_videos_folder,self.fin)
        
        self.VideoObject    = cv2.VideoCapture(self.MovieFullName)
        self.numberOfFrames = int(self.VideoObject.get(cv2.CAP_PROP_FRAME_COUNT))
        self.vidHeight = int(self.VideoObject.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.vidWidth = int(self.VideoObject.get(cv2.CAP_PROP_FRAME_WIDTH))
        
        
        self.j = 1

        '''
        specify the user input value such as: time, initial position of the sensor, the coordinate system seen in
        the video expressed in the global coordinate system so that the data that we get from the video can be a
        valid benchmark/reference for the data that we get from trajectory class.
        
        Scaling factor is needed to resize the image so that the computation time will be faster.
        
        And target_size is needed to convert the unit from pixel to mm.
        '''

#USER INPUT VALUE -------------------------------------------------------------------------------------

        self.time = 0 #USER INPUT
        
        self.value_initial_position = np.zeros((1,3))

        self.value_initial_position[:,0] = 1388.62
        self.value_initial_position[:,1] = -412.101
        self.value_initial_position[:,2] = 858.216
        
        self.global_position_x = 1
        self.global_position_y = 1
        self.global_position_z = -1
        
        self.scaling_factor_width = 0.25
        self.scaling_factor_height= 0.25
        
        self.target_size = 40

        '''
        Then, detect the transition: if the video contains a lot of transitions, e.g side view, top view, etc, then 
        we try to make sure that the video will take the first frame of the top view as the first input, and will 
        take the last frame of the top view as the second input (as we already get in the identify_transition class)

        If the video doesn't contain any transition, then we take the very first frame of the video as the first
        input, and the last frame of the video as the second input
        '''

# DETECT THE TRANSITIONS -----------------------------------------------------------------------------
        
        self.real_trans = self.trans
        self.scalar_real_trans_start = np.asscalar(self.real_trans[:,0])+1
        self.scalar_real_trans_end   = np.asscalar(self.real_trans[:,1])
#        print(self.real_trans[:,0])
        
        if self.trans[:,0] == 0 :
            self.real_trans_ = np.zeros((1,2))
            self.real_trans_[:,0] = 0
            self.real_trans_[:,1] = self.numberOfFrames-1
            self.real_trans = self.real_trans_.astype(int)
            
            self.scalar_real_trans_start = np.asscalar(self.real_trans[:,0])
            self.scalar_real_trans_end   = np.asscalar(self.real_trans[:,1])
            
        '''
        Initialize the time and displacement vector, as well as the position vector before we are looping
        through each frame of the videoto get the result of time, displacement, and position of the sensor 
        in each frame.
        '''
#INITIALIZE THE TIME, DISPLACEMENT, AND POSITION VECTOR----------------------------------------------------------------

        self.ref_trajectory_pos_x = []
        self.ref_trajectory_pos_y = [] 
        self.ref_trajectory_pos_z = []
        self.ref_trajectory_time   = []

        self.current_position_x    = np.zeros((1,self.scalar_real_trans_end-self.scalar_real_trans_start))
        self.current_position_y    = np.zeros((1,self.scalar_real_trans_end-self.scalar_real_trans_start))
        self.current_position_z    = np.zeros((1,self.scalar_real_trans_end-self.scalar_real_trans_start))

        '''
        Loop through the whole top view scene of the video to get the result of time and position of the sensor
        in each frame
        '''

#LOOP THROUGH THE WHOLE TOP VIEW SCENE OF THE VIDEO ----------------------------------------------------------------------

        for frame in range (self.scalar_real_trans_start,self.scalar_real_trans_end):

            self.VideoObject.set(1,frame)

            success = True        
            success, self.frame_file_c = self.VideoObject.read()

        
            if success:
                
    
# GET THE BARRIER COLOR AND POSITIONS ------------------------------------------------------------------------------------------------------
                
                '''
                First, we need to check if the frame contains a barrier or not. The most common color of 
                the barrier for crash test simulation is orange/brown. Hence, we need to set a certain threshold 
                of blue, green, and yellow color so that the masked frame will only detect the orange/brown 
                color in the frame
                '''
                
                b2 = 60
                b1 = 0 
                g1 = 100
                g2 = 130
                r1 = 200
                r2 = 255
                self.treshold = [[b1,b2],[g1,g2],[r1,r2]]

                if self.j<2:

                    self.BarrierInfo    = getBarrierInfo(self.frame_file_c,self.treshold)
                    self.BarrierInfo.BarrierInfo()
                
                '''
                There are two possibilities of the result that we get from the BarrierInfo class. 
                First: The frame contains a barrier. In this case the BarrierInfo class will return the 
                coordinate of the bounding box of the barrier seen in the frame
                
                Second: The frame doesn't have a barrier. In this case, the BarrierInfo class will simply 
                return the coordinate of the bounding box = [0,0,0,0]
                '''
                

#GET THE TARGET POSITION -----------------------------------------------------------------------------------------------------------------------
                '''
                After that, set another threshold to detect the yellow target in the frame. Normally, the 
                yellow color of the target differs from one video to another, then the adjustment of the 
                threshold also need to be done.
                
                Before detecting the yellow color in the frame, we need to resize the image especially if
                the frame contains a barrier (which means it is a crash test video). The crash test video
                commonly has a huge region of interest (ROI) which will take a lot of time to compute. Hence,
                we need to resize the image.
                
                Meanwhile, a frame which doesn't contain a barrier commonly has a small ROI, thus resizing the
                image is unecessary.
                '''
                
                if self.BarrierInfo.getCoordBarrier() == [0,0,0,0]:
                    b2 = 88
                    b1 = 0
                    g1 = 160
                    g2 = 255
                    r1 = 160
                    r2 = 255
                    
                    self.frame_file_resize = cv2.resize(self.frame_file_c,None,fx = 1,fy = 1, interpolation=cv2.INTER_AREA)
                    
                else:
                    b2 = 85
                    b1 = 0
                    g1 = 135
                    g2 = 255
                    r1 = 135
                    r2 = 255
                    
                    self.frame_file_resize = cv2.resize(self.frame_file_c,None,fx = self.scaling_factor_width,fy = self.scaling_factor_height, interpolation=cv2.INTER_AREA)
                    
                self.treshold_yellow = [[b1,b2],[g1,g2],[r1,r2]]

                self.VehicleYellow = getVehicleYellow(self.frame_file_resize,self.BarrierInfo.getCoordBarrier(),self.treshold_yellow)
                self.VehicleYellow.VehicleYellow()
                
                '''
                The output that we get from the VehicleYellow class is the coordinate of the bounding box
                that covers our ROI (part of the frame which contains yellow color).
                
                However, the result is shown in pixel. In order to become a valid reference/benchmark for the
                data that we get from trajectory class, then we need to convert the unit from pixels to mm
                '''                
#CONVERT THE UNIT FROM PIXEL TO MM ---------------------------------------------------------------------------
                
                if self.j == 1:
                    
                    self.length_rectangle_pixels = self.VehicleYellow.getCoordVehYellow()[2]-self.VehicleYellow.getCoordVehYellow()[0] 
                    self.cf_pxl2mm = self.target_size/self.length_rectangle_pixels
                    
#               
                cv2.rectangle(self.frame_file_resize,(self.VehicleYellow.getCoordVehYellow()[0],self.VehicleYellow.getCoordVehYellow()[1]),(self.VehicleYellow.getCoordVehYellow()[2],self.VehicleYellow.getCoordVehYellow()[3]),(0,255,0),2)

                '''
                Then, we need to find the target in each frame, usually defined as black and yellow circle
                in the frame. In order to do that, we need to create a masked black and white frame. White
                if the frame contains a yellow color and black if not.
                
                In algorithm below, first we copy the original frame, and then turn it into entirely black
                '''

##CREATE A COPY OF THE CONTRAST FRAME AND THEN MAKE IT AS A COMPLETELY BLACK FRAME ----------------------------------------------------------------------

                self.ref_frame      = self.VehicleYellow.getPattern().copy().astype(float)
                self.ref_frame[:,:] = 0

                self.final_frame    = self.ref_frame.copy()
                
                '''
                After that, we need to create a structuring element. This is an important feature so that
                the algorithm will find the correct target (in this case the center of the black and yellow
                target) from our ROI
                
                This structuring element will detect which part of the frame has the highest nonzero values.
                And as expected, the part in the frame which has the highest nonzero values belongs to the
                center circle of black and yellow target
                '''

##CREATE A STRUCTURING ELEMENT TO DETECT THE HIGHEST NONZERO VALUE IN THE MATRICES -------------------------------------------------------
               
                if self.VehicleYellow.getCoordVehYellow()[2]-self.VehicleYellow.getCoordVehYellow()[0] < 30:                 
                    self.boundary_width = self.VehicleYellow.getCoordVehYellow()[2]-self.VehicleYellow.getCoordVehYellow()[0]
                    self.boundary_height= self.VehicleYellow.getCoordVehYellow()[3]-self.VehicleYellow.getCoordVehYellow()[1]              
                    self.kernel         = cv2.getStructuringElement(cv2.MORPH_RECT,(self.boundary_height,self.boundary_width))
                    
                else:
                    self.boundary_width = int(self.scaling_factor_width*21)
                    self.boundary_height= int(self.scaling_factor_height*21)
                    self.kernel         = cv2.getStructuringElement(cv2.MORPH_RECT,((self.boundary_width,self.boundary_height)))

                '''
                After defining the structuring element, then we loop through the entire top view scene and
                apply the dilation technique so that the structuring element can detect the center of black 
                and yellow circle in every frame
                '''
##LOOP OVER THE AREA OF THE RECTANGLE TO DETERMINE THE CENTER OF THE CIRCLE BY OBSERVING THE HIGHEST NONZERO VALUES IN THE MATRICES ----------------------

                for i in range (0,((self.VehicleYellow.getCoordVehYellow()[3])-(self.VehicleYellow.getCoordVehYellow()[1]))):
                    for j in range (0,((self.VehicleYellow.getCoordVehYellow()[2])-(self.VehicleYellow.getCoordVehYellow()[0]))):
                        
                        self.ref_frame[i,j]         = 1
#                      
                        self.ref_frame_final        = cv2.dilate(self.ref_frame,self.kernel,iterations=1)
                        self.ref_frame_final_result = np.logical_and(self.ref_frame_final,self.VehicleYellow.getPattern())
                        self.sum_nonzero            = np.count_nonzero(self.ref_frame_final_result)
                        self.final_frame[i,j]       = self.sum_nonzero

                        self.ref_frame[i,j]         = 0

                '''
                After we get the information of the highest nonzero values, then we can determine 
                the coordinate of center black and yellow circle.
                '''
                
##DETERMINE THE COORDINATE OF THE CENTER OF THE CIRCLE IN EVERY FRAME ------------------------------------------------------------------------------------
                
                self.center_of_circle_tuple     = np.unravel_index(self.final_frame.argmax(),self.final_frame.shape)
                self.int_center_of_circle_z     = self.center_of_circle_tuple[0].astype(int)
                self.int_center_of_circle_x     = self.center_of_circle_tuple[1].astype(int)
                self.center_of_circle           = [self.int_center_of_circle_x,self.int_center_of_circle_z]
                print(np.amax(self.final_frame))
                print(self.center_of_circle)
             
                '''
                Then, draw the circle to mark the center circle based from the information of the coordinate 
                of center black and yellow target so that it will be visible in each frame
                '''
                
                cv2.circle(self.frame_file_resize,(((self.VehicleYellow.getCoordVehYellow()[0])+self.center_of_circle[0]),((self.VehicleYellow.getCoordVehYellow()[1])+self.center_of_circle[1])),3,(0,255,0))
#                cv2.imwrite('frame_file_c.jpg', self.frame_file_c)

                '''
                Then, we can define the position of the center circle in x and z direction (in the video the y direction 
                is not visible, so we assume it's 0 in every frame).
                
                However, the result is still in pixels. To make it a valid benchmark/reference data, then
                we need to convert it to mm
                '''

##CONVERT THE DISP UNIT FROM PIXELS TO MM AND STORE THE DISPLACEMENT VALUE IN EVERY FRAME AND WRITING THEM INTO A VIDEO FILE -------------------------------------------------------------------------------------------------

                self.pos_x_pixels = self.VehicleYellow.getCoordVehYellow()[0]+self.center_of_circle[0]
                self.pos_z_pixels = self.VehicleYellow.getCoordVehYellow()[1]+self.center_of_circle[1]
                self.pos_y_pixels = 0
                
                self.pos_x_mm = np.multiply(self.cf_pxl2mm,self.pos_x_pixels)
                self.pos_y_mm = np.multiply(self.cf_pxl2mm,self.pos_y_pixels)
                self.pos_z_mm = np.multiply(self.cf_pxl2mm,self.pos_z_pixels)
                
                '''
                Then, append the time and position of center circle in x,y,z into the vectors that we already initialized
                above in each loop, so that in the end we can get the complete results/data
                '''
                
                self.ref_trajectory_pos_x.append(int(self.pos_x_mm))
                self.ref_trajectory_pos_y.append(int(self.pos_y_mm))
                self.ref_trajectory_pos_z.append(int(self.pos_z_mm))
                self.ref_trajectory_time.append(float(self.time))
                
                
                cv2.imwrite("frame_file_c%d.jpg" % self.j, self.frame_file_resize)  
                
                self.out.write(self.frame_file_resize)
#
            self.j    += 1
            self.time += 0.002
        
        '''
        Then, we collect the position and time vectors and concatenate it into one single array so that
        we can save the output result into csv file
        '''
##COLLECT THE DISPLACEMENT IN AN ARRAY --------------------------------------------------------------------------------- 
       
        self.diff_x = np.diff(self.ref_trajectory_pos_x)*self.global_position_x
        self.diff_y = np.diff(self.ref_trajectory_pos_y)*self.global_position_y   
        self.diff_z = np.diff(self.ref_trajectory_pos_z)*self.global_position_z 
          
        self.ref_trajectory_pos_x  = np.array([self.ref_trajectory_pos_x]).reshape((self.j-1,1))
        
        self.ref_trajectory_pos_y  = np.array([self.ref_trajectory_pos_y]).reshape((self.j-1,1))
        self.ref_trajectory_pos_z  = np.array([self.ref_trajectory_pos_z]).reshape((self.j-1,1))
        self.ref_trajectory_time    = np.array([self.ref_trajectory_time]).reshape((self.j-1,1))

        self.ref_trajectory_overall = np.concatenate((self.ref_trajectory_time,self.ref_trajectory_pos_x,self.ref_trajectory_pos_y,self.ref_trajectory_pos_z),axis=1 )
        
        '''
        However, the position that we get in each frame above is still based on the actual position seen
        in the video. In oder to make it a valid reference data, then we need to make an adjustment by
        transforming the position that we already got into the position based on the intial position
        x, y, z that the user need to specify manually
        '''

##TRANSFORM THE CURRENT POSITION RESULT INTO THE ACTUAL POSITION RESULT DEPENDING ON THE INPUT OF INITIAL POSITION---------------------------------------------------------------
        
        for i in range (self.scalar_real_trans_start,self.scalar_real_trans_end):
            
            if i == self.scalar_real_trans_start:
                
                self.current_position_x[:,i] = self.value_initial_position[:,0]
                self.current_position_y[:,i] = self.value_initial_position[:,1]
                self.current_position_z[:,i] = self.value_initial_position[:,2]
                
            
            if i > self.scalar_real_trans_start:
                
                self.current_position_x[:,i] = self.current_position_x[:,i-1]+self.diff_x[i-1]
                self.current_position_y[:,i] = self.current_position_y[:,i-1]+self.diff_y[i-1]
                self.current_position_z[:,i] = self.current_position_z[:,i-1]+self.diff_z[i-1]

        '''
        Then once again we collect the position vectors and the concatenate it into one vectors. 
        With the information of the position for the center circle in each frame, it is possible to
        determine the displacement and collect the result into one array
        '''

        self.real_ref_trajectory_x = self.current_position_x.reshape((self.scalar_real_trans_end-self.scalar_real_trans_start,1))
        self.real_ref_trajectory_y = self.current_position_y.reshape((self.scalar_real_trans_end-self.scalar_real_trans_start,1))
        self.real_ref_trajectory_z = self.current_position_z.reshape((self.scalar_real_trans_end-self.scalar_real_trans_start,1))
        print(self.real_ref_trajectory_x.shape)
        self.real_ref_trajectory_overall = np.concatenate((self.ref_trajectory_time,self.real_ref_trajectory_x,self.real_ref_trajectory_y,self.real_ref_trajectory_z),axis=1)
        
        '''
        We compute the displacement of the sensor in each frame
        '''
        
        self.ref_displacement = np.zeros((self.scalar_real_trans_end-self.scalar_real_trans_start,3))
        self.ref_displacement[:,0] = self.real_ref_trajectory_overall[:,1]- self.value_initial_position[:,0]
        self.ref_displacement[:,1] = self.real_ref_trajectory_overall[:,2]- self.value_initial_position[:,1]
        self.ref_displacement[:,2] = self.real_ref_trajectory_overall[:,3]- self.value_initial_position[:,2]
        
        '''
        Final step, we save the result into a csv file and also add the header in the csv file.
        This function will return the array of the displacement results.
        '''
        
##SAVE THE FINAL RESULT INTO CSV FILE AND ADD THE HEADER--------------------------------------------------------------------------------------------------------------------------------------------
        
        np.savetxt('real_ref_trajectory_csv.csv',self.real_ref_trajectory_overall,fmt='%f',delimiter=',')
        np.savetxt('real_ref_trajectory_displacement.csv',self.ref_displacement,fmt='%f',delimiter=',')
        
        with open('real_ref_trajectory_csv.csv',newline='') as f:
            r = csv.reader(f)
            data = [line for line in r]
        with open('real_ref_trajectory_csv.csv','w',newline='') as f:
            w = csv.writer(f)
            w.writerow(['time(s)','x(mm)','y(mm)','z(mm)'])
            w.writerows(data)
        
        return self.ref_displacement
    

        