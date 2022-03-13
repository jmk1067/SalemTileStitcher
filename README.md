### Note To Potential Employers
You may be looking at this script as you review my application, and yes this is just a script for a game, but there is still a lot you can learn from this. First it shows you that I am coding in my free time, which says I am passionate and self-motivated. Secondly, this script deals with batch processing of images and merging large  datasets, both of which I am sure are relevent skills to the position I applied for. 

# Salem Tile Stitcher
Salem Map Tool, available https://github.com/dymm2000/salem-map-tool seems to work well for merging and exporting saved map tiles but fails when trying to stitch tiles together into a combined single image. This Tool reads in the numbered tiles from Salem Map Tool and exports them to a single jpg, or if the map is too big, into 4x jpgs, with a user determined resolution. 

## Prerequisites
You will need a custom Salem client which saves map tiles such as Taipion's found here http://forum.salemthegame.com/viewtopic.php?f=11&t=20661 Those tiles must be merged and exported using the Salem Map Tool. This will create a folder of possibly thousands of 100px x 100px individual tiles. This must be run with a python 64bit executable, otherwise it will run into memory issues.

## Version 4.4
Added a default function to automatically choose what needs to be done to make program slightly more user friendly.
Found an area of redundancy where files were being moved where the folder could simply be renamed to the same affect. In theory breaking the map should be up to 25% faster. 
Small changes to the percentage function, namely added the ability to call the process seperately in the debugg controls.

## How to Run
Simply put this script in the same folder as the maptiles folder and run it. If it is your first time running the program add "0" to the DesiredProcess. 
