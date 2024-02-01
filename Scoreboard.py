from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget

class Scoreboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ScoreBoard")
        self.score = 0
        self.scoreLabel = QLabel(str(self.score))
        layout = QVBoxLayout()
        layout.addWidget(self.scoreLabel)
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def update_score(self, score):
        self.score = score
        self.scoreLabel.setText(str(self.score))