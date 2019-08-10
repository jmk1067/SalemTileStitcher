# Salem Tile Stitcher

Salem Map Tool, available https://github.com/dymm2000/salem-map-tool seems to work well for merging and exporting saved map tiles but fails when trying to stitch tiles together into a combined single image. This Tool reads in the numbered tiles from Salem Map Tool and exports them to a single jpg with a user determined resolution. 

## Prerequisites

You will need a custom Salem client which saves map tiles such as Taipion's found here http://forum.salemthegame.com/viewtopic.php?f=11&t=20661 Those tiles must be merged and exported using the Salem Map Tool. This will create a folder of possibly thousands of 100px x 100px individual tiles. These tiles will have their map positions coded in x y coordinates in the image title, starting with 0_0 tile. 

## How to Run
Open the exe and select a resolution for your finial image. The higher the resolution the larger the finial product, by the time you need this tool over Salem Map Tool's own export to image feature, your export will probably be in the hundreds of MBs at the highest resolution. Salem Tile Stitcher is set at a 25 default resolution.

After the resolution is set, select the folder with your merged files in it. You will know as it will contain a 0_0 tile. Hit Run and the progress bar will close when the image is finished saving. It will have a variable name based off the resolution you selected.
