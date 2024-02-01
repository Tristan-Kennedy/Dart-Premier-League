from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QPainterPath, QColor
from PySide6.QtCore import Qt, QPoint
import math

class Dartboard(QWidget):
    def __init__(self, scoreboard):
        super().__init__()

        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle('Dartboard')

        self.point_values = [6, 13, 4, 18, 1, 20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15, 10]
        self.clicked_point = None

        self.setMouseTracking(True)
        
        self.scoreboard = scoreboard

    # This entire function just draws the dart board
    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        radius = min(width, height) // 2
        center = QPoint(width // 2, height // 2)
        anglePerPie = 18 * 16
        angleOffset = 9 * 16

        green = QColor('#309F6A')
        red = QColor('#E3292E')

        for i in range(20):
            angle = (i * anglePerPie) - angleOffset
            qp.setPen(QPen(Qt.black, 2))
            qp.setBrush(QBrush(QColor("#F9DFBC") if i % 2 == 0 else Qt.black))
            qp.drawPie(center.x() - radius, center.y() - radius, radius * 2, radius * 2, angle, anglePerPie)

        qp.setPen(QPen(Qt.black, 2))
        qp.setBrush(Qt.NoBrush)

        fill_color = [green, red]

        for i in range(20):
            angle = (i * anglePerPie) - angleOffset 

            outer_path = QPainterPath()
            outer_path.arcMoveTo(center.x() - radius, center.y() - radius, radius * 2, radius * 2, angle / 16)
            outer_path.arcTo(center.x() - radius, center.y() - radius, radius * 2, radius * 2, angle / 16, 18)
            outer_path.arcTo(center.x() - radius * 0.9, center.y() - radius * 0.9, 1.8 * radius, 1.8 * radius, (angle + anglePerPie) / 16, -18)
            qp.fillPath(outer_path, QBrush(fill_color[i % 2]))
            
            inner_path = QPainterPath()
            inner_path.arcMoveTo(center.x() - radius * 0.6, center.y() - radius * 0.6, radius * 1.2, radius * 1.2, angle / 16)
            inner_path.arcTo(center.x() - radius * 0.6, center.y() - radius * 0.6, radius * 1.2, radius * 1.2, angle / 16, 18)
            inner_path.arcTo(center.x() - radius * 0.5, center.y() - radius * 0.5, radius, radius, (angle + anglePerPie) / 16, -18)
            qp.fillPath(inner_path, QBrush(fill_color[i % 2]))

        # Redraw dividing lines
        qp.drawArc(center.x() - radius * 0.9, center.y() - radius * 0.9, radius * 1.8, radius * 1.8, 0, 360 * 16)
        qp.drawArc(center.x() - radius * 0.6, center.y() - radius * 0.6, radius * 1.2, radius * 1.2, 0, 360 * 16)
        qp.drawArc(center.x() - radius * 0.5, center.y() - radius * 0.5, radius * 1.0, radius * 1.0, 0, 360 * 16)

        # Draw bullseye
        qp.setBrush(QBrush(green))
        qp.drawEllipse(center, radius * 0.1, radius * 0.1)
        qp.setBrush(QBrush(red))
        qp.drawEllipse(center, radius * 0.05, radius * 0.05)

    def mousePressEvent(self, event):
        self.clicked_point = event.position()
        self.update()

    def mouseReleaseEvent(self, event):
        if self.clicked_point is not None:
            point = self.clicked_point
            width = self.width()
            height = self.height()
            radius = min(width, height) // 2
            center = QPoint(width // 2, height // 2)
            distance = math.sqrt((point.x() - center.x()) ** 2 + (point.y() - center.y()) ** 2)
            angle = self.calculate_angle(point, center)

            section = int(angle // 18)
            if section >= 20:     # Correct for getting the 20th value which doesn't exist
                section = 0   # Wrap around to the start of the list

            # This sets the base score based upon the section
            score = self.point_values[section]

            # This modifies the score based upon the distance from the center
            if distance < radius * 0.05:
                score = 50
            elif distance < radius * 0.1:
                score = 25
            elif distance < radius * 0.6 and distance > radius * 0.5:
                score *= 3
            elif distance > radius * 0.9:
                score *= 2

            # Change or add to this code to modify what the function of clicking on the sections is.
            self.scoreboard.update_score(score)
            self.clicked_point = None

    def mouseMoveEvent(self, event):
        self.update()

    # Angle calculation <3
    def calculate_angle(self, point, center):
        diff = QPoint(point.x() - center.x(), point.y() - center.y())
        angle = math.atan2(-diff.y(), diff.x())
        return ((angle * 57.2958) + 360) % 360 + 9
