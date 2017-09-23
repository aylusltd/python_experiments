import socket
import time

TCP_IP = '127.0.0.1'
OUTBOUND_IP = '127.0.0.1'
TCP_PORT = 5005
LISTENING_PORT = 5006
BUFFER_SIZE = 1024
display_message = True

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
outbound = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
outbound.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def get_input():
    global OUTBOUND_IP
    global TCP_PORT
    global display_message
    global outbound

    start_time = time.time()
    t = time.time()
    if display_message:
        prompt = "What should we say?. \n"
    else:
        prompt = ""
    while t < start_time +10:
        message = raw_input(prompt)
        display_message = False

    outbound.connect(OUTBOUND_IP, TCP_PORT)

    


try:
    s.bind((TCP_IP, LISTENING_PORT))
except:
    print "Swapping ports"
    t = BROADCAST_PORT
    BROADCAST_PORT = LISTENING_PORT
    LISTENING_PORT = t
    s.bind(TCP_IP, LISTENING_PORT)
    


print "Server Listening"

while True:
    conn, addr = s.accept()
    data = conn.recv(BUFFER_SIZE)
    if data:
        print "received data:\n", data
        conn.send(message)  # echo
        conn.send("\n")
        conn.close()
s.close()
