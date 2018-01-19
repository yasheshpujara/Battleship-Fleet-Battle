import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
port = 10010
s.close()

print("IP address of server is " + str(ip) + ":" + str(port))

# Bind the socket to the port
server_address = (ip, port)
# print('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    # print(str(client_address) + " Connected!")

    try:
        # print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(160)
            print(str(data) + " Connected!")
            if data:
                # print >>sys.stderr, 'sending data back to the client'
                connection.sendall(str(data) + ", You are connected!")
            else:
                # print >>sys.stderr, 'no more data from', client_address
                break

    finally:
        # Clean up the connection
        connection.close()
