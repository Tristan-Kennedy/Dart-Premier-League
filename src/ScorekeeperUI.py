from PySide6.QtWidgets import QMainWindow, QVBoxLayout
from .Dartboard import *
from .Settings import *

class ScorekeeperUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a Dartboard instance
        self.dartboard = Dartboard()
        self.settings = Settings()

        # Create a QVBoxLayout to hold the Dartboard
        layout = QVBoxLayout()
        layout.addWidget(self.dartboard, 5)
        layout.addWidget(self.settings, 1)

        # Create a central widget to hold the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)

        # Set the central widget
        self.setCentralWidget(central_widget)

        self.setWindowTitle('Scorekeeper Window')
        self.setGeometry(100, 100, 800, 800)
