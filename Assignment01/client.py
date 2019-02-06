import socket

def send_data(sock, data):
    try:
        msg = str(len(data)) + "\n" + data
        sock.sendall(msg)
        pass
    except Exception as e:
        raise

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect(("localhost",65432))

        send_data(s, 'Helou')
        pass
    except Exception as e:
        print("Error:" + str(e))

main()
