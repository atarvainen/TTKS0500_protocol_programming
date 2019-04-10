import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 8888))

while True:
    try:
        msg = raw_input("Anna viesti: ")
        s.send(msg)
        print s.recv(1024)
    except KeyboardInterrupt:
        s.close()
