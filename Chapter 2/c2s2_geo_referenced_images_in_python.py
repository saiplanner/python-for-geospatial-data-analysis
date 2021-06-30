# -*- coding: utf-8 -*-
"""C2S2 - Geo Referenced Images in Python.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aWQrfHJgxNxC8hAo-yQ0o8vgZhBpn73x

# Chapter 2 - Session 2
# Geo Referenced Images in Python

## Objectives
#### learn how to use python library call GDAL which is dedicated to geo referenced images handling and related function 

## Content
#### 1) Installation and Importing GDAL Library
#### 2) Reading Images using GDAL library
#### 3) Writing Images using GDAL library
#### 4) Working with folders (multiple file)

<hr>

In last exercise, we learn how to deal in matrixes in python. the missing link is, how to bring raster image such as GeoTIFF file to our python workspace as NumPy matrix. that we can use for further analysis. This Gap is filled by another library call GDAL.

GDAL (Geospatial Data Abstraction Library) is a computer software library for reading and writing raster and vector geospatial data formats. 

In this exercise, we will use GDAL library to read geo referenced TIFF image (GeoTIFF) to our python workspace as a NumPy matrix and run some operations on it

Eventhough, we use only GeoTIFF images for this exercise, GDAL library supports 100s of raster data formats. some of them are as follows

    TIFF
    JPEG, JPEG2000, PNG, GIF
    ArcInfo grids, Imagine
    ENVI, GRASS
    HDF4, HDF5
    and many more

# 1) Installation and Importing GDAL Library

First we have to install GDAL to the Python using pip3 command as below. with NumPy library we directly install from internet using pip3. but in case of GDAL version compatibility is sensitive. So first, we download the GDAL library and then install it using pip3 command

most of python libraries including GDAL can be downloaded from this link.

    https://www.lfd.uci.edu/~gohlke/pythonlibs/
    
now we go to GDAL section

    https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal
    
then download GDAL version which is compatible with python version and OS (32bit or 64bit)

since we are using python 3.6 and

if you have windows 64 bit OS, first download "GDAL‑2.3.3‑cp36‑cp36m‑win_amd64.whl" file, navigate to downloaded directory and install using pip3
    
    pip3 install GDAL‑2.3.3‑cp36‑cp36m‑win_amd64.wh
    
if you have windows 32 bit OS, first download "GDAL‑2.3.3‑cp36‑cp36m‑win32.whl" file, navigate to downloaded directory and install using pip3
    
    pip3 install GDAL‑2.3.3‑cp36‑cp36m‑win32.whl

or if you use Anaconda, you can use, Anaconda Navigator to install GDAL library

then we can import and access various functions from GDAL library to our python work space
"""

'''import gdal and numpy library'''

# import gdal
from osgeo import gdal
import numpy as np

"""# 1) Reading Images using GDAL library

In this example, we will read sample SRTM digital elevation data (DEM data) from USGS as GeoTIFF file which is most common geo referenced image file format
"""

'''now we can read a tiff file and get information about the image'''

img = gdal.Open('.//data//srtm_57_08_1.tif')

print(img.RasterXSize)
print(img.RasterYSize)
print(img.RasterCount)

print('\n---------------------\n')

print(img.GetProjection())

print('\n---------------------\n')

print(img.GetGeoTransform())

print('\n---------------------\n')

"""Note that, srtm_img.GetGeoTransform() contains 5 values, which are corresponding to geopraphic cordinates of image

    [0] : top left x
    [1] : w-e pixel resolution
    [2] : rotation, 0 if image is "north up"
    [3] : top left y
    [4] : rotation, 0 if image is "north up"
    [5] : n-s pixel resolution
"""

'''read band from imported image and band information'''

band = img.GetRasterBand(1) #index starts from 1

print(band.GetNoDataValue())

'''from band, we can read our data as numpy matrix that can be used for further analysis'''

mat_srtm = band.ReadAsArray(0, 0, img.RasterXSize, img.RasterYSize)

