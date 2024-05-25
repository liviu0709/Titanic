import PyQt5.QtWidgets as pq
import PyQt5.QtCore as pc
import PyQt5.QtGui as pg
import sys

import asyncio

import model





def handleBuild(checkBuild, checkNorm, app):
    features = []
    normalise = []
    for check in checkBuild:
        if check.isChecked():
            print(check.text())
            features.append(check.text())
    print("Normalising data:")
    for check in checkNorm:
        if check.isChecked():
            print(check.text())
            normalise.append(check.text())
    print("Building model...")
    model.buildModel(features, normalise)



# Init window
app = pq.QApplication(sys.argv)
screen = app.primaryScreen()
size = screen.size()
width = size.width()
height = size.height()
# Create a Qt widget, which will be our window.
window = pq.QMainWindow()

window.setWindowTitle("Pick model options!!!!")

primary_layout = pq.QVBoxLayout()

main_layout = pq.QHBoxLayout()

buttom = pq.QVBoxLayout()

right = pq.QVBoxLayout()
left = pq.QVBoxLayout()

main_layout.addLayout(left)
main_layout.addLayout(right)

primary_layout.addLayout(main_layout)
primary_layout.addLayout(buttom)

leftLabel = pq.QLabel("Choose the features to build the model with:")

left.addWidget(leftLabel)
features = ['Age', 'Fare', 'SibSp', 'Parch', 'Sex', 'Cabin', 'Embarked', 'Pclass']
checkBuild = []
# Add checkboxes for features
for feature in features:
    checkbox = pq.QCheckBox(feature)
    left.addWidget(checkbox)
    checkBuild.append(checkbox)

# Center them on layout
left.setAlignment(pc.Qt.AlignCenter)

rightLabel = pq.QLabel("Choose what data to normalise:")
right.addWidget(rightLabel)

checkNorm = []
normalise = ['Age', 'Fare', 'SibSp', 'Parch', 'Pclass', 'Cabin']
# Add checkboxes for what to normalise
for norm in normalise:
    checkbox = pq.QCheckBox(norm)
    right.addWidget(checkbox)
    checkNorm.append(checkbox)
# Center them on layout
right.setAlignment(pc.Qt.AlignCenter)

button = pq.QPushButton("Build model")
# button.setCheckable(True)
button.clicked.connect(lambda: handleBuild(checkBuild, checkNorm, app))
buttom.addWidget(button)

buttone = pq.QPushButton("Exit")
buttone.setCheckable(True)
buttone.clicked.connect(app.quit)
buttom.addWidget(buttone)

trollButton = pq.QPushButton("NO ESCAPE")
left.addWidget(trollButton)



layout = pq.QWidget()
layout.setLayout(primary_layout)
window.setCentralWidget(layout)

# Display window max size
window.showMaximized()
# Enable app
app.exec()