#############################################
# Salem Tile Stitcher
# Author:pistolshrimp
# jmk1067@humboldt.edu
# Date: 08/04/2019
#
#############################################

# This script stitches together Salem map tiles.
# The tiles must be numbered correctly (ie merged) using the Salem Map Tool (https://github.com/dymm2000/salem-map-tool/releases)
# This must be run with a python 64bit executable, otherwise it will run into memory issues. 
# The folder with the tiles must be labeled, "Tiles". 
# Put this script in the same folder as (but not in) the folder named "Tiles". 

#############################################

"""
This function finds Maximum and Minimum tile numbers. 

Inputs:
- Two lists corresponding to the X and Y tile numbers. 

Outputs:
- The X and Y Maximum and X and Y Minimum tile numbers.
"""

def StartStop(List1, List2):
    XStart = min(List1) # Finds the Minimum value in the XList. 
    XStop = max(List1) # Finds the Maximum value in the XList. 
    YStart = min(List2) # Finds the Minimum value in the YList. 
    YStop = max(List2) # Finds the Maximum value in the YList. 
    return(XStart, XStop, YStart, YStop)

"""
This function grabs the tiles and merges the them together. 

Inputs:
- The starting and stoping values.

Outputs:
-The full image.

Notes:
It fucntion was roughly adapted from https://github.com/nst/gmap_tiles/blob/master/merge_tiles.py
"""

def MergeTiles(List1, List2, Path, Resolution):   
    ResNumber = int(Resolution) # Turns user resolution into an integer.
  
    XStart, XStop, YStart, YStop = StartStop(List1, List2) # Calls StartStop function.   
   
    AbsStart = abs(XStart) # Turns XStart to absolute for progress bar math.
    ProgressBarRange = AbsStart + XStop # Determines size of the progress bar. 
     
    TYPE, ext = 'r', 'png' # Image type. 
       
    Width = (XStop - XStart) * 100 # Width of the image. 100 is the pixels size each tile. 
    Height = (YStop - YStart) * 100 # Hieght of the image. 
    
    #print ("width:", Width)
    #print ("height:", Height)   

    result = Image.new("RGB", (Width, Height)) # Sets up image dimensions.

    layout = [[sg.Text("This popup will close when the map is done saving.")],  # Layout of the progress bar popup. 
              [sg.ProgressBar(ProgressBarRange, orientation='h', size=(20, 20), key='progressbar')],
              [sg.Cancel()]]
    
    window = sg.Window('Salem Map Stitcher', layout) # Calls the progress bar layout. 
    progress_bar = window.FindElement('progressbar')

    for x in range(XStart, XStop):                          
        for y in range(YStart, YStop):
           
            event, values = window.Read(timeout=0) # Breaks if user hits cancel. 
            if event == 'Cancel'  or event is None:
                break
            
            progress_bar.UpdateBar(x + AbsStart + 1) # Updates the progress bar. 
                                       
            FullPath = Path + "//"  # Established where to read the tiles from.
            FileName = FullPath + "tile_" + format(x) + "_" + format(y) + ".png" # Looks for each individual tile by name.
            MapName = "Salem_Map_Resolution" + format(ResNumber) # Creates a variable name based on the user selected resolution.
                        
            if not os.path.exists(FileName): # Deals with missing tiles.
                continue           
                                      
            x_paste = (x - XStart) * 100 # Finds where to paste.
            y_paste = Height - (YStop - y) * 100 # Finds where to paste.
                        
            try:
                i = Image.open(FileName)
            except Exception as e:
                print ("-- %s, removing %s" % (e, FileName))
                trash_dst = os.path.expanduser("~/.Trash/%s" % FileName)
                os.rename(FileName, trash_dst)
                continue
            
            result.paste(i, (x_paste, y_paste)) # Combines the images. 
            
            del i
    
    result.save(MapName+".jpg", quality=ResNumber, optimize=True) # Save based on name and resolution.
    
    window.Close()  # Closes the progress bar when everything is complete.

"""
This function finds the tiles and creates a list of X and Y values. 

Inputs:
- A path to a folder tiles organized by position. 

Outputs:
- A list of X and Y values as well as passing on the path and user selected resolution.
"""

def TileStitcher(Path, Resolution):    
    XList = []  # Creates a list of the X's.
    YList = []  # Creates a list of the Y's.
    
    Tiles = os.listdir(Path) # Gets a list of all the Tiles.
    
    for Tile in Tiles:
        TheFileName, TheFileExtension = os.path.splitext(Tile) # Breaks the file name into pieces based on periods.
        
        Tile, X, Y = os.path.basename(TheFileName).split("_") # Breaks the filename into pieces based on underscores.
        
        XInt = int(X) # Turns X values into integers for sorting purposes. 
        YInt = int(Y) # Turns Y values into integers for sorting purposes. 
        
        XList.append(XInt) # Adds the X to the XList.
        YList.append(YInt) # Adds the Y to the YList.
        
    MergeTiles(XList, YList, Path, Resolution) # Calls the function which creates the image.    

#############################################

import PySimpleGUI as sg
from PIL import Image
import sys, os
from sys import exit as exit

#############################################

column1 = [
    [sg.Text("Pick Resolution", size = (15,1), font = ('Calibri', 14, 'bold'))],
    [sg.Text("The higher the resolution", size = (20,1), font = ('Calibri', 10))],
    [sg.Text("the bigger the file.", size = (20,1), font = ('Calibri', 10))],
    [sg.Text("", size =(1,4))]]
column2 = [
    [sg.Text("Choose Tiles Folder", size = (30,1), font = ('Calibri', 14, 'bold'))],
    [sg.Text("Where your Salem Map Tool merged tile's are stored.", size = (50,1), font = ('Calibri', 10))],
    [sg.InputText(""), sg.FolderBrowse()],
    [sg.ReadButton("Run", font = ('Calibri', 16, 'bold'), size = (8, 1))],
    ]
    
layout = [
    [sg.Text("Salem Map Stitcher", font = ('Calibri', 20,'bold'))],
    [sg.Slider(range = (5, 100),orientation = 'v', size = (10,20), default_value = 25),
      sg.Text('   '), sg.Column(column1), sg.Column(column2),]
    ]

window = sg.Window("Salem Map Stitcher",grab_anywhere = False).Layout(layout) # Calls the window. 
 
while True:
    button, value = window.Read() # Extracts the button and the values from the user selections. 
    Resolution = value[0] # Resolution from the slider. 
    Source_Folder = value[1] # File path from the folder browser.    
    
    if not os.path.exists(Source_Folder+"//"+"tile_0_0.png"): # Checks if the dolder is correct, if not exits.
        sg.PopupCancel("Your folder must contain a 0_0 staring tile.")
        exit(0)            
        
    else:
        TileStitcher(Source_Folder, Resolution) # Calls the TileSticher function. 
    
       
