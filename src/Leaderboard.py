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
        header_labels = ["Rank", "Player", "Total Games Played", "Total Wins"]
        for col, label_text in enumerate(header_labels):
            label = QLabel(label_text)
            label.setStyleSheet("QLabel { border: 1px solid black; padding: 5px; background-color: white; font: bold 20px}")
            self.layout.addWidget(label, 0, col)

    def populate_leaderboard(self, players):
        # Sort players by rank
        players.sort(key=lambda x: x[10], reverse=False)

        # Populate leaderboard with player data or ---
        for row in range(10):
            if row < len(players):
                player = players[row]
                data = [str(row+1), str(player[1] + ' ' + player[2]), str(player[8]), str(player[9])]  # Assuming player name, games played, average turns are at index 0, 1, 2
            else:
                data = ['---', '---', '---', '---']

            for col, item in enumerate(data):
                label = QLabel(str(item))
                label.setStyleSheet("QLabel { border: 1px solid black; padding: 5px; background-color: white; font: 16px; }")
                self.layout.addWidget(label, row+1, col)