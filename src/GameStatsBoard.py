from PySide6.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PySide6.QtGui import QFont, QColor, QLinearGradient
from PySide6.QtCore import Qt

class GameStatisticsWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)

        self.setWindowTitle("Game Statistics")
        self.setGeometry(1350, 50, 500, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)

        # background
        self.setStyleSheet("QMainWindow { border: 4px solid black; }")

        # stats labels
        statistics = ["Current Turn Average", "Average Score / turn", "Number of 180s", "Lowest Turn Score"]

        for row, stat in enumerate(statistics, start=1):
            stat_label = QLabel(stat)
            stat_label.setFont(QFont("Arial", 12, QFont.Bold))
            stat_label.setStyleSheet("QLabel { border: 1px solid black; padding: 5px; background-color: white; }")
            self.layout.addWidget(stat_label, row, 0)

        # stats
        self.game_stats = {
            "Current Turn Average": 0,
            "Average Score / turn" : 0,
            "Number of 180s": 0,
            "Lowest Turn Score": 999
        }
        for row, stat in enumerate(self.game_stats.values(), start=1):
            stat_val = QLabel(str(stat))
            stat_val.setFont(QFont("Arial", 12))
            stat_val.setStyleSheet("QLabel { border: 1px solid black; padding: 5px; background-color: white; }")
            stat_val.setAlignment(Qt.AlignRight)
            self.layout.addWidget(stat_val, row, 1)

        # Hide the window initially
        self.hide()

    def refresh_stat_board(self, game):
        self.game_stats = {
            "Average Turn Score": '%.2f'%(game.avg_turn_score),
            "Average Score / turn" : '%.2f'%(game.avg_score_per_turn),
            "Number of 180s": game.num_180s,
            "Lowest Turn Score": game.lowest_turn_score
        }
        for row, stat in enumerate(self.game_stats.values(), start=1):
            stat_val = QLabel(str(stat))
            stat_val.setFont(QFont("Arial", 12))
            stat_val.setStyleSheet("QLabel { border: 1px solid black; padding: 5px; background-color: white; }")
            stat_val.setAlignment(Qt.AlignRight)
            self.layout.addWidget(stat_val, row, 1)
    def set_visibility(self, visible):
        if visible:
            self.show()
        else:
            self.hide()