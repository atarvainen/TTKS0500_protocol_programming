import socket
import argparse
import thread, time

def input_thread(L):
    raw_input()
    L.append(None)

def main():
    # create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

    parser = argparse.ArgumentParser(description='Receive a message')
    parser.add_argument('-a','--address', help='Address', required=True)
    parser.add_argument('-p','--port', help='Port', required=True)
    args = vars(parser.parse_args())
    addr = args['address']
    port = args['port']
    try:
        # bind the socket to an address and port
        sock.bind((addr, int(port)))
        # start listening for new connections
        sock.listen(5)
        L = []
        thread.start_new_thread(input_thread, (L,))
        while True:
            # wait for a client using accept()
            # accept() returns a client socket and the address from which
            # the client connected
            (client, addr) = sock.accept()
            print "\n", "Received a connection from", addr
            # read and print whatever the client sends us
            print client.recv(1024),
            # send "hello world!" back to the client
            client.send("hello world!\n")
            time.sleep(.1)
            if L:
                print("breaking")
                break
    except KeyboardInterrupt:
        print("Server closed")
    except Exception as e:
        print("Error" + str(e))

if __name__ == "__main__":
    main()
