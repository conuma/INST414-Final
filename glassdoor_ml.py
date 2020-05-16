# -*- coding: utf-8 -*-
"""
Created on Sat May 16 06:20:09 2020

@author: cathe
"""

import pandas as pd
import numpy as np

# load cleaned dataset
glassdoor = pd.read_csv("C:/Users/cathe/glassdoor_clean.csv", header=0)

glassdoor['rating'] = glassdoor['rating'].astype(int)

#Creating a dataset of predictors and target
X = glassdoor.iloc[:, 3:9].values #predictor dataset
y = glassdoor.iloc[:, 2].values #target dataset

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)


from sklearn.metrics import explained_variance_score,mean_absolute_error

from sklearn.ensemble import RandomForestRegressor
#Creating an instance of random forest regressor
rf_regressor = RandomForestRegressor(n_estimators = 100, random_state = 0)
rf_regressor.fit(X, y)
y_pred_rf=rf_regressor.predict(X_test)
print('Variance score: %.2f', explained_variance_score(y_test, y_pred_rf))
print('MAE score: %.2f', mean_absolute_error(y_test, y_pred_rf))