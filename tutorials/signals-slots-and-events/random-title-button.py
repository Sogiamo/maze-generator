from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow
from PySide6.QtCore import QSize
import random
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.titles = [
            "What a nice day",
            "What a nice day",
            "I like pizza",
            "I like pizza",
            "Press more",
            "Something went wrong"
        ]
        self.setWindowTitle("Random Window")

        self.button = QPushButton("Button")
        self.button.released.connect(self.button_released)
        self.windowTitleChanged.connect(self.title_changed)

        self.setCentralWidget(self.button)

        self.setFixedSize(QSize(500, 400))

    def button_released(self):
        random_title = random.choice(self.titles)
        print(f"Setting New Title to: {random_title}")

        self.setWindowTitle(random_title)

    def title_changed(self):
        current_title = self.windowTitle()
        print(f"Title was changed to: {current_title}")

        if current_title == "Something went wrong":
            self.button.setDisabled(True)
            print("The button was disabled")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()



