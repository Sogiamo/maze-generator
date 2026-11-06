import sys

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Press Button Exactly Once")

        self.count_clicks = 0
        self.button = QPushButton("Press Me Only Once")
        self.button.released.connect(self.button_pressed)

        self.setCentralWidget(self.button)
    def button_pressed(self):
        self.count_clicks += 1

        if self.count_clicks == 1:
            self.button.setText("Congrats, you clicked me exactly once!")
            self.setWindowTitle("One Press Master")
        else:
            self.button.setText("You are a loser X<")
            self.setWindowTitle("You disappointed us")
            self.button.setEnabled(False)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
