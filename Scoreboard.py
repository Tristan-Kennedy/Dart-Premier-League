from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 501

class Scoreboard(QMainWindow):
    def __init__(self, players):
        super().__init__()
        self.setWindowTitle("ScoreBoard")
        self.players = players
        self.current_player_index = 0
        self.turns = 0

        self.scoreLabels = [QLabel(self.get_score_text(player)) for player in self.players]
        
        layout = QVBoxLayout()
        for scoreLabel in self.scoreLabels:
            layout.addWidget(scoreLabel)
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def get_score_text(self, player):
        return f"{player.name}: {player.score}"

    def update_score(self, score):
        self.players[self.current_player_index].score -= score
        self.scoreLabels[self.current_player_index].setText(self.get_score_text(self.players[self.current_player_index]))
        self.turns += 1

        if self.turns >= 3:
            self.turns = 0
            self.current_player_index = (self.current_player_index + 1) % len(self.players)