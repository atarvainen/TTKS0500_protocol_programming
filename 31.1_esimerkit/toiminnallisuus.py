def send_data(socket, data):
    total = 0
    while total < len(data):
        sent = socket.send(data[total:])
        total += sent
    print "Sent %d bytes" % total

def send_msg(socket, data):
    data_len = len(data)
    send_data(socket, str(data_len)+"\n")
    send_data(socket, data)

def read_length(socket):
    buffer = ""
    while True:
        tmp = socket.recv(1)
        if tmp == "\n":
            break
        buffer += tmp
    return int(buffer)

def read_msg(socket):
    buffer = ""
    length = read_length(socket)
    print "Incoming bytes: ", length

    received = 0

    while received < length:
        data = socket.recv(1024)
        buffer += data
        received += len(data)

    return buffer
