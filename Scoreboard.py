from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QVBoxLayout

class Scoreboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ScoreBoard")

        self.scoreLabels = []
        
        self.layout = QVBoxLayout()
        for scoreLabel in self.scoreLabels:
            self.layout.addWidget(scoreLabel)
        centralWidget = QWidget()
        centralWidget.setLayout(self.layout)
        self.setCentralWidget(centralWidget)

    def get_score_text(self, player, is_current_player):
        return f"{'-->' if is_current_player else ''} {player.name}: {player.score}, Legs won: {player.legs_won}"

    def refresh_scoreboard(self, players, current_player_index):
        for i, player in enumerate(players):
            if i < len(self.scoreLabels):
                # Update existing label
                self.scoreLabels[i].setText(self.get_score_text(player, i == current_player_index))
            else:
                # Create new label and add it to layout
                label = QLabel(self.get_score_text(player, i == current_player_index))
                self.scoreLabels.append(label)
                # Assuming you have a layout for the labels
                self.layout.addWidget(label)