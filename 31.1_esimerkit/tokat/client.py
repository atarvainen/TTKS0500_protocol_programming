import socket
osoite = "localhost"

portti = 8888
tiedosto = "/home/student/Downloads/cat.jpg"

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((osoite, portti))
    s.send(tiedosto+"\n")

    kuva = open(tiedosto, 'rb')

    data = kuva.read(1024)

    while data:
        s.send(data)
        data = kuva.read(1024)

    print "Kuva lahetetty onnistuneesti"

    kuva.close()
    s.close()

main()
