import socket
import threading

logging.basicConfig(filename="server.log", level=logging.DEBUG, format="%(levelname)s %(message)s")

def clientThread(client, addr):
    while True:
        data = client.recv(1024)
        reply = "OK"
        if not data:
            break;
        print data
        client.send(reply)
    client.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 8888)
s.listen(5)

while True:
    client, addr = s.accept()
    logging.debug("connected " + addr[0] + ":" + str(addr[1]))

    thread = threading.Thread(target=clientThread, args=(client, addr))
    thread.start()

s.close()
