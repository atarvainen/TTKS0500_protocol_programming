import socket
import protocol
import sys
import shutil
import os

try:
    # Python 3
    from urllib.parse import urlsplit, urlunsplit
except ImportError:
    # Python 2
    from urlparse import urlsplit, urlunsplit

server_addr = "localhost"
server_port = 65432
server_datadir = "data/"


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((server_addr,server_port))
    s.listen(10)

    while True:
        client, (client_addr, client_port) = s.accept()
        print("Client connected from %s") % client_addr

        try:
            (method, bodylen, methodparams) = protocol.read_firstpart(client)
            body = ""
            if method == "LIST" and bodylen > 0:
                print("malformed bodylength")
                client.close()
            else:
                if bodylen > 0:
                    body = protocol.read_body(client, bodylen)
                re = protocol.Message(method, methodparams, body)
                response = handle_request(re,client)
                protocol.send_message(client, response)
        except protocol.InvalidMethodException:
            print("received malformed header from the client")

        client.close()

def resolve_path(path):
    parts = list(urlsplit(path))
    segments = parts[2].split('/')
    segments = [segment + '/' for segment in segments[:-1]] + [segments[-1]]
    resolved = []
    for segment in segments:
        if segment in ('../', '..'):
            if resolved[1:]:
                resolved.pop()
        elif segment not in ('./', '.'):
            resolved.append(segment)
    parts[2] = ''.join(resolved)
    return urlunsplit(parts)


def handle_request(re,client):
    if re.method == "DOWNLOAD":
        filename = re.methodparams[0]
        print(filename)
        try:
            f = open(server_datadir+filename, "r")
            body = "".join(f.readlines())
            print(body)
            #body = f.read()
            response = protocol.Message("FILE", filename, body)
            return response
        except Exception as e:
            print(e)
            error_response = protocol.Message("ERROR", protocol.ERROR_FILENOTFOUND, "")
            return error_response
    elif re.method == "LIST":
        filepath = resolve_path(server_datadir + re.methodparams[0])
        #filepath = server_datadir + re.methodparams[0]
        try:
            if os.path.isdir(filepath):
                files = os.listdir(filepath)
                filesLen = 0
                if len(files) > 0:
                    body = '\r\n'.join(files)
                    filesLen = len(files)
                else:
                    body = 0
                print(body)
                response = protocol.Message("LISTRESPONSE", filesLen, body)
                return response
            else:
                print("error")
                error_response = protocol.Message("ERROR", protocol.ERROR_BADFOLDER, "")
                return error_response
        except Exception as e:
            print(e)
            error_response = protocol.Message("ERROR", protocol.ERROR_FILENOTFOUND, "")
            return error_response
    else:
        print("something went wrong!")

main()
