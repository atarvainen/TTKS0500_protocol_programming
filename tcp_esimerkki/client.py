import socket

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)

sock.connect(("localhost",8888))

sock.send("Terve")

print sock.recv(1024)

sock.close()
