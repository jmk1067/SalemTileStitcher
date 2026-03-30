
"""
from osgeo import gdal


def gdalinfo_python(filepath):
    # Open the raster dataset
    ds = gdal.Open(filepath)

    if ds is None:
        print("Failed to open the dataset!")
        return

    # Basic information
    print(f"Driver: {ds.GetDriver().ShortName}/{ds.GetDriver().LongName}")
    print(f"Size is {ds.RasterXSize} x {ds.RasterYSize} x {ds.RasterCount}")

    # Georeferencing information
    geotransform = ds.GetGeoTransform()
    if geotransform:
        print(f"Origin = ({geotransform[0]}, {geotransform[3]})")
        print(f"Pixel Size = ({geotransform[1]}, {geotransform[5]})")

    # Projection information
    projection = ds.GetProjection()
    if projection:
        print(f"Projection is: {projection}")

    # Raster bands information
    for i in range(1, ds.RasterCount + 1):
        band = ds.GetRasterBand(i)
        print(f"Band {i} Type={gdal.GetDataTypeName(band.DataType)}")

        min_val, max_val, _, _ = band.GetStatistics(True, True)
        print(f"Min={min_val:.3f}, Max={max_val:.3f}")

        if band.GetOverviewCount() > 0:
            print(f"Overviews: {band.GetOverviewCount()}")

        if band.GetRasterColorTable():
            print(f"Color Table Found!")

    ds = None  # Close the dataset

# Usage
filepath = "C:/Users/jmk10/Downloads/saa.jpg"
gdalinfo_python(filepath)
"""

"""
# degrees to radians
def deg2rad(degrees):
    return math.pi*degrees/180.0
# radians to degrees
def rad2deg(radians):
    return 180.0*radians/math.pi

# Semi-axes of WGS-84 geoidal reference
WGS84_a = 6378137.0  # Major semiaxis [m]
WGS84_b = 6356752.3  # Minor semiaxis [m]

# Earth radius at a given latitude, according to the WGS-84 ellipsoid [m]
def WGS84EarthRadius(lat):
    # http://en.wikipedia.org/wiki/Earth_radius
    An = WGS84_a*WGS84_a * math.cos(lat)
    Bn = WGS84_b*WGS84_b * math.sin(lat)
    Ad = WGS84_a * math.cos(lat)
    Bd = WGS84_b * math.sin(lat)
    return math.sqrt( (An*An + Bn*Bn)/(Ad*Ad + Bd*Bd) )

# Bounding box surrounding the point at given coordinates,
# assuming local approximation of Earth surface as a sphere
# of radius given by WGS84
def boundingBox(latitudeInDegrees, longitudeInDegrees, halfSideInKm):
    lat = deg2rad(latitudeInDegrees)
    lon = deg2rad(longitudeInDegrees)
    halfSide = 1000*halfSideInKm

    # Radius of Earth at given latitude
    radius = WGS84EarthRadius(lat)
    # Radius of the parallel at given latitude
    pradius = radius*math.cos(lat)

    latMin = lat - halfSide/radius
    latMax = lat + halfSide/radius
    lonMin = lon - halfSide/pradius
    lonMax = lon + halfSide/pradius

    return (rad2deg(latMin), rad2deg(lonMin), rad2deg(latMax), rad2deg(lonMax))
"""
import os

import gdal2tiles
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal, osr




project_path = os.path.dirname(os.path.abspath(__file__))

source_path = project_path
src_filename = project_path+'/ne.jpg'
dst_filename = source_path+'/bluemarble1.jpg'
outfilemaybe = dst_filename
somefile = source_path+'/bluemarble2.vrt'

'''
# Opens source dataset
src_ds = gdal.Open(src_filename)
format = "JPEG"
driver = gdal.GetDriverByName(format)

# Open destination dataset
dst_ds = driver.CreateCopy(dst_filename, src_ds, 0)


# Specify raster location through geotransform array
# (uperleftx, scalex, skewx, uperlefty, skewy, scaley)
# Scale = size of one pixel in units of raster projection
# this example below assumes 100x100
gt = [41.5488053797, 1, 0, -72.7189359492, 0, 100]


# Set location
dst_ds.SetGeoTransform(gt)

# Get raster projection
epsg = 3857
srs = osr.SpatialReference()
srs.ImportFromEPSG(epsg)
dest_wkt = srs.ExportToWkt()

# Set projection
dst_ds.SetProjection(dest_wkt)

# Close files
dst_ds = None
src_ds = None
'''


gcps = [
    (0, 0, -71.47980833333334, 41.8246417),
    (5887,0, -71.40876111111112, 41.8262167),
    (5887,5327, -71.4073, 41.7763083),
    (0, 5327, -71.47818333333333, 41.7767194),
    ]
    
    
    

ds = gdal.Open(src_filename)
gdal.Translate(
    dst_filename,
    ds,
    outputSRS='EPSG:4326',
    GCPs=[gdal.GCP(x, y, 0, pixel, line) for (pixel, line, x, y) in gcps],
)






kwargs = {'format': 'VRT'}
this = gdal.Warp(somefile, outfilemaybe,  dstSRS = 'EPSG:4326', **kwargs)
del this




def create_tiles(source_path, destination_path):
    options = {'zoom': 16,'s_srs':'EPSG:4326', 'kml': "TRUE"}
    gdal2tiles.generate_tiles(source_path, destination_path, **options)
    
create_tiles(somefile, source_path)

#'srs': 'EPSG:4326
