from PySide6.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PySide6.QtGui import QColor, QLinearGradient

class Leaderboard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Leaderboard")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)

        # Set background gradient
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#E3292E"))
        gradient.setColorAt(1, QColor("#309F6A"))
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setBrush(self.backgroundRole(), gradient)
        self.setPalette(p)

        # Header labels
        header_labels = ["Rank", "Player", "Total Games Played", "Average Turns to Win"]
        for col, label_text in enumerate(header_labels):
            label = QLabel(label_text)
            label.setStyleSheet("QLabel { border: 1px solid black; padding: 5px; background-color: white; font: bold 20px}")
            self.layout.addWidget(label, 0, col)

        # Mock data for top 10 players
        top_players = [
            {"name": "Player 1", "games_played": 10, "avg_turns": 12},
            {"name": "Player 2", "games_played": 8, "avg_turns": 15},
            {"name": "Player 3", "games_played": 12, "avg_turns": 11},
            {"name": "Player 4", "games_played": 15, "avg_turns": 10},
            {"name": "Player 5", "games_played": 9, "avg_turns": 14},
            {"name": "Player 6", "games_played": 11, "avg_turns": 13},
            {"name": "Player 7", "games_played": 13, "avg_turns": 10},
            {"name": "Player 8", "games_played": 7, "avg_turns": 16},
            {"name": "Player 9", "games_played": 14, "avg_turns": 9},
            {"name": "Player 10", "games_played": 10, "avg_turns": 12}
        ]

        # Populate leaderboard with mock data
        for row, player in enumerate(top_players, start=1):
            rank_label = QLabel(str(row))
            rank_label.setStyleSheet("QLabel { border: 1px solid black; padding: 5px; background-color: white; font: 16px;}")
            self.layout.addWidget(rank_label, row, 0)
            
            name_label = QLabel(player["name"])
            name_label.setStyleSheet("QLabel { border: 1px solid black; padding: 5px; background-color: white; font: 16px; }")
            self.layout.addWidget(name_label, row, 1)
            
            games_played_label = QLabel(str(player["games_played"]))
            games_played_label.setStyleSheet("QLabel { border: 1px solid black; padding: 5px; background-color: white; font: 16px; }")
            self.layout.addWidget(games_played_label, row, 2)
            
            avg_turns_label = QLabel(str(player["avg_turns"]))
            avg_turns_label.setStyleSheet("QLabel { border: 1px solid black; padding: 5px; background-color: white; font: 16px; }")
            self.layout.addWidget(avg_turns_label, row, 3)
