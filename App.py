from PySide6.QtWidgets import QApplication
from Dartboard import *
from Scoreboard import *
from Game import *
from Controller import *

# Run this to start the program
app = QApplication([])
player1 = Player("Test Player 1")
player2 = Player("Test Player 2")
players = [player1, player2]
game = Game(players)
scoreboard = Scoreboard()
dartboard = Dartboard()
controller = Controller(game, scoreboard, dartboard)

app.exec()