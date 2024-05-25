import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def removeOutliersZScore(data, col, tol):
    # Remove rows with score Nan
    data.dropna(subset=[col], inplace=True)

    # Get score list
    ages = [x for x in data[col].values if not np.isnan(x)]

    # Get Z-score
    z = np.abs(sp.stats.zscore(ages))

    # print(z)

    # Add Z-score to data
    data_with_z = data.copy()
    data_with_z['z'] = z

    # Get rows with Z-score > tol
    rows_to_drop = data_with_z[data_with_z['z'] > tol].index

    data.drop(rows_to_drop, inplace=True)

    return data
