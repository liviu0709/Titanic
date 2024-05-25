import scipy as sp
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn.preprocessing import MinMaxScaler
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation

from sklearn.tree import export_graphviz
from io import StringIO
from IPython.display import Image
import pydotplus

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np

import Task2
import Task1

# Adds parent directory to be able to import from it
import sys
sys.path.append("..")
import data_read

import warnings
# Warnings are never important !
warnings.filterwarnings('ignore')

def sexToNum(data, indexCrt):
    for i in range(len(data)):
        if data.iloc[i, indexCrt] == "male":
            data.iloc[i, indexCrt] = 0
        else:
            data.iloc[i, indexCrt] = 1
    return data

def embarkToNum(data, indexCrt):
    for i in range(len(data)):
        if data.iloc[i, indexCrt] == "S":
            data.iloc[i, indexCrt] = 0
        elif data.iloc[i, indexCrt] == "C":
            data.iloc[i, indexCrt] = 1
        elif data.iloc[i, indexCrt] == "Q":
            data.iloc[i, indexCrt] = 0.5
    return data

def normaliseColumns(data, columns):
    scaler = MinMaxScaler()
    for c in columns:
        data[c] = scaler.fit_transform(data[[c]])
    return data

# Convert whats down here to function depending on feature and normalise cols
# Also graphical interface

def buildModel(feature_cols, cols_normalise):
# DEPRECATED
# Columns to be used as features
# feature_cols = ['Age', 'Pclass', 'Sex', 'Fare']
# cols_normalise = ['Age', 'Fare']

    # Testing protocol:
    # -> ../train.csv is the input file
    #-> ../test.csv is the file to be used for testing

    # Preprocessing -> load adata
    data = pd.read_csv("../train.csv")


    # Using Part 1 -> Task 8
    data_read.fill_null_entries(data)

    # Convert sex to numeric
    # male -> 0
    # female -> 1
    # Convert embarked to numeric
    # S -> 0
    # C -> 1
    data = sexToNum(data, 4)
    data = embarkToNum(data, 11)

    data.to_csv('filled.csv', index=False)

    data = normaliseColumns(data, cols_normalise)

    # Remove outliers using Task 1 and Task 2
    # Depending on best accuracy, choose one of the two methods

    # Get data without outliers for age
    # data = Task2.removeOutliersZScore(data, 'Age', 3)
    data = Task1.RemoveOutliersInterquartile(data, 'Age', 0)


    # Get data without outliers for fare
    # data = Task2.removeOutliersZScore(data, colList[9], 0.5)
    data = Task1.RemoveOutliersInterquartile(data, 'Fare', 0)

    # Get data without outliers for SibSp
    data = Task2.removeOutliersZScore(data, 'SibSp', 2)
    # data = Task1.RemoveOutliersInterquartile(data, 'SibSp', 0)

    # Get data without outliers for Parch
    # data = Task2.removeOutliersZScore(data, 'Parch', 2)
    data = Task1.RemoveOutliersInterquartile(data, 'Parch', 0)

    data.to_csv('noOutliersModel.csv', index=False)

    # Split dataset in features and target variable
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
    print("Accuracy on 20% of training data no outliers:",metrics.accuracy_score(y_test, y_pred), metrics.log_loss(y_test, y_pred))

    # Use this on test data

    data = pd.read_csv("../test.csv")

    # Using Part 1 -> Task 8
    # data_read.fill_null_entries(data)
    # Cant fill data with mean of survived bcz no survived

    data = sexToNum(data, 3)
    data = embarkToNum(data, 10)

    data = normaliseColumns(data, cols_normalise)

    X_test = data[feature_cols] # Features

    data = pd.read_csv("../gender_submission.csv")

    y_test = data['Survived'] # Target variable

    # Predict the response for test dataset
    y_pred = clf.predict(X_test)

    # Model Accuracy, how often is the classifier correct?
    print("Accuracy on test data:",metrics.accuracy_score(y_test, y_pred), metrics.log_loss(y_test, y_pred))

    dot_data = StringIO()
    export_graphviz(clf, out_file=dot_data,
                    filled=True, rounded=True,
                    special_characters=True,feature_names = feature_cols,class_names=['0','1'])
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    graph.write_png('DecisionTree.png')
    Image(graph.create_png())

    importances = clf.feature_importances_
    features = X.columns

    print("Feature importances:", importances)
    print("Features:", features)

    # Convert to % for nice look
    importances = [x * 100 for x in importances]
    # Plot relevant graphs
    # importances vs features
    # Subplot -> 1 row, 2 columns, 1st plot
    plt.subplot(1, 2, 1)
    colors = ['red', 'black', 'green', 'blue', 'purple']
    plt.bar(features, importances, color=colors)
    plt.xlabel('Feature name')
    plt.ylabel('Importance (%)')
    plt.title('Feature importances')

    # Confusion matrix -> Compares true values with pred
    # Subplot -> 1 row, 2 columns, 2nd plot
    plt.subplot(1, 2, 2)
    # cmap -> color scheme
    # fmt -> format of the numbers
    sb.heatmap(metrics.confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Reds', xticklabels=['Nu a supraviețuit', 'A supraviețuit'], yticklabels=['Nu a supraviețuit', 'A supraviețuit'])
    plt.xlabel('Predicted')
    plt.xticks(rotation='horizontal')
    plt.ylabel('True')
    plt.title('Confusion matrix')
    # Block -> False -> No more error bcz app.exec PyQt5
    plt.show(block=False)

    # TODO ROC curve