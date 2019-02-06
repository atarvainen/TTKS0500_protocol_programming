import socket

def read_length(socket):
    try:
        buffer = ""
        while True:
            tmp = socket.recv(1)
            if not tmp:
                break
            if tmp == "\n":
                break
            buffer += tmp
        return int(buffer)
        pass
    except Exception as e:
        raise

def read_msg(socket):
    try:
        buffer = ""
        length = read_length(socket)
        print("Incoming bytes: " + str(length))

        received = 0

        while received < length:
            data = socket.recv(1024)
            buffer += data
            received += len(data)

        return buffer
        pass
    except Exception as e:
        raise

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

    try:
        s.bind(("localhost",65432))
        s.listen(5)

        client, addr = s.accept()

        msg = read_msg(client)

        print("Message: " + msg)

        client.close()
        s.close()

        pass
    except Exception as e:
        print("Error:" + str(e))

main()
