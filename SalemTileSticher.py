#############################################
# Salem Tile Stitcher v3.2
# Author:"pistolshrimp"
# jkennedy@humboldt.edu
# Date: 08/26/2020
#
#############################################

# This script stitches together Salem map tiles.
# The tiles must be numbered correctly (ie merged) using the Salem Map Tool (https://github.com/dymm2000/salem-map-tool/releases)
# This must be run with a python 64bit executable, otherwise it will run into memory issues. 
# Requires tiles to be downsized to 10 - 70 px. 
# Put this script in the same folder that holds the rezized tiles folder. 

#############################################

def FolderMaker (): # Checks to see if a folder exists, if it does not it makes it.
    OutputFolder = ProjectPath+"/outputimages/"
    Check = os.path.isdir(OutputFolder) # Checks to see if that location already exists.
    if Check == True:
        pass
    else:
        os.mkdir(OutputFolder) # Makes the folder.
    return(OutputFolder)


def MergeTiles(List1, List2, Size, Name):  # Merges the tiles together and outputs the image.
    OutpathPath = FolderMaker() # Make the output folder.
    XStart, XStop, = StartStop(List1)
    YStart, YStop  = StartStop(List2)

    Width = (XStop - XStart) * Size # Width of the image.
    Height = (YStop - YStart) * Size # Hieght of the image.
    result = Image.new("RGB", (Width, Height)) # Sets up image dimensions.

    for x in range(XStart, XStop): # Loop through Xs and Ys and paste them together.
        for y in range(YStart, YStop):

            if x in List1 and y in List2:
                FileName = InputPath + format(x) + "," + format(y) + ".png" # Looks for each individual tile by name.

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
    result.save(MapName) #Output image.
 
def NumberOfOutputsCaluclator(TileSize): # Finds how many times the full image needs to be split to be a useable size.
    if TileSize < 11:
        Outputs = 1
    elif 10 > TileSize < 60:
        Outputs = 4
    elif 59 > TileSize < 71:
        Outputs = 9
    else:
        print("Tiles are too big to process.")
        exit()
    return(Outputs)


def ListDividerTwo(List): # Divides lists into 2 parts.
    List.sort()
    ListA = []
    ListB = []
    for Number in List:
        if Number < 376:
            ListA.append(Number) # Adds the X to the XList.
        else:
            ListB.append(Number)
    return(ListA, ListB)
        
        
def ListDividerThree(List): # Divides lists into 3 parts.
    List.sort()
    ListA = []
    ListB = []
    ListC = []
    for Number in List:
        if Number < 250:
            ListA.append(Number)
        elif 250 < Number < 500:
            ListB.append(Number)
        else:
            ListC.append(Number)
    return(ListA, ListB, ListC)
    
 
def StartMerge(Manual):
    XList, YList = XYListMaker()
    Tile = Image.open(InputPath + format(XList[0]) + "," + format(YList[0]) + ".png")
    TileSize, Height = Tile.size
    if Manual == 0:
        NumberOfOutputs = NumberOfOutputsCaluclator(TileSize)          
    else:
        NumberOfOutputs = Manual
    TileProcessor(XList, YList, NumberOfOutputs, TileSize)


def StartStop(List): # Finds Maximum and Minimum tile numbers.
    Start = min(List) # Finds the Minimum value.
    Stop = max(List) # Finds the Maximum value.
    return(Start, Stop)


def TileProcessor(XList, YList, Outputs, Size):  # Finds the tiles and creates a list of X and Y values, send those lists to be merged.
    if Outputs == 1:
        MergeTiles(XList, YList, Size, "Salem_Samll")      
    if Outputs == 4:        
        XListA, XListB = ListDividerTwo(XList)    
        YListA, YListB = ListDividerTwo(YList)

        MergeTiles(XListA, YListA, Size, "1_North_West")
        MergeTiles(XListA, YListB, Size, "3_South_West")

        MergeTiles(XListB, YListA, Size, "2_North_East")  
        MergeTiles(XListB, YListB, Size, "4_South_East")         

    if Outputs == 9:
        XListA, XListB, XListC  = ListDividerThree(XList)    
        YListA, YListB, YListC = ListDividerThree(YList)

        MergeTiles(XListA, YListA, Size, "1_North_West")
        MergeTiles(XListA, YListB, Size, "4_Center_West")
        MergeTiles(XListA, YListC, Size, "7_South_West")

        MergeTiles(XListB, YListA, Size, "2_North_Center") 
        MergeTiles(XListB, YListB, Size, "5_Center_Center")   
        MergeTiles(XListB, YListC, Size, "8_South_Center")

        MergeTiles(XListC, YListA, Size, "3_North_East")
        MergeTiles(XListC, YListB, Size, "6_Center_East")
        MergeTiles(XListC, YListC, Size, "9_South_East")


def XYListMaker(): # Creates a list of X and Y values from the tiles.
    XList = []  # Creates a list of the X's.
    YList = []  # Creates a list of the Y's.

    Tiles = os.listdir(InputPath) # Gets a list of all the Tiles.  
    for Tile in Tiles:
        TheFileName, TheFileExtension = os.path.splitext(Tile) # Breaks the file name into pieces based on periods.
        X, Y = os.path.basename(TheFileName).split(",") # Breaks the filename into pieces based on underscores.
        XInt = int(X) # Turns X values into integers for sorting purposes.
        YInt = int(Y) # Turns Y values into integers for sorting purposes.
        XList.append(XInt) # Adds the X to the XList.
        YList.append(YInt) # Adds the Y to the YList.
    return(XList, YList)
   
#############################################

from PIL import Image
import os

ProjectPath = os.path.dirname(os.path.abspath(__file__)) # Finds the path of the current file.
InputPath = ProjectPath+"/resizedtiles/" # Sets where the inputs are stored.

#############################################

print("Beginning merge...")
Manual = 0 # Use 0 to automatically find tile size, or input Number of Outputs if manual.
StartMerge(Manual)
print("Merge complete.")