#attempt at making a knockout/foul button
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QPainterPath, QColor, QFont
from PySide6.QtCore import Qt, QPoint, QRectF, Signal

class Foul(QWidget):
    #Basic Widget Construction 
    foul_signal = Signal(int)

    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 50, 50)
        self.setWindowTitle('Foul')

        self.setMouseTracking(True)

    #Paint the button
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(QBrush(QColor(176, 200, 112)))
        button_size = 75
        button_rect = QRectF((self.width() - button_size) / 2, (self.height() - button_size) / 2, button_size, button_size)
        painter.drawRect(button_rect) #draw the button with our custom size 
        
        
    #add text
        text = "FOUL"
        font = QFont("Comic Sans MS", 10) #pick a font. I dare you to find one more cursed than this
        painter.setFont(font)
        text_rect = QRectF(0, 0, self.width(), self.height())
        painter.drawText(text_rect, Qt.AlignCenter, text) 
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.foul_signal.emit(1)
            

        
