from PySide6.QtWidgets import QMainWindow, QPushButton, QApplication
from PySide6.QtCore import QSize, Qt

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Signals and sensors")
        self.setFixedSize(QSize(500, 400))

        self.button_is_toggled = True

        button = QPushButton("Press me and something happens")
        button.setCheckable(True)
        button.clicked.connect(self.button_clicked)
        button.released.connect(self.button_released)
        # button.clicked.connect(self.button_toggled)
        button.setChecked(self.button_is_toggled)
        self.setCentralWidget(button)

    def toggle_button(self, checked):
        self.button_is_toggled = checked

    def button_clicked(self):
        print("Button clicked")

    def button_released(self):
        print("Button released")

    def button_toggled(self, checked):
        print(f"Toggled? {checked}")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()