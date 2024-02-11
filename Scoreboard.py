from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 501
        self.legs_won = 0
        self.previous_score = self.score

class Scoreboard(QMainWindow):
    def __init__(self, players):
        super().__init__()
        self.setWindowTitle("ScoreBoard")
        self.players = players
        self.current_player_index = 0
        self.starting_player_index = 0
        self.turns = 0

        self.scoreLabels = [QLabel(self.get_score_text(player, i == self.current_player_index)) for i, player in enumerate(self.players)]
        
        layout = QVBoxLayout()
        for scoreLabel in self.scoreLabels:
            layout.addWidget(scoreLabel)
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def get_score_text(self, player, is_current_player):
        return f"{'-->' if is_current_player else ''} {player.name}: {player.score}, Legs won: {player.legs_won}"

    def refresh_scoreboard(self):
        for i, player in enumerate(self.players):
            self.scoreLabels[i].setText(self.get_score_text(player, i == self.current_player_index))

    def reset_scores(self):
        for player in self.players:
            player.score = 501

    def update_score(self, score):
        current_player = self.players[self.current_player_index]
        current_player.previous_score = current_player.score
        current_player.score -= score
        self.turns += 1
        
        bust = False
        if current_player.score == 0:
            # Exactly 0, player wins the leg
            current_player.legs_won += 1
            # Reset the score to 501 for the next leg
            self.reset_scores()
            # Reset turns and alternate starting player
            self.turns = 0
            self.starting_player_index = (self.starting_player_index + 1) % len(self.players)
            self.current_player_index = self.starting_player_index

        elif current_player.score < 1 or current_player.score == 1:
            # Bust, reset score to previous score
            current_player.score = current_player.previous_score
            bust = True

        if self.turns >= 3 or bust:
            self.turns = 0
            self.current_player_index = (self.current_player_index + 1) % len(self.players)

        # Update the labels for all players
        self.refresh_scoreboard()