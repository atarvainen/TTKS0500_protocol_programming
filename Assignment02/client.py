import socket

def send(sock, data):
    try:
        data_len = len(data)
        send_data(sock, str(data_len)+"\n")
        send_data(sock, data)

        pass
    except Exception as e:
        raise

def send_data(sock, data):
    try:
        total = 0
        while total < len(data):
            sent = sock.send(data[total:])
            total += sent

        print("Sent %d bytes" % total)

        pass
    except Exception as e:
        raise

try:
    # create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server (in this case on the same machine)
    s.connect(("localhost", 65432))

    # send "hello" to server

    send(s, "hello world")

    # print whatever server sends back.
    print s.recv(1024),

    # close the socket and exit the program
    s.close()
    pass
except Exception as e:
    print("Error:" + str(e))
