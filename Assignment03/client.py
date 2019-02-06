import socket
import argparse

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

parser = argparse.ArgumentParser(description='Send a message')
parser.add_argument('-a','--address', help='Address', required=True)
parser.add_argument('-p','--port', help='Port', required=True)
args = vars(parser.parse_args())
addr = args['address']
port = args['port']

try:
    # connect to server (in this case on the same machine)
    s.connect((addr, int(port)))
except:
    print("Cannot connect to server")

try:
    # send "hello" to server
    s.send("hello world")
except:
    print("Sending data to the server failed")

try:
    # print whatever server sends back.
    print s.recv(1024)
except:
    print("No response from server")

# close the socket and exit the program
s.close()
