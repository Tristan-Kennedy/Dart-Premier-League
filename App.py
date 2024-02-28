from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider
from PySide6.QtCore import Qt
from Dartboard import *
from Scoreboard import *
from Game import *
from Controller import *

# Custom widget for resizable window with slider
class ResizableWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):  #sets up a slider and a label
        layout = QVBoxLayout(self)
        label = QLabel("Window Size. Drag to adjust") #always assume your user is an idiot
        layout.addWidget(label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(100)
        self.slider.setMaximum(1000)
        self.slider.setValue(400)
        self.slider.valueChanged.connect(self.on_slider_change) #the slider can send a signal. this will pick up that signal 
        layout.addWidget(self.slider)

    def on_slider_change(self, value):
        self.main_window.resize(value, value) #resizes the window 

# Create a main window
class MainWindow(QMainWindow): 
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

       
        player1 = Player("Test Player 1")
        player2 = Player("Test Player 2")
        players = [player1, player2]
        game = Game(players)
        scoreboard = Scoreboard()
        dartboard = Dartboard()
        controller = Controller(game, scoreboard, dartboard)

        layout.addWidget(dartboard)
        resizable_widget = ResizableWidget(self)
        layout.addWidget(resizable_widget)
        layout.addWidget(scoreboard)


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
