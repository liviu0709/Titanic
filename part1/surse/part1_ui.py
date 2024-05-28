import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import math
import re
import PyQt5.QtWidgets as pq
import PyQt5.QtCore as pc
import PyQt5.QtGui as pg

import data_read as dr

data = pd.read_csv("./../../train.csv")

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
                text_label.setPlainText(dr.statistics(self.data))
            case 1:
                self.setWindowTitle('Correlation')
                text_label.setPlainText(dr.correlation(self.data))
            case 2:
                self.setWindowTitle('Null Statistics')
                text_label.setPlainText(dr.null_statistics(self.data))
            case 3:
                self.setWindowTitle('Age Statistics')
                text_label.setPlainText(dr.age_statistics(self.data))
            case 4:
                self.setWindowTitle('Male statistics')
                text_label.setPlainText(dr.male_statistics(self.data))

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
        dr.histograms(self.data, header)
        plt.show(block=False)

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
        self.btn_survival_percentage.clicked.connect(lambda: dr.survival_percentage(data))
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
        self.btn_add_age_group.clicked.connect(lambda: dr.add_age_group(data))
        main_layout.addWidget(self.btn_add_age_group)

        self.btn_male_statistics = pq.QPushButton('Show Male Statistics', self)
        self.btn_male_statistics.clicked.connect(self.open_male_stat_window)
        main_layout.addWidget(self.btn_male_statistics)

        self.btn_fill_null_entries = pq.QPushButton('Fill Null Entries', self)
        self.btn_fill_null_entries.clicked.connect(lambda: dr.fill_null_entries(data))
        main_layout.addWidget(self.btn_fill_null_entries)

        self.btn_check_title_gender = pq.QPushButton('Check Title Gender', self)
        self.btn_check_title_gender.clicked.connect(lambda: dr.check_title_gender(data))
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
