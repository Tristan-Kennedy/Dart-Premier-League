from PySide6.QtWidgets import QApplication
from JumbotronUI import *
from ScorekeeperUI import *
from Game import *
from Controller import *

# Run this to start the program
app = QApplication([])
player1 = Player("Test Player 1")
player2 = Player("Test Player 2")
players = [player1, player2]
game = Game(players)
scorekeeper_ui = ScorekeeperUI()
jumbotron_ui = JumbotronUI()
jumbotron_ui.move(1000, 300)
controller = Controller(game, jumbotron_ui ,scorekeeper_ui)

app.exec()
