import socket

osoite = "localhost"
portti = 8888
sijainti = "/home/student/"

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

    s.bind((osoite,portti))
    s.listen(5)

    print "serveri on paalla"

    while True:
        client, addr = s.accept()
        filename = client.recv(1)
        while not "\n" in filename:
            filename += client.recv(1)

        filename = filename.strip()
        print len(filename), filename

        kuva = open(sijainti+"cat2.jpg", "wb")

        data = client.recv(1024)

        while data:
            kuva.write(data)
            data = client.recv(1024)

        print "kuva tuli perille"

        kuva.close()

main()
