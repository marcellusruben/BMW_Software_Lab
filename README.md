# BMW Software Lab Project - Trajectory Reconstruction and Video Analysis for Kinematic Assessment and FEM Vaidation in Passive Safety Application

## Problem 
- Initial orientation of the sensor is commonly unknown, hence there is uncertainty regarding its data accuracy.
- The data obtained from sensor are only available in local coordinate system.

## Objective
The main objective of this project is to minimize the uncertainty of the data's accuracy resulted from the sensor. However, this is difficult to achieve since the initial orientation of the sensor is unknown. The solution for this problem is to compare the data from sensor with the data from Finite Element (FE) video, then run an optimization algorithm to minimize the error in the data from sensor.

## Steps
There are 4 main steps in this project: trajectory reconstruction, video analysis, optimization, and robustness. The following is the brief explanation of each process:
1. The main objective of trajectory reconstruction is to convert and manipulate sensor's data from local to global coordinate system, since it will be compared with the data from FE video. In order to achieve this, simultaneous orthogonal rotation angle method (SORA) is used. The output of this process is a new sensor's data in its global coordinate system.
2. In the video analysis part, the algorithm for object recognition and object tracking needs to be built to detect and track the desired object from FE video. The output of this step is a new data from FE video. The Python script itself is designed to be able to work in two cases of crash test: first, a top view video of vehicle crash test and second, a video of crash test dummy, as seen in the following pictures.
<p align="center">
  <img width="460" height="300" src="https://github.com/marcellusruben/BMW_Software_Lab/blob/master/frame_file_c119.jpg">
</p>
<p align="center">
  <img width="460" height="300" src="https://github.com/marcellusruben/BMW_Software_Lab/blob/master/videoPict.png">
</p>

3. In optimization part, the sensor's data will be compared with the data from FE video. To minimize the error in the sensor's data, a stochastic optimization algorithm, differential evolution, will be performed. The output of this step is a new and optimized sensor's data.
4. Robustness or sensitivity analysis part is beneficial to 'guess' several possibilities regarding the initial orientation of the sensor.

## Files
There are four folders in this project: trajectory reconstruction, video analysis, optimization, robustness.<br/>
In folder trajectory reconstruction:
- main.py - main file for trajectory reconstruction.
- Trajectory.py - to convert the data from local to global coordinate.
- Rot_Matrix_AA.py - to generate directional cosines matrix.
- Rot_Matrix_DC.py - to generate rotational matrix.
- two excel files as an input: acceleration and rotational velocity from sensor's data.<br/>

In folder video analysis:
- main_video.py - main file for video analysis.
- ReadVideo.py - to read the video and convert it into several grayscale frames.
- identify_transitions.py - to detect the top view scene should there be a vehicle crash test video.
- ReadFrames.py - the application of object recognition and object tracking algorithm.
- BarrierInfo.py - to check whether a barrier exists in the video.
- VehicleYellow.py - to obtain a bounding box coordinate for the region of interest (ROI).
- IIHSO folder - a video used for this project.<br/>

In folder optimization:
- Opt.py - the main file in order for optimization process to proceed.
- The rest of the files are the combination of the files from trajectory reconstruction and video analysis.<br/>

In folder robustness:
- main.py - the main file for sensitivity study.
- Possible_IO.py - to generate several new possibilities of the initial orientation of the sensor.
- Signal_Error.py -  add certain tolerance from several possibilities generated from Possible_IO.py.
- Visualize_IO.py - to visualize several possibilities of initial orientation from Possible_IO.py.
- The rest of the files are the same as the file from trajectory reconstruction.
