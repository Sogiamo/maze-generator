import os

os.environ["QT_API"] = "PySide6"

from PySide6.QtWidgets import (QMainWindow, QHBoxLayout, QWidget, QVBoxLayout,
                               QSpinBox, QFormLayout, QPushButton, QMessageBox,
                               QLabel, QCheckBox)
from PySide6.QtCore import QSize

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from maze import Maze
from maze_generator import MazeGenerator
from plot_maze import draw_maze

import matplotlib as mpl
mpl.rcParams["savefig.dpi"] = 1000


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, layout="tight")
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

    def plot_maze(self, maze, start_end_visible=True):
        self.axes.clear()
        draw_maze(maze, self.axes, start_end_visible)
        self.draw_idle()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Maze Generator")
        self.setMinimumSize(QSize(500, 400))
        self.setMaximumSize(QSize(1200, 800))

        # left layout

        left_layout = QVBoxLayout()

        self.canvas = MplCanvas(self, width=5, height=4, dpi=200)

        toolbar = NavigationToolbar(self.canvas, self)

        left_layout.addWidget(toolbar)
        left_layout.addWidget(self.canvas)

        # Right Layout

        self.height_spin = self._make_spinbox(7, 500, 100)
        self.width_spin = self._make_spinbox(7, 500, 100)

        self.seed_spin = self._make_spinbox(0, 2_147_483_647, 42)

        start_end_info_layout = QHBoxLayout()
        start_end_info_layout.addWidget(QLabel("Height"))
        start_end_info_layout.addWidget(QLabel("Width"))

        self.start_height_spin = self._make_spinbox(0, self.height_spin.value() - 1, 0)
        self.start_width_spin = self._make_spinbox(0, self.width_spin.value() - 1, 0)

        start_layout = QHBoxLayout()
        start_layout.addWidget(self.start_height_spin)
        start_layout.addWidget(self.start_width_spin)

        self.end_height_spin = self._make_spinbox(0, self.height_spin.value() - 1, self.height_spin.value() - 1)
        self.end_width_spin = self._make_spinbox(0, self.width_spin.value() - 1, self.width_spin.value() - 1)

        end_layout = QHBoxLayout()
        end_layout.addWidget(self.end_height_spin)
        end_layout.addWidget(self.end_width_spin)

        self.show_start_end = QCheckBox()

        self.generate_button = QPushButton("Generate Maze")
        self.generate_button.released.connect(self.generate_and_show)

        form_layout = QFormLayout()
        form_layout.addRow("Height", self.height_spin)
        form_layout.addRow("Width", self.width_spin)
        form_layout.addRow("Info", start_end_info_layout)
        form_layout.addRow("Start", start_layout)
        form_layout.addRow("End", end_layout)
        form_layout.addRow("Seed", self.seed_spin)
        form_layout.addRow("Make start/end visible", self.show_start_end)

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
        self.height_spin.valueChanged.connect(self.update_spinbox_range)
        self.width_spin.valueChanged.connect(self.update_spinbox_range)

    def _make_spinbox(self, min, max, value):
        spinbox = QSpinBox()
        spinbox.setRange(min, max)
        spinbox.setValue(value)
        return spinbox

    def update_spinbox_range(self):
        self.end_height_spin.setRange(0, self.height_spin.value() - 1)
        self.end_width_spin.setRange(0, self.width_spin.value() - 1)

        self.start_height_spin.setRange(0, self.height_spin.value() - 1)
        self.start_width_spin.setRange(0, self.width_spin.value() - 1)

    def generate_and_show(self):
        shape = (self.height_spin.value(), self.width_spin.value())
        seed = self.seed_spin.value()
        start = (self.start_height_spin.value(), self.start_width_spin.value())
        end = (self.end_height_spin.value(), self.end_width_spin.value())
        maze_generator = MazeGenerator(seed)

        try:
            maze = maze_generator.generate_maze(shape, start, end)
        except (ValueError, RuntimeError) as error:
            QMessageBox.warning(self, "Could not generate maze", str(error))
            return
        maze.add_bounds()

        self.canvas.plot_maze(maze, self.show_start_end.isChecked())



