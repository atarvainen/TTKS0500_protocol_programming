# -*- coding: utf-8 -*-

from request import HttpRequest
import socket

def main():
    host = "httpbin.org"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,80))

    req = HttpRequest("GET", "/", headers={"Host": host, "Connection": "close"})

    f = s.makefile()
    req.write_to(f)

    for line in f:
        print line

    f.close()
    s.close()

main()
