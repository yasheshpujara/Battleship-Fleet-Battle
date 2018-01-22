import sys
import socket
from threading import Thread
from PyQt5.QtWidgets import QApplication, QDialog, QLabel
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class Example(QDialog):
    def __init__(self):
        super().__init__()
        self.ship_align = [None for _ in range(11)]
        self.ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        self.click = False
        self.pos = (0, 0)
        self.ship_coordinates = {}
        self.ship_count = 0
        self.attack_coordinates = []
        self.attack = True
        self.attack_count = 0
        self.all_coordinates = []
        self.hit = False
        self.opponent_attacked = []
        self.init_ui()

    def init_ui(self):
        self.setGeometry(50, 50, 1820, 950)
        self.setWindowTitle('Battleship - Fleet Battle')
        self.setWindowIcon(QIcon('battleship.png'))
        self.setMouseTracking(True)
        self.info_pane()
        self.show()

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

    def populate_ship_coordinates(self):
        temp = []
        for key in self.ship_coordinates.keys():
            for value in self.ship_coordinates[key]:
                temp.append(value)
        counter = 3
        for value in range(len(temp)):
            self.all_coordinates.append(temp[value])
            a, b = 60, 60
            for _ in range(counter):
                if self.ship_align[value+1]:
                    self.all_coordinates.append((temp[value][0], temp[value][1]+b))
                    b += 60
                else:
                    self.all_coordinates.append((temp[value][0] + a, temp[value][1]))
                    a += 60
            if value == 0 or value == 2 or value == 5:
                counter -= 1

    def get_coordinates(self):
        return self.pos[0] - self.pos[0] % 60, self.pos[1] - self.pos[1] % 60

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
                x = 420 if c == 0 else 1140
                for _ in range(10):
                    qp.drawRect(x, y, 60, 60)
                    x += 60
                y += 60
            y = 120

        if self.click:
            qp.setBrush(QColor(119, 136, 153))
            pen = QPen(QColor(135, 206, 250), 2, Qt.SolidLine)
            qp.setPen(pen)
            x, y = self.get_coordinates()
            ox, oy = x, y
            for _ in range(self.ships[0]):
                qp.drawRect(x, y, 60, 60)
                if self.ship_align[self.ship_count]:
                    y += 60
                else:
                    x += 60
            self.click = False
            if self.ships[0] in self.ship_coordinates.keys():
                self.ship_coordinates[self.ships[0]].append((ox, oy))
            else:
                self.ship_coordinates[self.ships[0]] = [(ox, oy)]

            self.draw_ships(qp)
            self.ships.pop(0)

        elif self.attack:
            self.draw_ships(qp)
            self.draw_attacks(qp)
            self.draw_opponent_attacks(qp)
            self.attack = False
        elif not self.attack:
            self.draw_ships(qp)
            self.draw_attacks(qp)
            self.draw_opponent_attacks(qp)
            self.attack = True

    def draw_ships(self, qp):
        counter = 0
        ships_present = list(self.ship_coordinates.keys())[:self.ship_count-1]
        for value in ships_present:
            for ship in range(len(self.ship_coordinates[value])):
                counter += 1
                x, y = self.ship_coordinates[value][ship][0], self.ship_coordinates[value][ship][1]
                qp.drawRect(x, y, 60, 60)
                for _ in range(value):
                    qp.drawRect(x, y, 60, 60)
                    if self.ship_align[counter]:
                        y += 60
                    else:
                        x += 60

    def draw_attacks(self, qp):
        qp.setBrush(QColor(250, 7, 7))
        pen = QPen(QColor(135, 206, 250), 2, Qt.SolidLine)
        qp.setPen(pen)
        for place in self.attack_coordinates:
            (p, q) = (place[0], place[1])
            qp.drawRect(p, q, 60, 60)

    def draw_opponent_attacks(self, qp):
        qp.setBrush(QColor(236, 142, 142))
        pen = QPen(QColor(135, 206, 250), 2, Qt.SolidLine)
        qp.setPen(pen)
        for place in self.opponent_attacked:
            (p, q) = (place[0], place[1])
            qp.drawRect(p, q, 60, 60)

    def mousePressEvent(self, event):
        button_pressed = event.button()
        button_pressed = int(button_pressed)
        x = event.x()
        y = event.y()
        self.pos = (x, y)
        if 420 <= self.pos[0] <= 1020 and 120 <= self.pos[1] <= 720 and self.ship_count < 10:
            self.ship_count += 1
            self.click = True
            if button_pressed == 1:
                self.ship_align[self.ship_count] = 0
            elif button_pressed == 2:
                self.ship_align[self.ship_count] = 1
            if self.ship_count == 10:
                print("Y")
                self.populate_ship_coordinates()
            self.update()
        elif 1120 <= self.pos[0] <= 1720 and 120 <= self.pos[1] <= 720 and self.ship_count == 10:
            # self.attack = True
            if button_pressed == 1:
                self.attack_count += 1
                self.attack_coordinates.append((self.get_coordinates()))
                t = Thread(target=threaded_function, args=self.attack_coordinates[self.attack_count - 1])
                t.start()
                self.update()

    def update_board(self, data):
        x, y = data.split()
        x, y = [int(x)-720, int(y)]
        if (x, y) in self.all_coordinates:
            self.opponent_attacked.append((x, y))
            self.update()


def threaded_function(arg, arg1):
    try:
        sock.sendall((str(arg) + " " + str(arg1)).encode('utf-8'))
    except Exception as e:
        print(e)


def receive_function(arg):
    while True:
        sock.sendall(name.encode('utf-8'))
        data = sock.recv(160).decode()
        arg.update_board(data)
        # print(data)


if __name__ == "__main__":
    name = input("Enter your Name: ")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip = input(name + " please Enter ip address of server: ")

    server_address = (ip, 10010)
    print('connecting to %s port %s' % server_address)
    sock.connect(server_address)

    # sock.sendall(name.encode('utf-8'))

    app = QApplication(sys.argv)
    ex = Example()
    t1 = Thread(target=receive_function, args=(ex,))
    t1.start()
    sys.exit(app.exec_())
