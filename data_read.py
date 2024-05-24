import pandas as pd
import matplotlib.pyplot as plt
import math
import re

data = pd.read_csv("train.csv") # index_col="PassengerId"

male_titles = ['Mr', 'Don', 'Rev', 'Sir', 'Count']
female_titles = ['Mrs', 'Miss', 'Ms', 'Lady', 'Mlle', 'Countess', 'Dona']

# ------------------
# print various info
# ------------------
# col_num = len(data.axes[1])
# row_num = len(data.axes[0])
# print(data.dtypes)

# --------------
# print the data
# --------------
# print(data)

# -------------------------------------
# no of cols, dtype of cols, no of rows
# -------------------------------------
# data.info()

# ---------------------------------
# no of missing elems for every row
# ---------------------------------
# print(data.isnull().sum(axis=0))

# ------------------------
# index of duplicate lines
# ------------------------
# dupes = data.duplicated()
# dupe_index =[]
# for i in range(len(dupes.axes[0])):
#     if dupes[i]:
#         dupe_index.append(i)
# print(dupe_index)

# -----------------------
# percentage of survivors
# -----------------------
# percentages = {}
# for col in ['Survived', 'Pclass', 'Sex']:
#     perc = ((data[col].value_counts()/data[col].count())*100)
#     for value in perc.keys():
#         percentages[col+': '+str(value)] = perc[value]
# plt.scatter(percentages.keys(), percentages.values())
# plt.show()

# ------------------------------
# histograms for numeric columns
# ------------------------------
# for header in data.keys():
#     if data[header].dtype in ["int64", "float64"]:
#         # print(data[header])
#         plt.hist(data[header])
#         plt.xlabel(header)
#         plt.ylabel("Number of Passengers")
#         plt.show()

# --------------------------
# NaN elements for every col
# --------------------------
# nulls = data.isnull().sum(axis=0)
# for header in nulls.keys():
#     if nulls[header] != 0:
#         prop = (nulls[header]*100)/len(data[header])
#         print(header, "column has", nulls[header], "null values, which equals to", prop, "% of values.")
# print()
# for i in [0, 1]:
#     split_dataset=data[(data["Survived"] == i)]
#     nulls = split_dataset.isnull().sum(axis=0)
#     for header in nulls.keys():
#         if nulls[header] != 0:
#             prop = (nulls[header]*100)/len(split_dataset[header])
#             if i:
#                 print("Survivors'", header, "column has", nulls[header], "null values, which equals to", prop, "% of values.")
#             else:
#                 print("Deceased's", header, "column has", nulls[header], "null values, which equals to", prop, "% of values.")
# print()

# -------------------------------------------------
# splitting the dataset between children and adults
# -------------------------------------------------
# children_data = data[(data['Age'] < 18)]
# adult_data = data[(data['Age'] > 18)]

# children_perc = len(children_data)/len(data)*100
# adult_perc = len(adult_data)/len(data)*100

# children_sv = ((children_data['Survived'].value_counts()/children_data['Survived'].count())*100)
# adult_sv = ((adult_data['Survived'].value_counts()/adult_data['Survived'].count())*100)

# legend = {}
# legend['Children'] = children_sv[1]
# legend['Adults'] = adult_sv[1]

# plt.bar(legend.keys(), legend.values())
# plt.ylabel("Survival Rate")
# plt.show()

# print("Percentage of children passengers:", children_perc)
# print("Percentage of adult passengers:", adult_perc)

# ----------------------------------------
# splitting the dataset between age groups
# ----------------------------------------
# data['AgeGroup'] = data['Age'].apply(lambda x: x if math.isnan(x) else int(max(min((x - 1) // 20, 3), 0)))
# data['AgeGroup'] = data['AgeGroup'].astype('Int64')
# values = {}
# for i in range(4):
#     values[i] = len(data[data['AgeGroup'] == i])
# plt.plot(values.keys(), values.values())
# plt.show()

# -----------------------------------------
# any cishet woman's dream: finding all men
# -----------------------------------------
# male_values = {}
# for i in range(4):
#     male_values[i] = len(data[(data['Survived'] == 1) & (data['Sex'] == 'male') & (data['AgeGroup'] == i)])
# plt.plot(male_values.keys(), male_values.values())
# plt.ylabel("Number of surviving males")
# plt.xlabel("Age group")
# plt.show()

# ------------------------------------------------
# filling in the gaps (insert another sexist joke)
# ------------------------------------------------
mean_age = data['Age'].mean()
data['Age'] = data['Age'].fillna(mean_age)
for label in ['Cabin', 'Embarked']:
    data[label] = data[label].fillna(data[label].value_counts().keys()[0])   

# --------------------------
# it's time to be homophobic
# --------------------------
# titles = {}
# for name in data['Name']:
#     temp = re.findall(" [a-zA-Z]+\. ", name)
#     if temp[0].strip(' .') not in titles.keys() and temp[0].strip(' .') in male_titles:
#         temp_data = data[(data['Sex'] == 'male')]
#         # print("temp stip:", temp[0].strip(' '))
#         titles[temp[0].strip(' ')] = temp_data['Name'].str.contains(temp[0]).sum()
#     else:
#         if temp[0].strip(' .') not in titles.keys() and temp[0].strip(' .') in female_titles:
#             temp_data = data[(data['Sex'] == 'female')]
#             titles[temp[0].strip(' ')] = temp_data['Name'].str.contains(temp[0]).sum()
#         else:
#             titles[temp[0].strip(' ')] = data['Name'].str.contains(temp[0]).sum()
# plt.plot(titles.keys(), titles.values())
# plt.show()
