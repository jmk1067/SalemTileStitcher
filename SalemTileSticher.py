#############################################
# Salem Tile Stitcher v4.4.4
# Author:"pistolshrimp"
# jkennedy@humboldt.edu
# Date: 04/04/2022
#
#############################################

# This provides a number of ways to deal with large amounts of map files.
# Ultimately the aim is to stitch together tiles into more useable images.
# The tiles must be numbered correctly (ie merged) using the Salem Map Tool (https://github.com/dymm2000/salem-map-tool/releases)
# This must be run with a python 64bit executable, otherwise it will run into memory issues.
# Merged tiles must be in a folder named "maptiles".
# Put this script in the same folder as the maptiles folder.

#############################################

ScalesList = [100] # Add output pixel sizes here, seperated by a comma if there is more than one.
DesiredProcesses = [5] # Leaving empty will assume the process you need. Enter numbers, seperated by a comma, if finer control is needed.

"""
0   If this is your first time running the program or if you need to fix the map numbering.
1   To break.
2   To tare.
3   To unbreak.
4   To resize.
5   To stitch.
6   To caluculate percent of total.
"""

#############################################

# Common Functions.

#############################################

def AbsFinder(ZipList):
    Difference1 = (ZipList[0])
    Difference2 = (ZipList[1])
    return(Difference1, Difference2)


def BaseMinMax(List): # Creates a list of all potential tiles.
    Start = list(map(min, zip(*List))) # Finds miniumum X and Y tuple.
    End = list(map(max, zip(*List))) # Finds maximum X and Y tuple.
    MinX, MinY = AbsFinder(Start)
    MaxX, MaxY = AbsFinder(End)
    XList = [x for x in range(MinX, (MaxX+1))] # Create list of all potential Xs.
    YList = [x for x in range(MinY, (MaxY+1))] # Create list of all potential Ys.
    return(XList, YList)


def BaseXYListMaker(TilePath):
    Tiles = os.listdir(TilePath) # Gets a list of all the Tiles.
    XYList = [(int((os.path.splitext(Tile)[0]).split("_")[1]), int((os.path.splitext(Tile)[0]).split("_")[2])) for Tile in Tiles]
    return(XYList)


def BaseXYSorter(XYList):
    ListPreSorted = sorted(XYList, key=lambda x: x[0]) # Sort the XYList by X.
    ListSorted = sorted(ListPreSorted, key=lambda x: x[1]) # Sort the newly sorted XYList by Y.
    return(ListSorted)


def FolderMaker (Folder): # Checks to see if a folder exists, if it does not it makes it.
    Check = os.path.isdir(Folder) # Checks to see if that location already exists.
    if Check == True:
        pass
    else:
        os.mkdir(Folder) # Makes the folder.

def ListProcessor(Folder): # Holder function for common list processing functions.
    XYList = BaseXYListMaker(Folder)
    SortedList = BaseXYSorter(XYList)
    XList, YList = BaseMinMax(SortedList)
    return(XList, YList)

