import socket

def main():
    # create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    try:
        # bind the socket to an address and port
        sock.bind(("localhost", 65432))
        # start listening for new connections
        sock.listen(5)
        # wait for a client using accept()
        # accept() returns a client socket and the address from which
        # the client connected
        (client, addr) = sock.accept()
        print "Received a connection from", addr
        # read and print whatever the client sends us
        print read_msg(client)
        # send "hello world!" back to the client
        client.send("hello world!\n")
        # the server proram terminates after sending the reply
        pass
    except Exception as e:
        print("Error:" + str(e))

def read_length(socket):
    try:
        buffer = ""
        while True:
            tmp = socket.recv(1)
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

if __name__ == "__main__":
    main()
