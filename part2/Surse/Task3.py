import pandas as pd

import sys
sys.path.append("../../")
import data_read

data = pd.read_csv("../Date/noOutliersModel.csv")

# Compare output data with the one from Part 1
data_read.survival_percentage(data)
data_read.histograms(data)
data_read.null_statistics(data)
data_read.correlation(data)

# After comparing them, they look similar, but the data from Part 1 has no outliers, so the data is more accurate.