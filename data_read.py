import pandas as pd
import matplotlib.pyplot as plt
import math
import re
import seaborn as sb
import data_read

def null_entries(data):
    print(data.isnull().sum(axis=0))

def dupe_indexes(data):
    dupe_index =[]
    for i in range(len(data.duplicated().axes[0])):
        if data.duplicated()[i]:
            dupe_index.append(i)
    print(dupe_index)

def statistics(data):
    # se putea folosi si data.info()
    print("Number of columns:", len(data.axes[1]))
    print("Number of rows:", len(data.axes[0]))
    print(data.dtypes)
    print("Null entries for every column:")
    null_entries(data)
    print("Indexes of duplicate lines:")
    dupe_indexes(data)


def survival_percentage(data):
    percentages = {}
    for col in ['Survived', 'Pclass', 'Sex']:
        perc = ((data[col].value_counts()/data[col].count())*100)
        for value in perc.keys():
            percentages[col+': '+str(value)] = perc[value]
    plt.scatter(percentages.keys(), percentages.values())
    plt.show()

def histograms(data):
    for header in data.keys():
        if data[header].dtype in ["int64", "float64"] and header != 'PassengerId':
            plt.hist(data[header])
            plt.xlabel(header)
            plt.ylabel("Number of Passengers")
            plt.show()

def null_statistics(data):
    nulls = data.isnull().sum(axis=0)
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

def age_statistics(data):
    children_data = data[(data['Age'] < 18)]
    adult_data = data[(data['Age'] > 18)]
    children_perc = len(children_data)/len(data)*100
    adult_perc = len(adult_data)/len(data)*100
    children_sv = ((children_data['Survived'].value_counts()/children_data['Survived'].count())*100)
    adult_sv = ((adult_data['Survived'].value_counts()/adult_data['Survived'].count())*100)
    legend = {}
    legend['Children'] = children_sv[1]
    legend['Adults'] = adult_sv[1]
    plt.bar(legend.keys(), legend.values())
    plt.ylabel("Survival Rate")
    plt.show()
    print("Percentage of children passengers:", children_perc)
    print("Percentage of adult passengers:", adult_perc)

def add_age_group(data):
    data['AgeGroup'] = data['Age'].apply(lambda x: x if math.isnan(x) else int(max(min((x - 1) // 20, 3), 0)))
    data['AgeGroup'] = data['AgeGroup'].astype('Int64')
    values = {}
    for i in range(4):
        values[i] = len(data[data['AgeGroup'] == i])
    plt.plot(values.keys(), values.values())
    plt.show()
    return data

def male_statistics(data):
    male_values = {}
    for i in range(4):
        male_values[i] = len(data[(data['Survived'] == 1) & (data['Sex'] == 'male') & (data['AgeGroup'] == i)])
    plt.plot(male_values.keys(), male_values.values())
    plt.ylabel("Number of surviving males")
    plt.xlabel("Age group")
    plt.show()


def fill_null_entries(data): # doar mediile supravietuitorilor / ale mortilor
    for i in [0, 1]:
        data.loc[(data['Survived'] == i) & (data['Age'].isnull()), 'Age'] = data[data['Survived'] == i]['Age'].mean()
        for label in ['Cabin', 'Embarked']:
            data.loc[(data['Survived'] == i) & (data[label].isnull()), label] = data[(data['Survived'] == i)][label].value_counts().keys()[0]
    return data


def check_title_gender(data):
    male_titles = ['Mr', 'Don', 'Rev', 'Sir', 'Count']
    female_titles = ['Mrs', 'Miss', 'Ms', 'Lady', 'Mlle', 'Countess', 'Dona']
    titles = {}
    for name in data['Name']:
        temp = re.findall(" [a-zA-Z]+\. ", name)
        if temp[0].strip(' .') not in titles.keys() and temp[0].strip(' .') in male_titles:
            temp_data = data[(data['Sex'] == 'male')]
            # print("temp stip:", temp[0].strip(' '))
            titles[temp[0].strip(' ')] = temp_data['Name'].str.contains(temp[0]).sum()
        else:
            if temp[0].strip(' .') not in titles.keys() and temp[0].strip(' .') in female_titles:
                temp_data = data[(data['Sex'] == 'female')]
                titles[temp[0].strip(' ')] = temp_data['Name'].str.contains(temp[0]).sum()
            else:
                titles[temp[0].strip(' ')] = data['Name'].str.contains(temp[0]).sum()
    plt.plot(titles.keys(), titles.values())
    plt.show()

# ----------------------------
# it's conspiracy theory time!
# ----------------------------
def correlation(data):
    split_data = data.copy()
    for header in split_data.axes[1]:
        if header not in ["Survived", "SibSp"]:
            split_data.drop(header, axis='columns', inplace=True)
    print(split_data.corr())
    print("Putem trage concluzia ca starea de celibat pe vas nu a influențat considerabil rata de supraviețuire.")
    aux_split_data = data.copy()
    for header in aux_split_data.axes[1]:
        if header not in ["Survived", "Fare", "Pclass"]:
            aux_split_data.drop(header, axis='columns', inplace=True)
    sb.catplot(aux_split_data.head(100), x='Pclass', y='Fare', col='Survived', kind='swarm', size=2)
    plt.show()
