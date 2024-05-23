import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("train.csv") # index_col="PassengerId"

# col_num = len(data.axes[1])
# row_num = len(data.axes[0])
# print(data.dtypes)

# print the data
print(data)

# no of cols, dtype of cols, no of rows
data.info()

# no of missing elems for every row
print(data.isnull().sum(axis=0))

# index of duplicate lines
dupes = data.duplicated()
dupe_index =[]
for i in range(len(dupes.axes[0])):
    if dupes[i]:
        dupe_index.append(i)
print(dupe_index)

# percentage of survivors --- graficele sunt cel putin suspecte
percentages = {}
for col in ['Survived', 'Pclass', 'Sex']:
    perc = ((data[col].value_counts()/data[col].count())*100)
    # plt.plot(((data[col].value_counts()/data[col].count())*100))
    # plt.axis((0, data[col].nunique(), 0, 100))
    # plt.show()
    print(perc.dtype)
    for value in perc.keys():
        percentages[col+': '+str(value)] = perc[value]
        
# percentages graph
plt.scatter(percentages.keys(), percentages.values())
plt.show()


