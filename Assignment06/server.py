import socket
import threading
import protocol
import os
import argparse
import time

# argparse for using command line arguments
parser = argparse.ArgumentParser(description='TLDP client')
parser.add_argument('-a','--address', help='Address', required=True)
parser.add_argument('-p','--port', help='Port', required=True)
parser.add_argument('-f','--file', help='Filepath', required=True)
args = vars(parser.parse_args())
server_addr = args['address']
server_port = args['port']
filepath = args['file']

lock = threading.Lock()

# list all items in file and send to client
def listItems( c, name ):
    lock.acquire()
    #print("thread %s locking" % name)
    with open(filepath, "r") as f:
        todo = f.readlines()
    # sleep to test locks
    #time.sleep(3)
    lock.release()
    #print("thread %s released lock" % name)
    # add numbers 1) etc to todo list items
    if len(todo) > 0:
        list = []
        for idx, listitem in enumerate(todo):
            list.append(str(idx) + ") " + listitem)

        body = '\r\n'.join(list)
        listLen = len(todo)
    else:
        listLen = 0
        body = ""

    response = protocol.Message("LISTRESPONSE", listLen, body)
    return response

# remove item with index sent from client, respond with success or error
# different locks for writing and reading
def removeItem( c, r, name ):
    try:
        lock.acquire()
        #print("thread %s locking" % name)
        with open(filepath, "r") as f:
            lines = f.readlines()
        #time.sleep(3)
        lock.release()
        #print("thread %s released lock" % name)

        if len(lines) > r:
            lock.acquire()
            #print("thread %s locking" % name)
            with open(filepath, "w") as f:
                for idx, line in enumerate(lines):
                    if idx != r:
                        f.write(line)
                    else:
                        print("Removed task: %s" % line)
            #time.sleep(3)
            lock.release()
            #print("thread %s released lock" % name)
            response = protocol.Message("SUCCESS", 0, "")
            return response
        else:
            error_response = protocol.Message("ERROR", protocol.ERROR_ITEMNOTFOUND, "")
            return error_response

    except Exception as e:
        print(e)
        error_response = protocol.Message("ERROR", protocol.ERROR_ITEMNOTFOUND, "")
        return error_response

# add item to the end of the file, respond with success or error
def addItem( c, data, name):
    try:
        lock.acquire()
        #print("thread %s locking" % name)
        with open(filepath, "a+") as f:
            f.write("%s\n" % data)
        #time.sleep(3)
        lock.release()
        #print("thread %s released lock" % name)

        #print("Added task: %s" % data)
        response = protocol.Message("SUCCESS", 0, "")
        return response

    except Exception as e:
        print(e)
        error_response = protocol.Message("ERROR", protocol.ERROR_ADDFAILED, "")
        return error_response

# thread for handling each client connection
def handleConnection( c ):
    name = threading.currentThread().getName()
    while True:

        try:
            # false is returned from protocol if client closes connection
            parts = protocol.read_firstpart(c)
            if parts != False:
                if parts[0] == "LIST" and parts[1] > 0:
                    print("malformed bodylength")
                    c.close()
                else:
                    if parts[0] == "LIST":
                        response = listItems(c, name)
                        protocol.send_message(c, response)

                    elif parts[0] == "ADD":
                        body = protocol.read_body(c, parts[1])
                        response = addItem(c, body, name)
                        protocol.send_message(c, response)

                    elif parts[0] == "DONE":
                        response = removeItem(c, int(parts[2][0]), name)
                        protocol.send_message(c, response)
            else:
                break

        except protocol.InvalidMethodException:
            print("Received malformed header from the client")
    
    print("Closing client connection to %s" % name)
    c.close()

def Main():
    # file is created if it doesn't exist
    try:
        f = open(filepath, 'w+')
        f.close()
    except:
        print("Failed creating file")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((server_addr,int(server_port)))
    s.listen(10)
    threads = []

    # create threads for each client
    while True:
        c, (c_addr, c_port) = s.accept()

        print("Client connected from %s") % c_addr

        t = threading.Thread(target=handleConnection, args=(c,))
        threads.append(t)
        t.start()

if __name__ == '__main__':
    Main()