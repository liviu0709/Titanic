import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import math
import re

data = pd.read_csv("./../../train.csv")

male_titles = ['Mr', 'Don', 'Rev', 'Sir', 'Count']
female_titles = ['Mrs', 'Miss', 'Ms', 'Lady', 'Mlle', 'Countess', 'Dona']

def null_entries(data):
    return str(data.isnull().sum(axis=0))

def dupe_indexes(data):
    dupe_index =[]
    for i in range(len(data.duplicated().axes[0])):
        if data.duplicated()[i]:
            dupe_index.append(i)
    return " ".join(dupe_index)

def statistics(data): ## converted
    result = []
    result.append(f"Number of columns: {len(data.axes[1])}")
    result.append(f"Number of rows: {len(data.axes[0])}")
    result.append(str(data.dtypes))
    result.append("Null entries for every column:")
    result.append(null_entries(data))
    result.append("Indexes of duplicate lines:")
    result.append(dupe_indexes(data))
    return "\n".join(result)

def survival_percentage(data, pltShow=False): ## plot
    percentages = {}
    for col in ['Survived', 'Pclass', 'Sex']:
        perc = ((data[col].value_counts()/data[col].count())*100)
        for value in perc.keys():
            percentages[col+': '+str(value)] = perc[value]
    plt.bar(percentages.keys(), percentages.values())
    plt.ylabel("Percentage")
    plt.show(block=pltShow)

def histograms(data, header, pltShow=False): ## plot
    plt.hist(data[header])
    plt.xlabel(header)
    plt.ylabel("Number of Passengers")
    plt.show(block=pltShow)

def null_statistics(data): ## converted
    result = []
    nulls = data.isnull().sum(axis=0)
    for header in nulls.keys():
        if nulls[header] != 0:
            prop = (nulls[header]*100)/len(data[header])
            result.append(f"{header} column has {nulls[header]} null values, which equals to {prop}% of values.")
    for i in [0, 1]:
        result.append("")
        split_dataset=data[(data["Survived"] == i)]
        nulls = split_dataset.isnull().sum(axis=0)
        for header in nulls.keys():
            if nulls[header] != 0:
                prop = (nulls[header]*100)/len(split_dataset[header])
                if i:
                    result.append(f"Survivors' {header} column has {nulls[header]}, null values, which equals to {prop}% of values.")
                else:
                    result.append(f"Deceased's {header} column has {nulls[header]}, null values, which equals to {prop}% of values.")
    return "\n".join(result)

def age_statistics(data): ## converted
    result = []
    children_data = data[(data['Age'] < 18)]
    adult_data = data[(data['Age'] >= 18)]
    children_perc = len(children_data)/len(data)*100
    adult_perc = len(adult_data)/len(data)*100
    children_sv = ((children_data['Survived'].value_counts()/children_data['Survived'].count())*100)
    adult_sv = ((adult_data['Survived'].value_counts()/adult_data['Survived'].count())*100)
    legend = {}
    legend['Children'] = children_sv[1]
    legend['Adults'] = adult_sv[1]
    plt.bar(legend.keys(), legend.values())
    plt.ylabel("Survival Rate")
    plt.show(block=False)
    result.append(f"Percentage of children passengers: {children_perc}")
    result.append(f"Percentage of adult passengers: {adult_perc}")
    return "\n".join(result)

def add_age_group(data): ## plot
    data['AgeGroup'] = data['Age'].apply(lambda x: x if math.isnan(x) else int(max(min((x - 1) // 20, 3), 0)))
    data['AgeGroup'] = data['AgeGroup'].astype('Int64')
    values = {}
    for i in range(4):
        values[i] = len(data[data['AgeGroup'] == i])
    plt.plot(values.keys(), values.values())
    plt.xlabel("Age Group")
    plt.ylabel("Number of Passengers")
    plt.show(block=False)
    data.to_csv("./../date/age_group.csv", index=False)
    return data

def male_statistics(data): ## plot ---- add_age_group needs to be ran first
    male_values = {}
    try:
        data['AgeGroup']
    except:
        data['AgeGroup'] = data['Age'].apply(lambda x: x if math.isnan(x) else int(max(min((x - 1) // 20, 3), 0)))
        data['AgeGroup'] = data['AgeGroup'].astype('Int64')
    for i in range(4):
        male_values[i] = len(data[(data['Survived'] == 1) & (data['Sex'] == 'male') & (data['AgeGroup'] == i)]) / len(data[(data['Sex'] == 'male') & (data['AgeGroup'] == i)]) * 100
    plt.plot(male_values.keys(), male_values.values())
    plt.ylabel("Percentage of surviving males")
    plt.xlabel("Age group")
    plt.show(block=False)
    return str(data[(data['Survived'] == 1) & (data['Sex'] == 'male')]['AgeGroup'].value_counts())

def fill_null_entries(data): ## in place
    for i in [0, 1]:
        data.loc[(data['Survived'] == i) & (data['Age'].isnull()), 'Age'] = data[data['Survived'] == i]['Age'].mean()
        for label in ['Cabin', 'Embarked']:
            data.loc[(data['Survived'] == i) & (data[label].isnull()), label] = data[(data['Survived'] == i)][label].value_counts().keys()[0]
    # data.to_csv("./../date/filled_null.csv", index=False)
    return data

def check_title_gender(data): ## plot
    titles = {}
    for name in data['Name']:
        temp = re.findall(" [a-zA-Z]+\. ", name)
        if temp[0].strip(' .') not in titles.keys() and temp[0].strip(' .') in male_titles:
            temp_data = data[(data['Sex'] == 'male')]
            titles[temp[0].strip(' ')] = temp_data['Name'].str.contains(temp[0]).sum()
        else:
            if temp[0].strip(' .') not in titles.keys() and temp[0].strip(' .') in female_titles:
                temp_data = data[(data['Sex'] == 'female')]
                titles[temp[0].strip(' ')] = temp_data['Name'].str.contains(temp[0]).sum()
            else:
                titles[temp[0].strip(' ')] = data['Name'].str.contains(temp[0]).sum()
    plt.plot(titles.keys(), titles.values())
    plt.show(block=False)

# ----------------------------
# it's conspiracy theory time!
# ----------------------------
def correlation(data, pltShow=False): ## converted
    result = []
    split_data = data.copy()
    for header in split_data.axes[1]:
        if header not in ["Survived", "SibSp"]:
            split_data.drop(header, axis='columns', inplace=True)
    result.append(str(split_data.corr()))
    result.append("Putem trage concluzia ca starea de celibat pe vas nu a influențat considerabil rata de supraviețuire.")
    sb.catplot(data.head(100), x='Pclass', y='Fare', col='Survived', kind='swarm', size=2)
    plt.show(block=pltShow)
    return "\n".join(result)