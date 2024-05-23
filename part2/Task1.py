import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("../train.csv")

colList = data.columns

print(data[colList[5]].values)

# Get ages list
ages = [x for x in data[colList[5]].values if not np.isnan(x)]

# Get IQR
q3, q1 = np.percentile(ages, [75 ,25])
iqr = q3 - q1

# Get upper and lower bounds
print(q1 - 1.5 * iqr, q3 + 1.5 * iqr)

upper = q3 + 1.5 * iqr
lower = q1 - 1.5 * iqr

# Age < 0 makes no sense
if lower < 0 :
    lower = 0

# Get data without outliers for age
noAgeOutlier = data[(data[colList[5]] >= lower) & (data[colList[5]] <= upper)]

print(noAgeOutlier[colList[9]].values)

# Get fares list
fares = [x for x in data[colList[9]].values if not np.isnan(x)]

fares.sort()

print(fares)

# Get IQR
q3, q1 = np.percentile(fares, [75 ,25])

iqr = q3 - q1

# Get upper and lower bounds
print(q1 - 1.5 * iqr, q3 + 1.5 * iqr)

upper = q3 + 1.5 * iqr
lower = q1 - 1.5 * iqr

# Fares < 0 makes no sense
if lower < 0 :
    lower = 0

# Get data without outliers for fare
noFareOutlier = noAgeOutlier[(data[colList[9]] >= lower) & (data[colList[9]] <= upper)]

print(noFareOutlier[colList[9]])

# Get SibSp list
sibSp = [x for x in data[colList[6]].values if not np.isnan(x)]
sibSp.sort()
print(sibSp)

# Get IQR
q3, q1 = np.percentile(sibSp, [75 ,25])

iqr = q3 - q1

# Get upper and lower bounds
print(q1 - 1.5 * iqr, q3 + 1.5 * iqr)

upper = q3 + 1.5 * iqr
lower = q1 - 1.5 * iqr

# SibSp < 0 makes no sense
if lower < 0 :
    lower = 0

# Get data without outliers for SibSp
noSibSpOutlier = noFareOutlier[(data[colList[6]] >= lower) & (data[colList[6]] <= upper)]

print(noSibSpOutlier)

# Get Parch list
parch = [x for x in data[colList[7]].values if not np.isnan(x)]
parch.sort()
print(parch)

# Get IQR
q3, q1 = np.percentile(parch, [75 ,25])
print(np.unique(parch))
print(np.histogram(parch))
iqr = q3 - q1

# Get upper and lower bounds
print(q1 - 1.5 * iqr, q3 + 1.5 * iqr)
print(q1, q3, iqr)

upper = q3 + 1.5 * iqr
lower = q1 - 1.5 * iqr

# Parch < 0 makes no sense
if lower < 0 :
    lower = 0

# Get data without outliers for Parch
noParchOutlier = noSibSpOutlier[(data[colList[7]] >= lower) & (data[colList[7]] <= upper)]

print(noParchOutlier)

noParchOutlier.to_csv('noOutliers.csv', index=False)