import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import math
import re
import PyQt5.QtWidgets as pq
import PyQt5.QtCore as pc
import PyQt5.QtGui as pg

filepath = ''
data = pd.read_csv("train.csv") # index_col="PassengerId"

male_titles = ['Mr', 'Don', 'Rev', 'Sir', 'Count']
female_titles = ['Mrs', 'Miss', 'Ms', 'Lady', 'Mlle', 'Countess', 'Dona']

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

def histograms(data, header):
    plt.hist(data[header])
    plt.xlabel(header)
    plt.ylabel("Number of Passengers")
    plt.show()

def null_statistics(data):
    result = []
    nulls = data.isnull().sum(axis=0)
    for header in nulls.keys():
        if nulls[header] != 0:
            prop = (nulls[header]*100)/len(data[header])
            # print(header, "column has", nulls[header], "null values, which equals to", prop, "% of values.")
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
                    # print("Survivors'", header, "column has", nulls[header], "null values, which equals to", prop, "% of values.")
                else:
                    result.append(f"Deceased's {header} column has {nulls[header]}, null values, which equals to {prop}% of values.")
                    # print("Deceased's", header, "column has", nulls[header], "null values, which equals to", prop, "% of values.")
    print("\n".join(result))
    return "\n".join(result)

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
    result = []
    split_data = data.copy()
    for header in split_data.axes[1]:
        if header not in ["Survived", "SibSp"]:
            split_data.drop(header, axis='columns', inplace=True)
    result.append(str(split_data.corr()))
    result.append("Putem trage concluzia ca starea de celibat pe vas nu a influențat considerabil rata de supraviețuire.")
    aux_split_data = data.copy()
    for header in aux_split_data.axes[1]:
        if header not in ["Survived", "Fare", "Pclass"]:
            aux_split_data.drop(header, axis='columns', inplace=True)
    sb.catplot(aux_split_data.head(100), x='Pclass', y='Fare', col='Survived', kind='swarm', size=2)
    plt.show()
    return "\n".join(result)

class StatWindow(pq.QWidget):
    def __init__(self, data, code):
        super().__init__()
        self.data = data
        self.code = code
        self.initUI()

    def initUI(self):
        text_label = pq.QPlainTextEdit()
        main_layout = pq.QVBoxLayout()
        match self.code:
            case 0:
                self.setWindowTitle('General Statistics')
                text_label.setPlainText(statistics(self.data))
            case 1:
                self.setWindowTitle('Correlation')
                text_label.setPlainText(correlation(self.data))
            case 2:
                self.setWindowTitle('Null Statistics')
                text_label.setPlainText(null_statistics(self.data))
            case 3:
                self.setWindowTitle('Age Statistics')
                text_label.setPlainText(age_statistics(self.data))
            case 4:
                self.setWindowTitle('Male Statistics')
                text_label.setPlainText(male_statistics(self.data))

        text_label.setReadOnly(True)
        main_layout.addWidget(text_label)
        self.setLayout(main_layout)

class HistogramWindow(pq.QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Select Histogram')

        main_layout = pq.QVBoxLayout()

        self.combo = pq.QComboBox(self)
        numerical_headers = [header for header in self.data.columns if self.data[header].dtype in ["int64", "float64"]]
        numerical_headers.remove('PassengerId')
        self.combo.addItems(numerical_headers)
        main_layout.addWidget(self.combo)

        self.btn_show_histogram = pq.QPushButton('Show Histogram', self)
        self.btn_show_histogram.clicked.connect(self.show_histogram)
        main_layout.addWidget(self.btn_show_histogram)

        self.setLayout(main_layout)
        self.setGeometry(300, 300, 300, 200)

    def show_histogram(self):
        header = self.combo.currentText()
        histograms(self.data, header)
        plt.show()

class TitanicApp(pq.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Titanic Data Analysis')

        primary_layout = pq.QVBoxLayout()
        main_layout = pq.QHBoxLayout()

        self.btn_statistics = pq.QPushButton('Show Statistics', self)
        self.btn_statistics.clicked.connect(self.open_stat_window)
        main_layout.addWidget(self.btn_statistics)

        self.btn_survival_percentage = pq.QPushButton('Show Survival Percentage', self)
        self.btn_survival_percentage.clicked.connect(lambda: survival_percentage(data))
        main_layout.addWidget(self.btn_survival_percentage)

        self.btn_histograms = pq.QPushButton('Show Histograms', self)
        self.btn_histograms.clicked.connect(self.open_histogram_window)
        main_layout.addWidget(self.btn_histograms)

        self.btn_null_statistics = pq.QPushButton('Show Null Statistics', self)
        self.btn_null_statistics.clicked.connect(self.open_null_stat_window)
        main_layout.addWidget(self.btn_null_statistics)

        self.btn_age_statistics = pq.QPushButton('Show Age Statistics', self)
        self.btn_age_statistics.clicked.connect(self.open_age_stat_window)
        main_layout.addWidget(self.btn_age_statistics)

        self.btn_add_age_group = pq.QPushButton('Add Age Group and Show', self)
        self.btn_add_age_group.clicked.connect(lambda: add_age_group(data))
        main_layout.addWidget(self.btn_add_age_group)

        self.btn_male_statistics = pq.QPushButton('Show Male Statistics', self)
        self.btn_male_statistics.clicked.connect(self.open_male_stat_window)
        main_layout.addWidget(self.btn_male_statistics)

        self.btn_fill_null_entries = pq.QPushButton('Fill Null Entries', self)
        self.btn_fill_null_entries.clicked.connect(lambda: fill_null_entries(data))
        main_layout.addWidget(self.btn_fill_null_entries)

        self.btn_check_title_gender = pq.QPushButton('Check Title Gender', self)
        self.btn_check_title_gender.clicked.connect(lambda: check_title_gender(data))
        main_layout.addWidget(self.btn_check_title_gender)

        self.btn_correlation = pq.QPushButton('Show Correlation', self)
        self.btn_correlation.clicked.connect(self.open_correlation)
        main_layout.addWidget(self.btn_correlation)

        primary_layout.addLayout(main_layout)
        self.setLayout(primary_layout)
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def open_histogram_window(self):
        self.histogram_window = HistogramWindow(data)
        self.histogram_window.show()

    def open_correlation(self, code):
        code = 1
        self.stat_window = StatWindow(data, code)
        self.stat_window.show()

    def open_stat_window(self, code):
        code = 0
        self.stat_window = StatWindow(data, code)
        self.stat_window.show()

    def open_null_stat_window(self, code):
        code = 2
        self.stat_window = StatWindow(data, code)
        self.stat_window.show()

    def open_age_stat_window(self, code):
        code = 3
        self.stat_window = StatWindow(data, code)
        self.stat_window.show()

    def open_male_stat_window(self, code):
        code = 4
        self.stat_window = StatWindow(data, code)
        self.stat_window.show()

if __name__ == '__main__':
    app = pq.QApplication(sys.argv)
    ex = TitanicApp()
    sys.exit(app.exec_())