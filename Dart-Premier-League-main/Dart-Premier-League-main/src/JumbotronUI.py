from PySide6.QtWidgets import QMainWindow, QVBoxLayout
from .Dartboard import *
from .Scoreboard import *
from .Leaderboard import *

class JumbotronUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a Scoreboard instance
        self.dartboard = Dartboard(clickable=False)
        self.scoreboard = Scoreboard()
        self.leaderboard = Leaderboard()

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
        self.setGeometry(850, 50, 500, 750)

    def enable_leaderboard(self):
        # Remove the dartboard and settings
        self.dartboard.setParent(None)
        self.scoreboard.setParent(None)

        # Add the leaderboard to the main layout
        main_layout = self.centralWidget().layout()
        main_layout.addWidget(self.leaderboard)

        self.setWindowTitle('Leaderboard')
