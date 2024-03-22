from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout
from .Dartboard import *
from .Settings import *
from .Knockout import *
from .Foul import Foul

class ScorekeeperUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a Dartboard instance
        self.dartboard = Dartboard(clickable=True)
        self.knockout = Knockout()
        self.foul = Foul()
        self.settings = Settings()

        # Create a QHBoxLayout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.knockout, 1)
        button_layout.addWidget(self.foul, 1)

        # Create a QVBoxLayout to hold the Dartboard
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.dartboard, 5)
        left_layout.addLayout(button_layout, 1)

        # Create a QHBoxLayout to hold the left_layout and Settings
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, 5)
        main_layout.addWidget(self.settings, 1)

        # Create a central widget to hold the layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        # Set the central widget
        self.setCentralWidget(central_widget)

        self.setWindowTitle('Scorekeeper Window')
        self.setGeometry(0, 50, 800, 800)