"""When we are reading data to a NumPy matrix, we pass 4 parameters to, which are corresponding to size of data chunk that we are reading

    ReadAsArray(<xoff>, <yoff>, <xsize>, <ysize>)
    
    xoff : starting image x cordinate
    yoff : starting image y cordinate
    xsize : width
    ysize : height
"""

'''get information about matrix'''

print(type(mat_srtm))
print(mat_srtm.dtype)
print(mat_srtm.shape)

print('\n---------------------\n')

print(np.max(mat_srtm))
print(np.min(mat_srtm))

"""### Putting all together, how to read image to a NumPy matrix which we can be used for analysis"""

#read image
img = gdal.Open('.//data//srtm_57_08_1.tif') 

# get band
band = img.GetRasterBand(1) 

#get numpy matrix
mat_srtm = band.ReadAsArray(0, 0, img.RasterXSize, img.RasterYSize)

"""# 3) Writing Images using GDAL library


"""

'''lets read the image again as a numpy file'''

img = gdal.Open('.//data//srtm_57_08_1.tif')
band = img.GetRasterBand(1)
mat_srtm = band.ReadAsArray(0, 0, 3001, 3001)

'''writing image to a file'''

# allocating space in hard drive
driver = gdal.GetDriverByName("GTiff")
outdata = driver.Create('out.tif', 3001, 3001, 1, gdal.GDT_UInt16)

# set image paramenters (imfrormation related to cordinates)
outdata.SetGeoTransform(img.GetGeoTransform())
outdata.SetProjection(img.GetProjection())

# write numpy matrix as new band and set no data value for the band
outdata.GetRasterBand(1).WriteArray(mat_srtm)
outdata.GetRasterBand(1).SetNoDataValue(band.GetNoDataValue())

# flush data from memory to harddrive 
outdata.FlushCache()
outdata=None

"""GDAL also have their own data type like NumPy, so we have to provide data type, when image is created. commonly used data type are as follows

    GDT_Unknown - Unknown or unspecified type
    GDT_Byte - Eight bit unsigned integer
    GDT_UInt16 - Sixteen bit unsigned integer
    GDT_Int16 - Sixteen bit signed integer
    GDT_UInt32 - Thirty two bit unsigned integer
    GDT_Int32 - Thirty two bit signed integer
    GDT_Float32 - Thirty two bit floating point
    GDT_Float64 - Sixty four bit floating point
    
in this case, we use GDT_UInt16 as our data type

### Exercise 1

Read ".//srtm//srtm_57_08_1.tif" image again and add 10.5 to image and write as float image

### Exercise 2

Read ".//srtm//srtm_57_08_1.tif" image again and convert pixel values units to Km and write back as float image (original image's pixel values unit were meters)

# 2) Working with folders (multiple file)

We can read all files path in a directory to a path list using "glob" library in python

Then we can use our knowledge of for loop go through each item in the list and perform operations for each image in the folder

This way, we can deal with any number of images. This is really helpful when we are automating process for large number of images
"""

import glob

fList = glob.glob(".\data\*.tif")
print(fList)

# create count variable to keep track of which file we are accessing
count = 0

#for loop to go through each image file
for fName in fList:
    print(fName)
    
    #Read Images
    img = gdal.Open('.//data//srtm_57_08_1.tif')
    band = img.GetRasterBand(1)
    mat_srtm = band.ReadAsArray(0, 0, 3001, 3001)

    #Making output file name
    output_file_name = 'out' + str(count) + '.tif'
    count = count + 1
    
    #Write Images
    driver = gdal.GetDriverByName("GTiff")
    outdata = driver.Create(output_file_name, 3001, 3001, 1, gdal.GDT_UInt16)
    outdata.SetGeoTransform(img.GetGeoTransform())
    outdata.SetProjection(img.GetProjection())
    outdata.GetRasterBand(1).WriteArray(mat_srtm)
    outdata.GetRasterBand(1).SetNoDataValue(band.GetNoDataValue())
    outdata.FlushCache()
    outdata=None

"""### Exercise 3

Read all images in "srtm folder" and add 10.5 to image and write as float image

### Exercise 4

Read all images in "srtm folder" and convert their units to Km from meters and write as separate file
"""

