# validit metodit
VALIDMETHODS = [
    "LIST",
    "LISTRESPONSE",
    "ADD",
    "DONE",
    "SUCCESS",
    "ERROR"
    ]

ERROR_ADDFAILED = 1
ERROR_ITEMNOTFOUND = 2

class Message:

    def __init__(self, method, methodparams, body):
        if method not in VALIDMETHODS:
            raise InvalidMethodException()

        self.method = method
        self.methodparams = methodparams
        self.body = body
        self.bodylen = len(body)

def read_until_newline(client):
    line = ""
    while "\n" not in line:
        c = client.recv(1)
        if c == "":
            break
        line += c
    return line

def read_firstpart(client):
    firstpart = read_until_newline(client).strip()
    parts = firstpart.split(" ")

    if len(parts) < 3:
        return False
    
    method = parts[0]

    try:
        bodylen = int(parts[1])
    except TypeError:
        raise MalformedHeaderException("bodylen is not a number!")
    methodparams = parts[2:]

    return (method, bodylen, methodparams)

def read_body(client, bodylen):
    body = ""

    while len(body) < bodylen:
        data = client.recv(1024)
        if data == "":
            break
        body += data

    return body

def send_message(client, message):
    data = "%s %d %s\r\n%s" % (message.method, message.bodylen, message.methodparams, message.body)
    client.sendall(data)

class InvalidMethodException(Exception):

    def __init__(self, *args):
        msg = "Invalid Method Exception"
        self.msg = msg
        super(InvalidMethodException, self).__init__(msg, args)

class MalformedHeaderException(Exception):

    def __init__(self, *args):
        msg = "Malformed Header Exception"
        self.msg = msg
        super(MalformedHeaderException,self).__init__(msg,args)