def SplitList(List): # Splits the lists.
    Halves = (len(List)//2)
    return (List[:Halves], List[Halves:])


#############################################

# Functions that handle other functions.

#############################################

def AutoProcess():
    if os.path.isfile(MapTilesPath):
        SalemMapBreaker()
    else:
        SalemTileTarer()
        SalemTileUnbreaker()
        SalemTileResizer()
        SalemTileStitcher()
        PercentofTotal()


def Debug(DesiredProcesses):
    FunctionList = [FirstBreak, SalemMapBreaker, SalemTileTarer, SalemTileUnbreaker, SalemTileResizer,  SalemTileStitcher, PercentofTotal]
    for Process in DesiredProcesses:
        FunctionList[Process]()


def PercentofTotal(): # Returns the percent of total tiles possible.
    Files = os.listdir(MapTilesPath)
    Have = len(Files)
    Percent = round(((Have/562490)*100),2) # 562490 = max tiles inside NWS map.
    print(format(Percent) + "%")


#############################################

# Salem Map Breaker v4.11
# Breaks the map tiles into 4 seperate folders.

#############################################

def SalemMapBreaker(): # Finds the tiles and creates a list of X and Y values.
    DirectionsList = ["NW", "NE", "SW", "SE"]
    print("Beginning map breaking...")
    XList, YList = ListProcessor(MapTilesPath)
    ZeroTileBackUp(0, 0)
    TileMoverHolder(XList, YList, DirectionsList)
    os.rename(MapTilesPath, ProjectPath+"/SE/")
    CommonTileMaker(0, 0, DirectionsList)
    print("Break complete...")


def CommonTileMaker(X, Y, DirectionsList): # Creates a place holder 0_0 tile.
    Image = np.zeros((100, 100, 3), np.uint8)
    Color = (90, 245, 17)
    Image[:] = Color
    Tally = 0
    while Tally < 4:
        Corner = DirectionsList[Tally]
        cv2.imwrite(BasePath+Corner+"/tile_" +format(X) + "_" +format(Y) + ".png", Image)
        Tally +=1


def FirstBreak(): # Fixes map tiles to be to have x,ys based on a center 0_0 tile.
    print("Beginning map breaking...")
    XList, YList = ListProcessor(MapTilesPath)
    MidX = XList[len(XList)//2] # Perdicted center X value.
    MidY = YList[len(YList)//2] # Perdicted center Y value.
    ZeroTileBackUp(MidX, MidY)
    TileMoverHolder(XList, YList)
    CommonTileMaker(MidX, MidY) # The center tile becomes the new 0_0 tile.
    SalemTileTarer()
    DirectionsList = ["NW", "NE", "SW", "SE"]
    Tally = 0
    while Tally < 4:
        InFolder = BasePath+DirectionsList[Tally]+ "2/" 
        os.rename(InFolder, BasePath+DirectionsList[Tally]) # Rename the folders to be used later.
        Tally +=1
    print("Break complete...")


def TileMover(List1, List2, Corner): # Finds the Actual tiles and copies them to their new folders.
    OutputFolder = ProjectPath+"/"+Corner+"/"
    FolderMaker(OutputFolder)
    for x in List1:
        for y in List2:
            try:
                Name = "tile_" + format(x) + "_" + format(y) + ".png"
                Source = MapTilesPath + Name
                Destination = OutputFolder + Name
                shutil.move(Source, Destination)
            except:
                continue


def TileMoverHolder(XList, YList, DirectionsList): # Holds common TileMover functions together for clairity.
    XListA, XListB  = SplitList(XList)
    YListA, YListB  = SplitList(YList)
    TileMover(XListA, YListA, DirectionsList[0])
    TileMover(XListB, YListA, DirectionsList[1])
    TileMover(XListA, YListB, DirectionsList[2])
    #TileMover(XListB, YListB, DirectionsList[3]) # As only SE tile remain SalemMapBreaker function instead renames the maptiles folder.


def ZeroTileBackUp(X, Y): # Saves the 0_0, if it exists, so it doesn't get written over by the common tile.
    FolderMaker(CommonTileBackupPath)
    try:
        shutil.move(MapTilesPath+"/tile_" +format(X) + "_" +format(Y) + ".png", CommonTileBackupPath+"tile_0_0.png")
    except:
        pass


#############################################

# Salem Tile Tarer v3.01
# This script re-orients the tiles around the common green tile after the tiles have been edited in another progam. 

#############################################

def SalemTileTarer(): # Reads in each direction folder, finds the place holder tile and uses that as the new 0_0 tile.
    DirectionsList = ["NW", "NE", "SW", "SE"]
    Tally = 0
    while Tally < 4:
        Direction = DirectionsList[Tally]
        print("Taring "+format(Direction)+"...")
        DirectionFolder = BasePath+Direction+"/"
        Check = CommonTileChecker(DirectionFolder+"tile_0_0.png")
        if Check == 1:
            os.rename(DirectionFolder, BasePath+Direction+"2") # Rename folder if no tiles have been added.
        else:
            CommonTileFinder(DirectionFolder, Direction)
            shutil.rmtree(DirectionFolder)
        Tally +=1
    print("Tare complete.")


def CommonTileFinder(DirectionFolder, Direction): # Finds the common tile and uses it to tare the rest of the tile.
    Sizes = [(os.stat(os.path.join(DirectionFolder, File)).st_size, os.path.join(DirectionFolder, File)) 
             for File in os.listdir(DirectionFolder)] # List of tiles and their size.
    CommonTile = sorted(Sizes, key=lambda x: x[0])[0] # Finds lowest file size.
    Check = CommonTileChecker(CommonTile[1])
    if Check == 1:
        XDifference, YDifference = TareFinder(CommonTile[1])
        RenameAndMove(Sizes, XDifference, YDifference, DirectionFolder, Direction)
    else:
        print("Cannot find the common tile.")
        exit()


def CommonTileChecker(TilePath): # Double checks the common tile.
    try:
        Input = Image.open(TilePath)
    except:
        return(0)
    Pixel = Input.crop((99, 99, 100, 100))
    Color = Image.Image.getcolors(Pixel)
    if Color == [(1, (17, 245, 90))]:
        #print(TilePath) # For debugging.
        return(1)
    else:
        return(0)

def RenameAndMove(Tiles, XDifference, YDifference, DirectionFolder, Direction): # Renames the tiles based on distance from placeholder tile.
    OutPath = BasePath+Direction+"2/"
    FolderMaker(OutPath)
    for Tile in Tiles:
        TheFileName, TheFileExtension = os.path.splitext(Tile[1]) # Breaks the file name into pieces based on periods.
        Z, X, Y = os.path.basename(TheFileName).split("_") # Breaks the filename into pieces based on underscores.
        NewName = OutPath + "tile_" +format(int(X)-XDifference)+"_"+format(int(Y)-YDifference) + ".png"
        shutil.move(Tile[1], NewName)


def TareFinder(CommonTile): # Finds the differences betweem common tile's X,Y values and 0.
    TheFileName, TheFileExtension = os.path.splitext(CommonTile) # Breaks the file name into pieces based on periods.
    Z, X, Y = os.path.basename(TheFileName).split("_") # Breaks the filename into pieces based on underscores.
    XDifference = int(X) # Turns X values into integers for sorting purposes.
    YDifference = int(Y) # Turns Y values into integers for sorting purposes.
    return(XDifference, YDifference)


#############################################
# Salem Tile Unbreaker v2.41
# This script merges all formerly split tile folders back together, after edits have been made.

#############################################

def SalemTileUnbreaker():
    print("Beginning merge...")
    FolderMaker(MapTilesPath)
    DirectionsList = ["NW2", "NE2", "SW2", "SE2"]
    Tally = 0
    while Tally < 4:
        InFolder = BasePath+DirectionsList[Tally]+ "/"
        Tiles = os.listdir(InFolder)
        for Tile in Tiles:
            FullOutPath = os.path.join(MapTilesPath, Tile)
            shutil.move(InFolder+Tile, FullOutPath)
        os.rmdir(InFolder)
        Tally +=1
    CommonTileReplacer()
    print("Merge complete.")


def CommonTileReplacer():
    try:
        shutil.move(CommonTileBackupPath+"tile_0_0.png", MapTilesPath+"tile_0_0.png")
        os.remove(CommonTileBackupPath+"tile_0_0.png")
    except:
        os.remove(MapTilesPath+"tile_0_0.png")
        

#############################################
    
# Salem Tile Resizer v4.4
# This script resizing and renames Salem map tiles.
# This counts the tiles and compares to the total poosible.

#############################################

def SalemTileResizer():
    for Scale in ScalesList:
        print("Beginning sizing to " +format(Scale) + "px")
        OutpathPath = ProjectPath+"/resizedtiles"+format(Scale)+"/"
        FolderMaker(OutpathPath) # Make the output folder.
        TilesList = [(os.path.join(MapTilesPath, File), os.path.join(MapTilesPath, File).replace
                      (MapTilesPath, OutpathPath)) for File in os.listdir(MapTilesPath)] # List of tile input and output paths.
        Size = (Scale, Scale) # Sets the output width and height based on the scale. 
        for Tile in TilesList:
            InputImage = cv2.imread(Tile[0], cv2.IMREAD_UNCHANGED) # Reads in the tile.
            OutputImage = cv2.resize(InputImage, Size, interpolation = cv2.INTER_CUBIC) # Resize the tile.
            cv2.imwrite(Tile[1], OutputImage) # Saves the tile.
        print ("Sizing to " +format(Scale) +"px complete.")


#############################################
    
# Salem Tile Stitcher v4.4
# This script stitches together Salem map tiles into full images.

#############################################

def SalemTileStitcher():
    for TileSize in ScalesList:
        print("Stitching "+format(TileSize)+"x"+format(TileSize)+"px resolution map...")
        InPath = MapTilesPath
        XList, YList = ListProcessor(InPath)
        TileProcessor(XList, YList, TileSize, InPath)
        shutil.rmtree(InPath)
    print("All processes complete.")


def TileProcessor(XList, YList, Size, InPath):
    if Size > 50:
        MergeTiles(XList, YList, Size, InPath, "Salem_Samll")
    else:
        XListA, XListB  = SplitList(XList)
        YListA, YListB  = SplitList(YList)
        MergeTiles(XListA, YListA, Size, InPath, "1_North_West")
        MergeTiles(XListA, YListB, Size, InPath, "3_South_West")
        MergeTiles(XListB, YListA, Size, InPath, "2_North_East")
        MergeTiles(XListB, YListB, Size, InPath, "4_South_East")


def MergeTiles(XList, YList, Size, InPath, Name):  # Merges the tiles together and outputs the image.
    FolderMaker(ImagePath) # Make the output folder.
    XStart = XList[0]
    YStop = YList[-1]
    Width = len(XList) * Size # Width of the image.
    Height = len(YList) * Size # Hieght of the image.
    result = Image.new("RGB", (Width, Height)) # Sets up image dimensions.
    for X in XList: # Loop through Xs and Ys and paste them together.
        for Y in YList:
            FileName = InPath + "tile_"+format(X) + "_" + format(Y) + ".png" # Looks for each individual tile by name.
            if not os.path.exists(FileName): # Deals with missing tiles.
                continue
            x_paste = (X - XStart) * Size # Finds where to paste.
            y_paste = (Height - ((YStop - Y) * Size)) - Size # Finds where to paste.
            try:
                i = Image.open(FileName)
            except Exception as e:
                print ("-- %s, removing %s" % (e, FileName))
                trash_dst = os.path.expanduser("~/.Trash/%s" % FileName)
                os.rename(FileName, trash_dst)
                continue
            result.paste(i, (x_paste, y_paste)) # Combines the images.
            del i
    #result.show() # for debugging
    MapName = ImagePath +format(Name) + ".jpg"
    result.save(MapName) # Output image.


#############################################

from PIL import Image
import cv2
import numpy as np
import os
import shutil

#############################################

ProjectPath = os.path.dirname(os.path.abspath(__file__)) # Finds the path of the current file.
BasePath = ProjectPath+"/"
CommonTileBackupPath = ProjectPath+"/backup/"
MapTilesPath = ProjectPath+"/maptiles/"
ImagePath = ProjectPath+"/outputimages/"

#############################################

if not DesiredProcesses: # If empty list run autoprocess function.
    AutoProcess()
else:
    Debug(DesiredProcesses)
