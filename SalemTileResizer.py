#############################################
# Salem Tile Resizer v1.0
# Author:"pistolshrimp"
# jkennedy@humboldt.edu
# Date: 08/22/2020
#
#############################################

# This script downsized Salem map tiles based on a user input.
# Change Scale to change output size.
# Put this script in the same folder that holds the folder with the tiles to be resized. 

#############################################

import cv2
import numpy as np
import os    

#############################################

ProjectPath = os.path.dirname(os.path.abspath(__file__)) # Finds the path of the current file. 
InputPath = ProjectPath+"/MergedMap/"  # Sets where the inputs are stored.  
OutpathPath = ProjectPath+"/resizedtiles/"  # Sets where the outputs will be stored.  

#############################################
     
TheList = os.listdir(InputPath) # Gets a list of all the files in the input folder.
for TheFile in TheList: # Loops through the tiles. 
    TheFileName, TheFileExtension = os.path.splitext(TheFile)  # Breaks the file name into pieces based on periods.
    InputFilePath = InputPath+TheFileName+TheFileExtension  # Creates a full path to the file.
    Img = cv2.imread(InputFilePath, cv2.IMREAD_UNCHANGED) # Reads in the tiles.    
   
    Scale = 50    
    
    Width = int(Img.shape[1] * Scale / 100) # Divides Width by Scale.
    Height = int(Img.shape[0] * Scale / 100)  # Divides Height by Scale.
    Size = (Width, Height)
    
    OutputImage = cv2.resize(Img, Size) # Resize the image.
    Save = OutpathPath + TheFileName + TheFileExtension  # Sets save path.
    cv2.imwrite(Save, OutputImage) # Writes image.

print("Complete")