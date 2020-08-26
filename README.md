### Note To Potential Employers
You may be looking at this script as you review my application, and yes this is just a script for a game, but there is still a lot you can learn from this. First it shows you that I am coding in my free time. Which says I am passionate and self-motivated. Secondly, this script deals with batch processing of images and merging large  datasets, both of which I am sure are relevent skills to the position I applied for. 

# Salem Tile Stitcher
Salem Map Tool, available https://github.com/dymm2000/salem-map-tool seems to work well for merging and exporting saved map tiles but fails when trying to stitch tiles together into a combined single image. This Tool reads in the numbered tiles from Salem Map Tool and exports them to a single jpg with a user determined resolution. 

## Prerequisites
You will need a custom Salem client which saves map tiles such as Taipion's found here http://forum.salemthegame.com/viewtopic.php?f=11&t=20661 Those tiles must be merged and exported using the Salem Map Tool. This will create a folder of possibly thousands of 100px x 100px individual tiles. These tiles will have their map positions coded in x y coordinates in the image title, starting with 0_0 tile. This must be run with a python 64bit executable, otherwise it will run into memory issues. Tiles must be already downsized to 10 - 70 px.

## Version 3.2
In 3.0 I revereted back to a pure python script. In 3.2 I completely rewrote the resizing function to rename all the tiles to modern map tile naming conventions, Number Comma Number starting from 0 at the most North West position. The Stictcher script now can use this to split the images into equal parts rather than splitting based on number of tiles resulting in some not-quite-as-square-as-I'd-like images. 3.2 also fixes a couple of small errors, creates the output folders rather than requiring the user to make them, and switches to a 4 image sturcture for 50px tiles and adds 9x images for 60px and 70px tiles.

## How to Run
Put this script in the same folder that holds the rezized tiles folder. The default is set to automatically find the tile size and figure out how many images it should output to avoid crashing, however this can be by-passed and manual input can be used.
