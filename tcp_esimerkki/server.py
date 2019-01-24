import socket

def server():
  sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)

  sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

  sock.bind(("localhost",8888))

  sock.listen(5)

  (client, address) = sock.accept()

  print "uusi yhteys osoitteesta", address

  print client.recv(1024)

  client.send("Moi vaan")

server()
