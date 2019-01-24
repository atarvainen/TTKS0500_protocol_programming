import socket

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

sock.sendto("Terve",("localhost",8888))

#(msg, addr) = sock.recvfrom(1024)

#print msg

