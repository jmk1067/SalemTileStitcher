# Salem Tile Stitcher

Salem Map Tool, available https://github.com/dymm2000/salem-map-tool seems to work well for merging and exporting saved map tiles but fails when trying to stitch tiles together into a combined single image. This Tool reads in the numbered tiles from Salem Map Tool and exports them to a single jpg with a user determined resolution. 

## Prerequisites
You will need a custom Salem client which saves map tiles such as Taipion's found here http://forum.salemthegame.com/viewtopic.php?f=11&t=20661 Those tiles must be merged and exported using the Salem Map Tool. This will create a folder of possibly thousands of 100px x 100px individual tiles. These tiles will have their map positions coded in x y coordinates in the image title, starting with 0_0 tile. This must be run with a python 64bit executable, otherwise it will run into memory issues. Tiles must be already downsized to 10 - 50 px.

## Version 3.0
This version has reverted to a python script as maintaining a GUI for such a small project seems unproductive. In 2.0 this script output a single image, which at best was ill-convinced as the output was often un-openable by any image viewing programs, and at worst simply crashed attempting to force the computer to hold a massive image in memory. This version works with downsized tiles and further splits the image before sending it to memory and outputs multiple and more manageable images.

## How to Run
Put this script in the same folder that holds the rezized tiles folder. The default is set to automatically find the tile size and figure out how many images it should output to avoid crashing, however this can be by-passed and manual input can be used.
  
