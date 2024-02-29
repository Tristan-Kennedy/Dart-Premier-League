from PySide6.QtWidgets import QMainWindow, QVBoxLayout
from .Scoreboard import *

class JumbotronUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a Scoreboard instance
        self.scoreboard = Scoreboard()

        # Create a QVBoxLayout to hold the Dartboard
        layout = QVBoxLayout()
        layout.addWidget(self.scoreboard)

        # Create a central widget to hold the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)

        # Set the central widget
        self.setCentralWidget(central_widget)

        self.setWindowTitle('Jumbotron Window')
        self.setGeometry(200, 200, 100, 100)
