#############################################
# Salem Tile Stitcher v2
# Author:"pistolshrimp"
# jkennedy@humboldt.edu
# Date: 08/22/2020
#
#############################################

# This script stitches together Salem map tiles.
# The tiles must be numbered correctly (ie merged) using the Salem Map Tool (https://github.com/dymm2000/salem-map-tool/releases)
# This must be run with a python 64bit executable, otherwise it will run into memory issues. 
# Requires tiles to be downsized to 10 - 50 px. 
# Put this script in the same folder that holds the rezized tiles folder. 

#############################################

def BeginningProcess(Manual, TileSize, Outputs): # Collects values and sends them to appropriate functions.
    if Manual == 0:
        TileSize = IfManual()
        NumberOfOutputs = NumberOfOutputsCaluclator(TileSize)  
        TileProcessor(NumberOfOutputs, TileSize)        
    else:
        TileProcessor(Outputs, TileSize)

def ListDividerTwo(List): # Divides lists into 2 parts.
    List.sort()
    ListSpilt = np.array_split(List, 2) 
    NewListA = ListSpilt[0]
    NewListB = ListSpilt[1]
    return(NewListA, NewListB)  

def ListDividerThree(List): # Divides lists into 3 parts.
    List.sort()
    ListSpilt = np.array_split(List, 3) 
    NewListA = ListSpilt[0]
    NewListB = ListSpilt[1]
    NewListC = ListSpilt[2]    
    return(NewListA, NewListB, NewListC)  

def IfManual(): # Finds the tile size for automatic sizing options. 
    Tile = Image.open(InputPath+"tile_0_0.png") # Loads in the first tile.
    Width, Height = Tile.size   
    return(Width)
    
def MergeTiles(List1, List2, Size, Name):  # Merges the tiles together and outputs the image.
    #IntSize = int(Size) # Turns tile size into an integer.   
    XStart, XStop, = StartStop(List1) # Calls StartStop function.   
    YStart, YStop  = StartStop(List2) # Calls StartStop function.      
        
    #TYPE, ext = 'r', 'png' # Image type.       
    Width = (XStop - XStart) * Size # Width of the image. 
    Height = (YStop - YStart) * Size # Hieght of the image.
    result = Image.new("RGB", (Width, Height)) # Sets up image dimensions.

    for x in range(XStart, XStop):                          
        for y in range(YStart, YStop):        
            
            if x in List1 and y in List2:                                       
                FullPath = InputPath + "//"  # Establishes where to read the tiles from.
                FileName = FullPath + "tile_" + format(x) + "_" + format(y) + ".png" # Looks for each individual tile by name.            
                            
                if not os.path.exists(FileName): # Deals with missing tiles.
                    continue           
                                          
                x_paste = (x - XStart) * Size # Finds where to paste.
                y_paste = Height - (YStop - y) * Size # Finds where to paste.
                            
                try:
                    i = Image.open(FileName)
                except Exception as e:
                    print ("-- %s, removing %s" % (e, FileName))
                    trash_dst = os.path.expanduser("~/.Trash/%s" % FileName)
                    os.rename(FileName, trash_dst)
                    continue
                
                result.paste(i, (x_paste, y_paste)) # Combines the images. 
                
                del i
            
    #result.show() #for debugging
    
    MapName = OutpathPath +format(Name) + ".jpg"    
    result.save(MapName) # Save based on name and resolution. 
 
def NumberOfOutputsCaluclator(TileSize): # Finds how many times the full image needs to be split to be a useable size.
    if TileSize == 10:
        Outputs = 1
    if TileSize > 10 <= 40:
        Outputs = 4    
    if TileSize == 50:
        Outputs = 9       
    else:
        print("Tiles are too big to process.")
    return(Outputs)  
       
def StartStop(List): # Finds Maximum and Minimum tile numbers. 
    Start = min(List) # Finds the Minimum value.
    Stop = max(List) # Finds the Maximum value. 
    return(Start, Stop)

def TileProcessor(Outputs, Size):  # Finds the tiles and creates a list of X and Y values, send those lists to be merged.
    XList = []  # Creates a list of the X's.
    YList = []  # Creates a list of the Y's.
    
    Tiles = os.listdir(InputPath) # Gets a list of all the Tiles.     
    for Tile in Tiles:
        TheFileName, TheFileExtension = os.path.splitext(Tile) # Breaks the file name into pieces based on periods. 
        tile, X, Y = os.path.basename(TheFileName).split("_") # Breaks the filename into pieces based on underscores.        
        XInt = int(X) # Turns X values into integers for sorting purposes. 
        YInt = int(Y) # Turns Y values into integers for sorting purposes.            
        XList.append(XInt) # Adds the X to the XList.
        YList.append(YInt) # Adds the Y to the YList.
    
    if Outputs == 1:
        MergeTiles(XList, YList, Size, "Salem_Samll")        
        
    if Outputs == 4:    
        XListA, XListB, XListC  = ListDividerTwo(XList)    
        YListA, YListB, YListC = ListDividerTwo(YList)   
        
        MergeTiles(XListA, YListA, Size, "1_North_West") # Calls the function which creates the image.
        MergeTiles(XListA, YListB, Size, "3_South_West") # Calls the function which creates the image. 
        
        MergeTiles(XListB, YListA, Size, "2_North_East") # Calls the function which creates the image.   
        MergeTiles(XListB, YListB, Size, "4_South_East") # Calls the function which creates the image.           
    
    if Outputs == 9:
        XListA, XListB, XListC  = ListDividerThree(XList)    
        YListA, YListB, YListC = ListDividerThree(YList)
        
        MergeTiles(XListA, YListA, Size, "1_North_West") # Calls the function which creates the image.
        MergeTiles(XListA, YListB, Size, "4_Center_West") # Calls the function which creates the image. 
        MergeTiles(XListA, YListC, Size, "7_South_West") # Calls the function which creates the image. 
        
        MergeTiles(XListB, YListA, Size, "2_North_Center") # Calls the function which creates the image.   
        MergeTiles(XListB, YListB, Size, "5_Center_Center") # Calls the function which creates the image.      
        MergeTiles(XListB, YListC, Size, "8_South_Center") # Calls the function which creates the image.      
        
        MergeTiles(XListC, YListA, Size, "3_North_East") # Calls the function which creates the image.   
        MergeTiles(XListC, YListB, Size, "6_Center_East") # Calls the function which creates the image.     
        MergeTiles(XListC, YListB, Size, "9_South_East") # Calls the function which creates the image.            
   
#############################################

from PIL import Image
import numpy as np
import os

ProjectPath = os.path.dirname(os.path.abspath(__file__)) # Finds the path of the current file. 
InputPath = ProjectPath+"/resizedtiles/"  # Sets where the inputs are stored.  
OutpathPath = ProjectPath+"/outputimages/"  # Sets where the outputs will be stored.  

#############################################

Manual = 0 # Use 0 to automatically find tile size, or 1 to use a manually input tile size.
TileSize = 50 # Tile Size
NumberOfOutputs = 4

BeginningProcess(Manual, TileSize, NumberOfOutputs)
print("complete")