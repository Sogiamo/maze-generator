import os

os.environ["QT_API"] = "PySide6"

from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QVBoxLayout, QSpinBox, QFormLayout, QPushButton, QMessageBox
from PySide6.QtCore import QSize

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from maze import Maze
from maze_generator import MazeGenerator
from plot_maze import draw_maze


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, layout="tight")
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

    def plot_maze(self, maze):
        self.axes.clear()
        draw_maze(maze, self.axes)
        self.draw_idle()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Maze Generator")
        self.setMinimumSize(QSize(500, 400))
        self.setMaximumSize(QSize(1200, 800))

        # left layout

        left_layout = QVBoxLayout()

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)

        toolbar = NavigationToolbar(self.canvas, self)

        left_layout.addWidget(toolbar)
        left_layout.addWidget(self.canvas)

        # Right Layout

        self.height_spin = self._make_spinbox(7, 500, 100)

        self.width_spin = self._make_spinbox(7, 500, 100)

        self.seed_spin = self._make_spinbox(0, 2_147_483_647, 42)

        self.generate_button = QPushButton("Generate Maze")
        self.generate_button.released.connect(self.generate_and_show)

        form_layout = QFormLayout()
        form_layout.addRow("Height", self.height_spin)
        form_layout.addRow("Width", self.width_spin)
        form_layout.addRow("Seed", self.seed_spin)

        right_layout = QVBoxLayout()
        right_layout.addLayout(form_layout)
        right_layout.addWidget(self.generate_button)

        # Main Layout
        layout = QHBoxLayout()
        layout.setSpacing(20)

        layout.addLayout(left_layout)
        layout.addLayout(right_layout)


        main_container = QWidget()

        main_container.setLayout(layout)

        self.setCentralWidget(main_container)

        self.generate_and_show()

    def _make_spinbox(self, min, max, value):
        spinbox = QSpinBox()
        spinbox.setRange(min, max)
        spinbox.setValue(value)
        return spinbox

    def generate_and_show(self):
        shape = (self.height_spin.value(), self.width_spin.value())
        seed = self.seed_spin.value()
        maze_generator = MazeGenerator(shape, seed)

        try:
            maze = maze_generator.generate_maze()
        except (ValueError, RuntimeError) as error:
            QMessageBox.warning(self, "Could not generate maze", str(error))
            return
        maze.add_bounds()

        self.canvas.plot_maze(maze)



