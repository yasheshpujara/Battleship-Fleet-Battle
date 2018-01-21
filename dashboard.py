import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QPushButton, QHBoxLayout, QGroupBox, QVBoxLayout, QGridLayout, QLabel
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class Example(QDialog):
    def __init__(self):
        super().__init__()
        self.initialize()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(50, 50, 1820, 950)
        self.setWindowTitle('Battleship - Fleet Battle')
        self.setWindowIcon(QIcon('battleship.png'))
        self.setMouseTracking(True)
        self.info_pane()
        self.show()

    def initialize(self):
        self.ship_align = 0
        self.ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

    def info_pane(self):
        header = QLabel("Battleship Type", self)
        header.setGeometry(50, 70, 100, 70)
        y1, y2 = 90, 90
        for i in range(1, 5):
            text = "Type-"+str(i)+":"
            bs = QLabel(text, self)
            bs.setGeometry(50, y1, 100, y2)
            ships_left = QLabel(str(self.ships.count(i)), self)
            ships_left.setGeometry(120, y1, 140, y2)
            y1 += 60
            y2 += 60

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_grid(qp)
        qp.end()

    def draw_grid(self, qp):
        qp.setBrush(QColor(25, 0, 90, 200))
        pen = QPen(QColor(135, 206, 250), 2, Qt.SolidLine)
        qp.setPen(pen)

        x, y = 420, 120
        for c in range(2):
            for _ in range(10):
                x = 420 if c == 0 else 1120
                for _ in range(10):
                    qp.drawRect(x, y, 60, 60)
                    x += 60
                y += 60
            y = 120

    def draw_ships(self, x, y, size):
        qp1 = QPainter()
        qp1.begin(self)
        qp1.setBrush(QColor(255, 80, 0, 160))
        pen1 = QPen(QColor(135, 206, 250), 2, Qt.SolidLine)
        qp1.setPen(pen1)
        x = x - x % 60
        y = y - y % 60
        for _ in range(size):
            qp1.drawRect(x, y, 60, 60)
            x += 60
        qp1.end()

    def mousePressEvent(self, event):
        button_pressed = event.button()
        button_pressed = int(button_pressed)
        if button_pressed == 1:
            x = event.x()
            y = event.y()
            print(x, y)
            self.draw_ships(x, y, self.ships[0])
            self.ships.pop(0)
            self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
