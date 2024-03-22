from PySide6.QtWidgets import QMainWindow, QVBoxLayout
from .Dartboard import *
from .Scoreboard import *

class JumbotronUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a Scoreboard instance
        self.dartboard = Dartboard(clickable=False)
        self.scoreboard = Scoreboard()

        # Create a QVBoxLayout to hold the Dartboard
        layout = QVBoxLayout()
        layout.addWidget(self.dartboard, 5)
        layout.addWidget(self.scoreboard, 1)

        # Create a central widget to hold the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)

        # Set the central widget
        self.setCentralWidget(central_widget)

        self.setWindowTitle('Jumbotron Window')
        self.setGeometry(1000, 50, 500, 750)
