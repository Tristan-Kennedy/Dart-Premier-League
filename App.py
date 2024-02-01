from PySide6.QtWidgets import QApplication
from Dartboard import Dartboard

# Run this to start the program
app = QApplication([])
window = Dartboard()
window.show()

app.exec()