import socket

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

sock.bind(("localhost",8888))

(msg, addr) = sock.recvfrom(1024)

print "%s , osoitteesta %s " % (msg,addr)

sock.sendto("Heip",addr)
