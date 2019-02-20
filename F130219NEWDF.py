import pandas as pd
import numpy as np
from sklearn.svm import SVR
from matplotlib import pyplot as plt
from Modul_ML.F17122018ML import F2020ML
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

#--- Load dataframe
path = 'D:/GitHub/GitTesis/SVR/R export/'
dframe = pd.read_csv(path + '200219_DbscanSamp_1.5_5.csv')
# colmn = ['Band_2','Band_3','Band_4','Band_5','Band_6','Band_7']
colmn = ['Band_2', 'Band_3', 'Band_4', 'Band_5', 'Band_6', 'Band_7', 'DEM', 'ASPECT_R', 'SLOPE_R']
trget = 'frci'
# trget = 'frci_5m'

dfx = pd.DataFrame(dframe, columns=colmn)
dfy = np.asarray(dframe[trget])

X_train, X_test, y_train, y_test = train_test_split(dfx, dfy, test_size = 0.3, random_state = 4)
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
clfSVR = SVR(kernel='rbf')
clfSVR.fit(X_train, y_train)
score = clfSVR.score(X_test, y_test)
y_pred = clfSVR.predict(X_test)

print(dframe.head())
print(F2020ML.F2020_RMSE(y_test, y_pred))
print(F2020ML.F2020_RSQRT(y_test, y_pred))
print(score, clfSVR)
