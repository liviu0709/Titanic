import scipy as sp
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation

from sklearn.tree import export_graphviz
from io import StringIO
from IPython.display import Image
import pydotplus

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import Task2
import Task1

import warnings
warnings.filterwarnings('ignore')

# Testing protocol:
# -> ../train.csv is the input file
#-> ../test.csv is the file to be used for testing

# Preprocessing -> load adata
data = pd.read_csv("../train.csv")

# To update by using Part 1 -> Task 8
toFill = ['Age', 'Fare', 'SibSp', 'Parch']
# Fill Nan with mean value
for column in toFill:
    data[column].fillna(data[column].mean(), inplace=True)

data['Cabin'] = data['Cabin'].fillna('C')

# Convert sex to numeric
# male -> 0
# female -> 1
# Convert embarked to numeric
# S -> 0
# C -> 1
for i in range(len(data)):
    if data.iloc[i, 4] == "male":
        data.iloc[i, 4] = 0
    else:
        data.iloc[i, 4] = 1
    if data.iloc[i, 11] == "S":
        data.iloc[i, 11] = 0
    elif data.iloc[i, 11] == "C":
        data.iloc[i, 11] = 1
    elif data.iloc[i, 11] == "Q":
        data.iloc[i, 11] = 0.5
    # Cabin -> ASCII code first letter
    data.iloc[i, 10] = ord(data.iloc[i, 10][0])

data.to_csv('filled.csv', index=False)

# Remove outliers using Task 1 and Task 2
# Depending on best accuracy, choose one of the two methods

# Get data without outliers for age
data = Task2.removeOutliersZScore(data, 'Age', 3)
# data = Task1.RemoveOutliersInterquartile(data, 'Age', 0)


# Get data without outliers for fare
# data = Task2.removeOutliersZScore(data, colList[9], 0.5)
data = Task1.RemoveOutliersInterquartile(data, 'Fare', 0)

# Get data without outliers for SibSp
data = Task2.removeOutliersZScore(data, 'SibSp', 2)
# data = Task1.RemoveOutliersInterquartile(data, 'SibSp', 0)

# Get data without outliers for Parch
data = Task2.removeOutliersZScore(data, 'Parch', 2)
# data = Task1.RemoveOutliersInterquartile(data, 'Parch', 0)

data.to_csv('NoOutliersModel.csv', index=False)

# TODO normalise Cabin
# cabins = data['Cabin'].unique()
# cabins.sort()
# print(cabins)

# data['Cabin'] = data['Cabin'].apply(lambda x: (x - cabins[0]) / (cabins[-1] - cabins[0]))

# cabins = data['Cabin'].unique()
# cabins.sort()
# print(cabins)

# Using cabin as a feature for the model does not improve accuracy

# Split dataset in features and target variable
feature_cols = ['Age', 'Pclass', 'Sex', 'Parch']
X = data[feature_cols] # Features
y = data['Survived'] # Target variable

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1) # 80% training and 20% test

# Create Decision Tree classifer object
clf = DecisionTreeClassifier()

# Train Decision Tree Classifer
clf = clf.fit(X_train,y_train)

#Predict the response for test dataset
y_pred = clf.predict(X_test)

# Model Accuracy, how often is the classifier correct?
print("Accuracy on 20% of training data no outliers:",metrics.accuracy_score(y_test, y_pred))

# Use this on test data

data = pd.read_csv("../test.csv")

# To update by using Part 1 -> Task 8
toFill = ['Age', 'Fare', 'SibSp', 'Parch']
# Fill Nan with mean value
for column in toFill:
    data[column].fillna(data[column].mean(), inplace=True)

data['Cabin'] = data['Cabin'].fillna('C')

for i in range(len(data)):
    if data.iloc[i, 3] == "male":
        data.iloc[i, 3] = 0
    else:
        data.iloc[i, 3] = 1
    if data.iloc[i, 10] == "S":
        data.iloc[i, 10] = 0
    elif data.iloc[i, 10] == "C":
        data.iloc[i, 10] = 1
    elif data.iloc[i, 10] == "Q":
        data.iloc[i, 10] = 0.5
    # Cabin -> ASCII code first letter
    data.iloc[i, 9] = ord(data.iloc[i, 9][0])

feature_cols = ['Age', 'Pclass', 'Sex', 'Parch']
X_test = data[feature_cols] # Features

data = pd.read_csv("../gender_submission.csv")

y_test = data['Survived'] # Target variable

# clf = clf.fit(X_train,y_train)

#Predict the response for test dataset
y_pred = clf.predict(X_test)

# Model Accuracy, how often is the classifier correct?
print("Accuracy on test data:",metrics.accuracy_score(y_test, y_pred))

dot_data = StringIO()
export_graphviz(clf, out_file=dot_data,
                filled=True, rounded=True,
                special_characters=True,feature_names = feature_cols,class_names=['0','1'])
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
graph.write_png('DecisionTree.png')
Image(graph.create_png())