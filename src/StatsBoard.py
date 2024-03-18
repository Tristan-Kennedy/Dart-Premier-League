from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget
from PySide6.QtGui import QFont, QColor, QLinearGradient

class StatisticsWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Player Statistics")
        self.setGeometry(100, 100, 600, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)

        # background
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#E3292E"))
        gradient.setColorAt(1, QColor("#309F6A"))
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setBrush(self.backgroundRole(), gradient)
        self.setPalette(p)

        # player labels
        player1_label = QLabel("Player 1")
        player1_label.setFont(QFont("Arial", 12, QFont.Bold))
        player1_label.setStyleSheet("QLabel { border: 1px solid black; padding: 5px; background-color: white; }")
        self.layout.addWidget(player1_label, 0, 1)

        player2_label = QLabel("Player 2")
        player2_label.setFont(QFont("Arial", 12, QFont.Bold))
        player2_label.setStyleSheet("QLabel { border: 1px solid black; padding: 5px; background-color: white; }")
        self.layout.addWidget(player2_label, 0, 2)

        # stats label
        statistics = ["Total Games Played", "Average Turns to Win"]

        for row, stat in enumerate(statistics, start=1):
            stat_label = QLabel(stat)
            stat_label.setFont(QFont("Arial", 12, QFont.Bold))
            stat_label.setStyleSheet("QLabel { border: 1px solid black; padding: 5px; background-color: white; }")
            self.layout.addWidget(stat_label, row, 0)

        # dummy stats p1
        player1_stats = {
            "Total Games Played": 10,
            "Average Turns to Win": 12
        }

        # dummy stats p2
        player2_stats = {
            "Total Games Played": 8,
            "Average Turns to Win": 15
        }

        # p1
        for row, stat in enumerate(player1_stats.values(), start=1):
            stat_label = QLabel(str(stat))
            stat_label.setFont(QFont("Arial", 12))
            stat_label.setStyleSheet("QLabel { border: 1px solid black; padding: 5px; background-color: white; }")
            self.layout.addWidget(stat_label, row, 1)

        # p2
        for row, stat in enumerate(player2_stats.values(), start=1):
            stat_label = QLabel(str(stat))
            stat_label.setFont(QFont("Arial", 12))
            stat_label.setStyleSheet("QLabel { border: 1px solid black; padding: 5px; background-color: white; }")
            self.layout.addWidget(stat_label, row, 2)