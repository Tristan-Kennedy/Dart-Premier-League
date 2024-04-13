from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics

class Scoreboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ScoreBoard") 
        self.scoreLabels = []
        self.layout = QVBoxLayout() 
        self.setLayout(self.layout)
        self.layout.setSpacing(0)  # Set the spacing between widgets to 0
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create and add header row
        self.header_labels = []
        header_layout = QHBoxLayout()
        for header in ["", "SETS", "LEGS", " "]:
            label = QLabel(header)
            label.setStyleSheet("background-color: black; color: white; font: bold 14px")
            if label.text() != "":
                label.setFixedWidth(50)
            label.setAlignment(Qt.AlignCenter)
            header_layout.addWidget(label)
            self.header_labels.append(label)
        self.layout.addLayout(header_layout)

        # Create footer row
        self.footer_layout = QHBoxLayout()
        self.footer_label = QLabel()
        self.footer_label.setStyleSheet("background-color: black; color: white;")
        self.footer_label.setAlignment(Qt.AlignCenter)
        self.footer_layout.addWidget(self.footer_label)

    def throws_to_win(self, target_score):
        # Define available throws
        available_throws = [
            [20, 3], [19, 3], [18, 3], [17, 3], [16, 3], [15, 3],
            [14, 3], [13, 3], [12, 3], [11, 3], [10, 3], [9, 3],
            [8, 3], [7, 3], [6, 3], [5, 3], [4, 3], [3, 3],
            [2, 3], [1, 3],
            [25, 2], [20, 2], [19, 2], [18, 2], [17, 2], [16, 2], [15, 2],
            [14, 2], [13, 2], [12, 2], [11, 2], [10, 2], [9, 2],
            [8, 2], [7, 2], [6, 2], [5, 2], [4, 2], [3, 2],
            [2, 2], [1, 2],
            [25, 1], [20, 1], [19, 1], [18, 1], [17, 1], [16, 1], [15, 1],
            [14, 1], [13, 1], [12, 1], [11, 1], [10, 1], [9, 1],
            [8, 1], [7, 1], [6, 1], [5, 1], [4, 1], [3, 1],
            [2, 1], [1, 1],
        ]  # throws are stored as their value + the multiplier

        throw_types = {1: '', 2: 'D', 3: 'T'}  # dictionary mapping multiplier to their literal

        # memo table speeds things up tremendously
        memo = {}  # initialize the memo table
        memo[0] = []

        for score in range(1, target_score + 1):  # iterate through the score
            best_combination = None  # initialize our best combo

            # Try all possible throws and update the best combination for the current score
            for throw, multiplier in available_throws:
                if score - throw * multiplier >= 0:
                    if memo[score - throw * multiplier] is not None:
                        combination = memo[score - throw * multiplier] + [(throw, multiplier)]  # big time saver: check the memo table to see if we already have an entry for that remaining score have an entry for the current

                        if score == target_score and multiplier != 2:  # you can only win on a double as far as I know. So if the last throw isn't a double, skip it
                            continue
                        if best_combination is None or len(combination) < len(best_combination):
                            best_combination = combination
            memo[score] = best_combination  # store the results in the memo table for future reference

        # Convert the combination to include throw types
        throw_combination = []
        for throw, multiplier in memo[target_score]:
            throw_type = throw_types[multiplier]
            throw_combination.append((throw, throw_type))

        # Return the best combination for the target score
        return throw_combination

    def refresh_scoreboard(self, game):
        # Clear existing labels
        for label_list in self.scoreLabels:
            for item in label_list:
                item.deleteLater()  # Delete label from the layout and release resources
        self.scoreLabels = []  # Clear the list of labels

        # Remove footer layout from main layout
        self.layout.removeItem(self.footer_layout)

        # Update footer
        self.footer_label.setText(f"First to {game.best_of_matches} Sets")

        # Add or update labels based on the players
        for i, player in enumerate(game.players):
            # Create a horizontal layout for each player (row)
            row_layout = QHBoxLayout()

            player_label = QLabel(f"{player.fName} {player.lName}")
            perfect_score_label = QLabel()
            ttw_label = QLabel()
            matches_won_label = QLabel(str(player.matches_won))
            legs_won_label = QLabel(str(player.legs_won))
            score_label = QLabel(str(player.score))
            # Set fixed width and elide text if necessary
            for label in [matches_won_label, legs_won_label, score_label]:
                label.setFixedWidth(50)
                fm = QFontMetrics(label.font())
                elided_text = fm.elidedText(label.text(), Qt.ElideRight, label.width())
                label.setText(elided_text)

            # Set background color for data fields
            for label in [matches_won_label, legs_won_label, score_label]:
                label.setStyleSheet("background-color: red; color: white; border: 1px solid black; padding: 5px; font: bold 14px")
                label.setAlignment(Qt.AlignCenter)

            # Highlight the current player
            if i == game.current_player_index:
                player_label.setStyleSheet("background-color: yellow; border: 1px solid black; padding: 5px; font: bold 14px")
                if game.bust:
                    player_label.setStyleSheet("background-color: red; border: 1px solid black; padding: 5px; font: bold 14px")
                    player_label.setText("BUST")
                if game.leg_end:
                    player_label.setStyleSheet("background-color: green; border: 1px solid black; padding: 5px; font: bold 14px")
                    player_label.setText(player_label.text() + " WINNER")
            else:
                player_label.setStyleSheet("border: 1px solid black; padding: 5px; font: bold 14px")

            # Add labels to the row layout
            row_layout.addWidget(player_label)

            # On track for perfect leg
            if player.total_throws + len(self.throws_to_win(player.score)) <= len(self.throws_to_win(player.starting_score)) and player.total_throws != 0:
                perfect_score_label.setText(f"{len(self.throws_to_win(player.starting_score))}")
                perfect_score_label.setStyleSheet("background-color: yellow; color: black; border: 1px solid black; padding: 5px; font: bold 14px")
                perfect_score_label.setFixedWidth(50)
                row_layout.addWidget(perfect_score_label)

            # Create a label for throws to win
            if player.score <= 170:
                ttw = self.throws_to_win(player.score)
                ttw_text = ", ".join(f"{item[1]}{item[0]}" for item in ttw)
                ttw_label.setText(ttw_text)
                ttw_label.setStyleSheet("background-color: green; color: white; border: 1px solid black; padding: 5px; font: bold 14px")
                row_layout.addWidget(ttw_label)

            row_layout.addWidget(matches_won_label)
            row_layout.addWidget(legs_won_label)
            row_layout.addWidget(score_label)
            # Add the row layout to the main layout
            self.layout.addLayout(row_layout)

            # Store the labels for later updates
            self.scoreLabels.append([player_label, perfect_score_label, ttw_label, matches_won_label, legs_won_label, score_label])

        # Add the footer layout to the main layout
        self.layout.addLayout(self.footer_layout)
