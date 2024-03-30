from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QSizePolicy, QMessageBox
from PySide6.QtCore import Signal
from .Dartboard import *
from .Settings import *

class ScorekeeperUI(QMainWindow):
    bounceout_signal = Signal()
    foul_signal = Signal()
    show_leaderboard_signal = Signal()

    def __init__(self):
        super().__init__()

        self.dartboard = Dartboard(clickable=True)
        self.settings = Settings()

        # Create QPushButton instances for buttons
        self.knockout_button = QPushButton("Knockout")
        self.foul_button = QPushButton("Foul")
        self.bounceout_button = QPushButton("Bounceout")

        # Connect button clicks to custom slots emitting signals
        self.knockout_button.clicked.connect(self.knockout)
        self.foul_button.clicked.connect(self.emit_foul_signal)
        self.bounceout_button.clicked.connect(self.emit_bounceout_signal)

        # Create a QVBoxLayout for the buttons
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.knockout_button)
        button_layout.addWidget(self.foul_button)
        button_layout.addWidget(self.bounceout_button)
        # Set the stretch factors for the buttons
        self.knockout_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.foul_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.bounceout_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create a QVBoxLayout for the side layout
        side_layout = QVBoxLayout()

        # Add the buttons layout to the side layout with a stretch factor of 1
        side_layout.addLayout(button_layout, 1)
        side_layout.addWidget(self.settings)

        # Create a QHBoxLayout to hold the Dartboard and settings
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.dartboard, 5)
        main_layout.addLayout(side_layout)

        # Create a central widget to hold the layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        # Set the central widget
        self.setCentralWidget(central_widget)

        self.setWindowTitle('Scorekeeper Window')
        self.setGeometry(0, 50, 800, 800)

    def knockout(self):
        self.dartboard.knockout_mode = True
        QMessageBox.information(self, "Knockout", "Click on the dart to be knocked out.")

    def emit_foul_signal(self):
        self.foul_signal.emit()  # Adjust argument as needed

    def emit_bounceout_signal(self):
        self.bounceout_signal.emit()  # Adjust argument as needed

    def show_leaderboard_dialog(self):
        reply = QMessageBox.question(self, 'Show Leaderboard', 'Do you want to show the leaderboard?', 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.show_leaderboard_signal.emit()
