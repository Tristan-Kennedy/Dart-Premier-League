from PySide6.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QVBoxLayout
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt

class PlayerStatisticsWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)

        self.setWindowTitle("Player Statistics")
        self.setGeometry(1350, 50, 500, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # background
        self.setStyleSheet("QMainWindow { border: 5px solid black; }")

        # Profile Picture
        self.profile_picture = QLabel()
        self.profile_picture.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.profile_picture)

        # Player info
        self.player_name = QLabel()
        self.player_name.setFont(QFont("Arial", 16, QFont.Bold))
        self.player_name.setAlignment(Qt.AlignCenter)
        self.player_name.setStyleSheet("QLabel { padding: 5px; }")

        self.player_country = QLabel()
        self.player_country.setFont(QFont("Arial", 14))
        self.player_country.setAlignment(Qt.AlignCenter)
        self.player_country.setStyleSheet("QLabel { padding: 5px; }")

        self.layout.addWidget(self.player_name)
        self.layout.addWidget(self.player_country)

        # stats grid layout
        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)

        # stats label
        statistics = ["Current League Rank", "Three Dart Avg Score", "Number of 180s (total)", "Total Games Played", "Total Wins"]

        for row, stat in enumerate(statistics, start=0):
            stat_label = QLabel(stat)
            stat_label.setFont(QFont("Arial", 12, QFont.Bold))
            stat_label.setStyleSheet("QLabel { border: 1px solid black; padding: 5px; background-color: white; }")
            self.grid_layout.addWidget(stat_label, row, 0)

        # Hide the window initially
        self.hide()

    def set_visibility(self, visible, player):
        if visible:
            self.player_name.setText(player[1] + " " + player[2]) # Assuming first name is at index 0 and last name is at index 1
            self.player_country.setText(player[3]) # Assuming country is at index 2
            self.profile_picture.setPixmap(QPixmap(player[4]).scaled(400, 400)) # Assuming profile picture path is at index 3

            # Assuming stats are at indices 10, 5, 7, 8, 9
            stats = [player[i] for i in [10, 5, 7, 8, 9]]

            for row, stat in enumerate(stats, start=0):
                stat_label = QLabel(str(stat))
                stat_label.setFont(QFont("Arial", 12))
                stat_label.setStyleSheet("QLabel { border: 1px solid black; padding: 5px; background-color: white; }")
                self.grid_layout.addWidget(stat_label, row, 1)

            self.show()
        else:
            self.hide()