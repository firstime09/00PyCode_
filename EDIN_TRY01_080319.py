## The leasson from: https://github.com/ceholden/open-geo-tutorial
from __future__ import print_function, division
from sklearn.ensemble import RandomForestClassifier
from osgeo import gdal, gdal_array
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

gdal.UseExceptions()
gdal.AllRegister()
#----- First Step
# Read our image and ROI image from path, the data using LandSat 7
path = 'D:/00PyCode/open-geo-tutorial-master/example/'
img_ds = gdal.Open(path + 'LE70220491999322EDC01_stack.gtif', gdal.GA_ReadOnly)
roi_ds = gdal.Open(path + 'training_data.gtif', gdal.GA_ReadOnly)

img = np.zeros((img_ds.RasterYSize, img_ds.RasterXSize, img_ds.RasterCount),
               gdal_array.GDALTypeCodeToNumericTypeCode(img_ds.GetRasterBand(1).DataType))
for b in range(img.shape[2]):
    img[:, :, b] = img_ds.GetRasterBand(b + 1).ReadAsArray()

roi = roi_ds.GetRasterBand(1).ReadAsArray().astype(np.uint8)

# Display the picture
plt.subplot(121)
plt.imshow(img[:, :, 4], cmap = plt.cm.Greys_r)
plt.title('SWIR1')

plt.subplot(122)
plt.imshow(roi, cmap = plt.cm.Spectral)
plt.title('ROI Training Data')

plt.show()

#----- Second Step
# Find how many non-zero entries we have -- i.e. how many training data samples?
n_samples = (roi > 0).sum()
print('We have {n} samples'.format(n = n_samples))
# What are our classification labels?
labels = np.unique(roi[roi > 0])
print('The training data include {n} classes: {classes}'.format(n = labels.size, classes = labels))

# We need X as the features and y as a Labels from the data
X = img[roi > 0, :]
y = roi[roi > 0]
print('X Matrix: {sz}'.format(sz = X.shape))
print('y array: {sz}'.format(sz = y.shape))

#----- Third Step
# Make the Randomforest Classification model
rf = RandomForestClassifier(n_estimators=500, oob_score=True)
rf = rf.fit(X,y)
print('Score acc: {oob}%'.format(oob = rf.oob_score_ * 100))

band = [1, 2, 3, 4, 5, 7, 6]
for b, imp in zip(band, rf.feature_importances_):
    print('Band {b} Importance: {imp}'.format(b=b, imp=imp))

#----- Forth Step
# Make dataframe from our result of randomforest model
df = pd.DataFrame()
df['truth'] = y
df['predict'] = rf.predict(X)
# Cross-tabulates prediction
print(pd.crosstab(df['truth'], df['predict'], margins=True))