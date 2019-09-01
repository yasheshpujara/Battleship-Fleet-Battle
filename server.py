import socket
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
                             QInputDialog, QApplication, QLabel)
from threading import Thread

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
port = 10010
s.close()

clients, ip_clients, connections = [], [], []

print("IP address of server is " + str(ip) + ":" + str(port))

# Bind the socket to the port
server_address = (ip, port)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)


# def select_one(index):
#     connections[index].sendall("From specific connection".encode("utf-8"))

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.label1 = QLabel(self)
        self.label = QLabel(self)
        self.initUI()

    def initUI(self):
        # self.label.move(20, 20)
        self.label.setFixedSize(180, 15)
        self.label.move(2, 0)
        self.label1.setFixedSize(180, 15)
        self.label1.move(2, 18)
        # self.btn.clicked.connect(self.showDialog)

        # self.le = QLineEdit(self)
        # self.le.move(130, 22)

        self.setGeometry(400, 400, 290, 150)
        self.setWindowTitle('Game Room')
        self.label1.setText("List of Connected Clients:")
        self.show()

    def setLabel(self, ip, port):
        self.label.setText("SERVER IP: " + str(ip) + ":" + str(port))


def threaded_function(arg):
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    connections.append(connection)

    try:
        i = 2
        # Receive the data in small chunks and retransmit it
        while i >= 0:
            data = connection.recv(160).decode('utf-8')
            if data:
                connection.sendall((str(data) + ", You are connected!").encode("utf-8"))
                clients.append(str(data))
                # connection.sendall("LOLOLOLOL".encode("utf-8"))
            else:
                break
            i-=1
        ip_clients.append(str(client_address))

    finally:
        # Clean up the connection
        connection.close()

    print(ip_clients)
    print(clients)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    thread = Thread(target=threaded_function, args=(10,))
    thread.start()
    print(ip)
    ex.setLabel(ip, port)
    print("thread finished...exiting")
    sys.exit(app.exec_())
