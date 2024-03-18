from PySide6.QtWidgets import QApplication
from src.Controller import *

# Run this to start the program
app = QApplication([])
controller = Controller()

app.exec()
