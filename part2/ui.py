import PyQt5.QtWidgets as pq
import PyQt5.QtCore as pc
import PyQt5.QtGui as pg
import sys

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

leftLabel = pq.QLabel("Choose what to build model with:")
rightLabel = pq.QLabel("Choose what data to normalise:")

left.addWidget(leftLabel)
right.addWidget(rightLabel)

button = pq.QPushButton("Exit")
button.setCheckable(True)
button.clicked.connect(app.quit)
buttom.addWidget(button)

trollButton = pq.QPushButton("NO ESCAPE")
left.addWidget(trollButton)



layout = pq.QWidget()
layout.setLayout(primary_layout)
window.setCentralWidget(layout)

# Display window max size
window.showMaximized()
# Enable app
app.exec()