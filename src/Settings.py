from PySide6.QtWidgets import QWidget, QSlider, QVBoxLayout
from PySide6.QtCore import Qt, Signal

class Settings(QWidget):
    scoreboard_resize = Signal(int)

    def __init__(self):
        super().__init__()
        self.scoreLabels = []
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(50)
        self.slider.setMaximum(500)
        self.slider.setValue(200)
        self.slider.valueChanged.connect(self.scoreboard_resize.emit)

        self.layout.addWidget(self.slider)

    