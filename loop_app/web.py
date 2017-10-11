#########################################################################
# Iterative server - webserver3b.py                                     #
#                                                                       #
# Tested with Python 2.7.9 & Python 3.4 on Ubuntu 14.04 & Mac OS X      #
#                                                                       #
# - Server sleeps for 60 seconds after sending a response to a client   #
#########################################################################
import socket
import time

SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 5


def handle_request(client_connection):
    request = client_connection.recv(1024)
    # print(request.decode())
    http_response = b"""\
HTTP/1.1 469 FUCKYOU

Hello, World!
"""
    client_connection.sendall(http_response)
    # time.sleep(60)  # sleep and block the process for 60 seconds
    client_connection.close()
    return request

s = None


def serve_forever(handler = handle_request):
    global s
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    s = listen_socket
    # print('Serving HTTP on port {port} ...'.format(port=PORT))

    client_connection, client_address = listen_socket.accept()
    # client_connection.close()
    return handler(client_connection)

def close_socket():
    global s
    if s:
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect(SERVER_ADDRESS)
        m=  """\
            HTTP/1.1 200 OK

            Hello, World!

            """
        clientsocket.send(m)
        clientsocket.close()
        s.close()
        print "Socket closed"
        s=None


if __name__ == '__main__':
    serve_forever()