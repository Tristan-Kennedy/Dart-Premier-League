from PySide6.QtWidgets import QApplication
from Dartboard import Dartboard
from Scoreboard import *

# Run this to start the program
app = QApplication([])
player1 = Player("Test Player 1")
player2 = Player("Test Player 2")
players = [player1, player2]
scoreboard = Scoreboard(players)
dartboard = Dartboard(scoreboard)
dartboard.show()
scoreboard.show()

app.exec()