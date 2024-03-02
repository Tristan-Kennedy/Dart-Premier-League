#attempt at making a knockout/foul button
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QPainterPath, QColor, QFont
from PySide6.QtCore import Qt, QPoint, QRectF, Signal

class Knockout(QWidget):
    #Basic Widget Construction 
    knockout_click = Signal(int)
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 50, 50)
        self.setWindowTitle('Knockout')

        self.setMouseTracking(True)

    #Paint the button
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(QBrush(QColor(128, 0, 128)))
        button_size = 75
        button_rect = QRectF((self.width() - button_size) / 2, (self.height() - button_size) / 2, button_size, button_size)
        painter.drawRect(button_rect) #draw the button with our custom size 
     #Add text to the button:
        text = "KNOCKOUT"
        font = QFont("Comic Sans MS", 8) #pick a font. I dare you to find one more cursed than this
        painter.setFont(font)
        text_rect = QRectF(0, 0, self.width(), self.height())
        painter.drawText(text_rect, Qt.AlignCenter, text) 
    

        
#Needs to be updated to add logic for what happens when the button is clicked. 
