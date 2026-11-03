from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My first app!")

        button = QPushButton("Push Me")

        # set fixed size of the widget in the middle (this makes button not in the middle
        # button.setFixedSize(QSize(400, 250))

        # set fixed size of the window to 1000 x 800
        # self.setFixedSize(QSize(1000, 800))

        # alternative to option above that allows resizing of the window
        self.setMinimumSize(QSize(500, 300))
        self.setMaximumSize(QSize(1200, 1000))

        # sets button as the central widget
        self.setCentralWidget(button)

app = QApplication(sys.argv)

window = MainWindow()
window.show()


app.exec()