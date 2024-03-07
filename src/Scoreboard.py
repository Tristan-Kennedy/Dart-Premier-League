from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class Scoreboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ScoreBoard")
        self.scoreLabels = []
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def get_score_text(self, player, is_current_player):
        return f"{'-->' if is_current_player else ''} {player.fName} {player.lName}: {player.score}, Legs won: {player.legs_won}, Matches won: {player.matches_won}"

    def refresh_scoreboard(self, players, current_player_index):
        # Clear existing labels
        for label in self.scoreLabels:
            label.deleteLater()  # Delete label from the layout and release resources
        self.scoreLabels = []  # Clear the list of labels

        # Add or update labels based on the players
        for i, player in enumerate(players):
            label = QLabel(self.get_score_text(player, i == current_player_index))
            self.scoreLabels.append(label)
            self.layout.addWidget(label)
