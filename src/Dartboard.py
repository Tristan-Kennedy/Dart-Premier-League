from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QPainterPath, QColor, QFont
from PySide6.QtCore import Qt, QPoint, QRectF, Signal, QPointF
import math

class Dartboard(QWidget):
    dart_hit = Signal(int, int, QPointF)

    def __init__(self, clickable):
        super().__init__()

        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle('Dartboard')

        self.point_values = [6, 13, 4, 18, 1, 20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15, 10]
        self.clicked_point = None
        self.clickable = clickable

        self.clicked_points = []
        self.clicked_points_history = [] 

        self.setMouseTracking(True)

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

        # Draw outer circle
        outer_radius = radius
        qp.setPen(QPen(Qt.black, 2))
        qp.setBrush(QBrush(Qt.black))
        qp.drawEllipse(center, outer_radius, outer_radius)

        # Draw text
        qp.setPen(QPen(Qt.white, 2))
        qp.setFont(QFont('Arial', radius * 0.05))
        for i in range(20):
            angle = ((5 - i) * anglePerPie) - angleOffset + anglePerPie / 2
            text_radius = radius * 0.95
            text_x = center.x() + text_radius * math.cos(math.radians(angle / 16 - 90))
            text_y = center.y() + text_radius * math.sin(math.radians(angle / 16 - 90))
            rect = QRectF(text_x - radius * 0.05, text_y - radius * 0.05, radius * 0.1, radius * 0.1)
            qp.drawText(rect, Qt.AlignCenter, str(self.point_values[i]))

        # Draw the slices in offwhite and black
        for i in range(20):
            angle = (i * anglePerPie) - angleOffset
            qp.setPen(QPen(Qt.black, 2))
            qp.setBrush(QBrush(QColor("#F9DFBC") if i % 2 == 0 else Qt.black))
            qp.drawPie(center.x() - radius * 0.9, center.y() - radius * 0.9, radius * 1.8, radius * 1.8, angle, anglePerPie)

        qp.setPen(QPen(Qt.black, 2))
        qp.setBrush(Qt.NoBrush)

        fill_color = [green, red]

        # Draw the double and triple sections
        for i in range(20):
            angle = (i * anglePerPie) - angleOffset 

            outer_path = QPainterPath()
            outer_path.arcMoveTo(center.x() - radius * 0.9, center.y() - radius * 0.9, radius * 1.8, radius * 1.8, angle / 16)
            outer_path.arcTo(center.x() - radius * 0.9, center.y() - radius * 0.9, radius * 1.8, radius * 1.8, angle / 16, 18)
            outer_path.arcTo(center.x() - radius * 0.85, center.y() - radius * 0.85, 1.7 * radius, 1.7 * radius, (angle + anglePerPie) / 16, -18)
            qp.fillPath(outer_path, QBrush(fill_color[i % 2]))
            
            inner_path = QPainterPath()
            inner_path.arcMoveTo(center.x() - radius * 0.55, center.y() - radius * 0.55, radius * 1.1, radius * 1.1, angle / 16)
            inner_path.arcTo(center.x() - radius * 0.55, center.y() - radius * 0.55, radius * 1.1, radius * 1.1, angle / 16, 18)
            inner_path.arcTo(center.x() - radius * 0.5, center.y() - radius * 0.5, radius, radius, (angle + anglePerPie) / 16, -18)
            qp.fillPath(inner_path, QBrush(fill_color[i % 2]))

        # Redraw dividing lines
        qp.drawArc(center.x() - radius * 0.85, center.y() - radius * 0.85, radius * 1.7, radius * 1.7, 0, 360 * 16)
        qp.drawArc(center.x() - radius * 0.55, center.y() - radius * 0.55, radius * 1.1, radius * 1.1, 0, 360 * 16)
        qp.drawArc(center.x() - radius * 0.5, center.y() - radius * 0.5, radius, radius, 0, 360 * 16)

        # Draw bullseye
        qp.setBrush(QBrush(green))
        qp.drawEllipse(center, radius * 0.1, radius * 0.1)
        qp.setBrush(QBrush(red))
        qp.drawEllipse(center, radius * 0.05, radius * 0.05)

        qp.setBrush(QBrush(Qt.white))
        for point in self.clicked_points:
            qp.drawEllipse(QPointF(self.width() / 2 + radius * point.x(), self.height() / 2 + radius * point.y()), radius * 0.02, radius * 0.02)

    def mousePressEvent(self, event):
        if self.clickable:
            self.clicked_point = event.position()
            self.update()

    def mouseReleaseEvent(self, event):
        if self.clickable:
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
                wedge_value = self.point_values[section]
                multiplier = 1

                # This modifies the score based upon the distance from the center
                if distance < radius * 0.05:
                    wedge_value = 25
                    multiplier = 2
                elif distance < radius * 0.1:
                    wedge_value = 25
                    multiplier = 1
                elif distance < radius * 0.55 and distance > radius * 0.5:
                    multiplier = 3
                elif distance < radius * 0.9 and distance > radius * 0.85:
                    multiplier = 2
                elif distance > radius * 0.9:
                    multiplier = 0

                radius = min(width, height) // 2
                relative_point = QPointF((self.clicked_point.x() - self.width() / 2) / radius, (self.clicked_point.y() - self.height() / 2) / radius)
                self.clicked_points_history.append(self.clicked_points.copy())

                self.dart_hit.emit(multiplier, wedge_value, relative_point)
                self.clicked_points.append(relative_point)
                self.clicked_point = None

    def mouseMoveEvent(self, event):
        if self.clickable:
            self.update()

    # Angle calculation <3
    def calculate_angle(self, point, center):
        diff = QPoint(point.x() - center.x(), point.y() - center.y())
        angle = math.atan2(-diff.y(), diff.x())
        return ((angle * 57.2958) + 360) % 360 + 9
    
    def add_clicked_point(self, point):
        self.clicked_points_history.append(self.clicked_points.copy())
        self.clicked_points.append(point)
        self.update()

    def undo_clicked_point(self):
        if self.clicked_points_history:  # check if there is any history to revert to
            self.clicked_points = self.clicked_points_history.pop()  # revert to the previous state
            self.update()

    def clear_clicked_points(self):
        self.clicked_points.clear()
        self.update()
