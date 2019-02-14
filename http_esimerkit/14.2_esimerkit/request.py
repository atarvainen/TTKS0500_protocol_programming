# -*- coding: utf-8 -*-

# metodi-lista
# https://tools.ietf.org/html/rfc7231#section-4

HTTP_VALID_METHODS = [
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "TRACE",
    "OPTIONS",
    "CONNECT"
]

class HttpRequest:
    # Luokan konstruktori
    def __init__(self, method, resource="/", headers={}, body=None):
        self.method = method
        self.resource = resource
        self.headers = headers
        # https://tools.ietf.org/html/rfc7231#section-3

        if method not in HTTP_VALID_METHODS:
            raise UnknownHTTPMethodException("Invalid method")
        else:
            print "Request: Method was ok"

        if not "Host" in headers.keys(): #keys() palauttaa listan kaikista dictin keystä
            raise NoHostHeaderException()
        else:
            print "Request: Host header was ok"
        # https://tools.ietf.org/html/rfc7230#section-5.4

    def write_to(self, f):
        print "Request: Request's write method"
        # https://tools.ietf.org/html/rfc7230#section-3.1.1
        f.write("%s %s HTTP/1.1\r\n" % (self.method, self.resource))
        write_header(f, self.headers)
        f.write("\r\n")
        f.flush() # Tyhjentää bufferin, eli pakottaa kirjoituksen file objektiin ilman sen sulkemista
        print "Request lähetetty"

def write_header(f, headers):
    print "write_headers"
    for header, value in headers.iteritems():
        f.write("%s: %s\r\n" % (header, value))

class UnknownHTTPMethodException(Exception):
    pass

class NoHostHeaderException(Exception):
    pass
    # code blockit ei saa olla tyhjiä, siksi pass-keyword
