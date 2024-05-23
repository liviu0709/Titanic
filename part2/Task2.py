import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def removeOutliersZScore(data, col, tol):
    # Remove rows with score Nan
    data.dropna(subset=[colList[5]], inplace=True)

    # Get score list
    ages = [x for x in data[col].values if not np.isnan(x)]

    # Get Z-score
    z = np.abs(sp.stats.zscore(ages))

    print(z)

    # Add Z-score to data
    data_with_z = data.copy()
    data_with_z['z'] = z

    # Get rows with Z-score > tol
    rows_to_drop = data_with_z[data_with_z['z'] > tol].index

    data.drop(rows_to_drop, inplace=True)

    return data

data = pd.read_csv("../train.csv")

colList = data.columns

# Get data without outliers for age
data = removeOutliersZScore(data, colList[5], 3)

# Get data without outliers for fare
data = removeOutliersZScore(data, colList[9], 0.5)

# Get data without outliers for SibSp
data = removeOutliersZScore(data, colList[6], 2)

# Get data without outliers for Parch
data = removeOutliersZScore(data, colList[7], 2)

data.to_csv('noOutliersZ-Score.csv', index=False)
