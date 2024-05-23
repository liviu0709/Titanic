import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("train.csv") # index_col="PassengerId"

# print various info
# ------------------
# col_num = len(data.axes[1])
# row_num = len(data.axes[0])
# print(data.dtypes)

# print the data
# --------------
# print(data)

# no of cols, dtype of cols, no of rows
# -------------------------------------
# data.info()

# no of missing elems for every row
# ---------------------------------
# print(data.isnull().sum(axis=0))

# index of duplicate lines
# ------------------------
# dupes = data.duplicated()
# dupe_index =[]
# for i in range(len(dupes.axes[0])):
#     if dupes[i]:
#         dupe_index.append(i)
# print(dupe_index)

# percentage of survivors
# -----------------------
# percentages = {}
# for col in ['Survived', 'Pclass', 'Sex']:
#     perc = ((data[col].value_counts()/data[col].count())*100)
#     for value in perc.keys():
#         percentages[col+': '+str(value)] = perc[value]
# plt.scatter(percentages.keys(), percentages.values())
# plt.show()

# histograms for numeric columns
# ------------------------------
# for header in data.keys():
#     if data[header].dtype in ["int64", "float64"]:
#         # print(data[header])
#         plt.hist(data[header])
#         plt.xlabel(header)
#         plt.ylabel("Number of Passengers")
#         plt.show()

# NaN elements for every col
# --------------------------
nulls = data.isnull().sum(axis=0)
# survive_count = data["Survived"].value_counts()
for header in nulls.keys():
    if nulls[header] != 0:
        prop = (nulls[header]*100)/len(data[header])
        print(header, "column has", nulls[header], "null values, which equals to", prop, "% of values.")
print()
for i in [0, 1]:
    split_dataset=data[(data["Survived"] == i)]
    nulls = split_dataset.isnull().sum(axis=0)
    for header in nulls.keys():
        if nulls[header] != 0:
            prop = (nulls[header]*100)/len(split_dataset[header])
            if i:
                print("Survivors'", header, "column has", nulls[header], "null values, which equals to", prop, "% of values.")
            else:
                print("Deceased's", header, "column has", nulls[header], "null values, which equals to", prop, "% of values.")