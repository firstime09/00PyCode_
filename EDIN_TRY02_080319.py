from __future__ import print_function, division
from sklearn.ensemble import RandomForestClassifier
from osgeo import gdal, gdal_array
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

gdal.UseExceptions()
gdal.AllRegister()
path = 'D:/00PyCode/00AllData/Test_Data_08032019/'
img_ds = gdal.Open(path + 'layerstack.TIF', gdal.GA_ReadOnly)
# roi_ds = gdal.Open('D:/00PyCode/00AllData/Test_Data_08032019/training/training.TIF', gdal.GA_ReadOnly)

img = np.zeros((img_ds.RasterYSize, img_ds.RasterXSize, img_ds.RasterCount),
               gdal_array.GDALTypeCodeToNumericTypeCode(img_ds.GetRasterBand(1).DataType))
# print(img)
for b in range(img.shape[2]):
    img[:, :, b] = img_ds.GetRasterBand(b + 1).ReadAsArray()

# roi = roi_ds.GetRasterBand(1).ReadAsArray().astype(np.uint8)

plt.subplot(121)
plt.imshow(img[:, :, 4], cmap = plt.cm.Greys_r)
plt.title('DATA LandSat')

plt.show()
