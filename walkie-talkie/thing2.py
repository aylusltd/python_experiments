import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT+1))
s.listen(5)
print "Server Listening"

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    # conn, addr = s.accept()
    # data = conn.recv(BUFFER_SIZE)
    # if not data: break
    # print "received data:\n", data
    message = raw_input("What should we say?. \n")
    # s.send(MESSAGE)
    m=  """\
        HTTP/1.1 200 OK

        Hello, World!
        """
    clientsocket.connect((TCP_IP, TCP_PORT))
    # clientsocket.send(m)
    clientsocket.send(message)  # echo
    clientsocket.send("\n")
    data=clientsocket.recv(BUFFER_SIZE)
    print "They Said:"
    print data
    clientsocket.close()
