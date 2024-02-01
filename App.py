from PySide6.QtWidgets import QApplication
from Dartboard import Dartboard
from Scoreboard import Scoreboard

# Run this to start the program
app = QApplication([])
scoreboard = Scoreboard()
dartboard = Dartboard(scoreboard)
dartboard.show()
scoreboard.show()

app.exec()