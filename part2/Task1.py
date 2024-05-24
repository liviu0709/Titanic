import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def RemoveOutliersInterquartile(data, col, negativeData):
    # Remove rows with score Nan
    data.dropna(subset=[col], inplace=True)

    # Get score list
    ages = [x for x in data[col].values if not np.isnan(x)]

    # Get IQR
    q3, q1 = np.percentile(ages, [75 ,25])
    iqr = q3 - q1

    # Get upper and lower bounds
    upper = q3 + 1.5 * iqr
    lower = q1 - 1.5 * iqr

    # Age < 0 makes no sense
    if lower < 0 and negativeData == 0:
        lower = 0

    # Get data without outliers for age
    data = data[(data[col] >= lower) & (data[col] <= upper)]

    return data
