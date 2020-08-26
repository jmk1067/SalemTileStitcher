#############################################
# Salem Tile Resizer v2
# Author:"pistolshrimp"
# jkennedy@humboldt.edu
# Date: 08/26/2020
#
#############################################

# This script resizing and renames Salem map tiles.
# The tiles must be numbered correctly (ie merged) using the Salem Map Tool (https://github.com/dymm2000/salem-map-tool/releases)
# Put this script in the same folder that holds the tiles folder. 
# Merged tiles must be in a folder named "maptiles"

#############################################

def DifferenceFinder(List): # Finds the diffemce betweem lowest X,Y values and 0.
    Start = list(map(min, zip(*List))) # Finds miniumum X and Y tuple.
    XDifference=abs(Start[0]) # Lowest X
    YDifference=abs(Start[1]) # Lowest Y
    return(XDifference, YDifference)


def FolderMaker (): # Checks to see if a folder exists, if it does not it makes it.
    OutputFolder = ProjectPath+"/resizedtiles40/"
    Check = os.path.isdir(OutputFolder) # Checks to see if that location already exists.
    if Check == True:
        pass
    else:
        os.mkdir(OutputFolder) # Makes the folder.
    return(OutputFolder)


def RenameAndResize(XDifference, YDifference, List): #Resizes and renames and then Saves the tiles.
    OutpathPath = FolderMaker() # Make the output folder.
    for Tile in List:
        OldName = InputPath + "tile_" + format(Tile[0]) + "_" + format(Tile[1]) + ".png"
        NewName = OutpathPath + format(XDifference+Tile[0])+","+ format(YDifference+Tile[1]) + ".png"
        InputImage = cv2.imread(OldName, cv2.IMREAD_UNCHANGED) # Reads in the tile.
        Size = WidthAndHeight(InputImage) # Get the size of the new tile based on the defined Scale.
        OutputImage = cv2.resize(InputImage, Size) # Resize the tile.
        cv2.imwrite(NewName, OutputImage) # Saves the tile.


def XYListMaker():  # Finds the tiles and creates a list of X and Y values.
    Tiles = os.listdir(InputPath) # Gets a list of all the Tiles.
    XYList = [(int((os.path.splitext(Tile)[0]).split("_")[1]), int((os.path.splitext(Tile)[0]).split("_")[2])) for Tile in Tiles] # Messy list comprehenion, I'm sorry Proffesor Graham.
    ListPreSorted = sorted(XYList, key=lambda x: x[0]) # Sort the XYList by X.
    ListSorted = sorted(ListPreSorted, key=lambda x: x[1]) # Sort the newly sorted XYList by Y.

    XDifference, YDifference = DifferenceFinder(ListSorted) # Find the X,Y differences from 0 for renaming.
    RenameAndResize(XDifference, YDifference, XYList) # Send the list to be exported.


def WidthAndHeight(Image): # Get the size of the new tile based on the defined Scale.
        Width = int(Image.shape[1] * Scale / 100) # Divides Width by Scale.
        Height = int(Image.shape[0] * Scale / 100) # Divides Height by Scale.
        Size = (Width, Height)
        return(Size)

#############################################

import cv2
import os

#############################################

ProjectPath = os.path.dirname(os.path.abspath(__file__)) # Finds the path of the current file.
InputPath = ProjectPath+"/maptiles/"  # Sets where the inputs are stored.
Scale = 50

#############################################

print ("Beginning tile reszing...")
XYListMaker()
print ("Resizing complete.")