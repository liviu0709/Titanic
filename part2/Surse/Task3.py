import pandas as pd

import sys
sys.path.append("../../")
import part1.surse.data_read

data = pd.read_csv("../Date/noOutliersModel.csv")

# Compare output data with the one from Part 1
part1.surse.data_read.survival_percentage(data, True)
part1.surse.data_read.histograms(data, "Age", True)
part1.surse.data_read.correlation(data, True)

# After comparing them, they look similar, but the data from Part 1 has no outliers, so the data is more accurate.