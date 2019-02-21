'''
Määrittele hyväksytyt metodit

requestline = "GET / HTTP/1.1"

tarkista requestlinestä:

--> elementtien määrä
--> että annetut metodi on tunnettu
--> tuettu http-versio

--> palauta funktiolta metodi,target,versio


tarkista että version syntaksi on oikein
--> ainostaan HTTP hyväksytään
--> sisältää /

testaa toimivuus requestlinen avulla
'''

import sys
requestline = "GET / HTTP/1.1"


# Valid HTTP method defined in RFC7231 Section 4
VALID_HTTP_METHODS = [
        "GET",
        "HEAD",
        "POST",
        "PUT",
        "DELETE",
        "OPTIONS",
        "TRACE"
]



# Parses a HTTP request-line according to RFC7230.
# Takes the request-line string as the only parameter.
# Returns a tuple containing method, resource and http version.
# Raises a MalformedRequestLineException or MalformedHTTPVersionException if
# the given line is not a valid HTTP request-line
def parse_request_line(line):
        parts = line.split(" ")
        if len(parts) != 3:
                print "MalformedRequestLine"
                sys.exit()
	# (method, resource, version) = parts
        method = parts[0]
        resource = parts[1]
        version = parts[2]

        if method not in VALID_HTTP_METHODS:
                raise UnknowHTTPMethod("Unknow method")

        validate_http_version(version)

        return (method, resource, version)

# Validates the HTTP version found in status-line or request-line.
# Raises a MalformedHTTPVersionException if the given version is not valid.
def validate_http_version(version):
        if "/" not in version:
                print "MalformedHTTPVersion"
        name, number = version.split("/")

	# "HTTP" is the only valid value for name
        if name != "HTTP":
                print "MalformedHTTPVersion"

	# According to the RFC, the version should contain two numbers separated by
	# a dot. If the dot is not there, the version part cannot be valid.
        if "." not in number:
                print "MalformedHTTPVersion"

	# Both values separated by the dot have to numbers. If they are not, the
	# HTTP version part cannot be valid.
        first, second = number.split(".")
        if not first.isdigit() or not second.isdigit():
                print "MalformedHTTPVersion"

class UnknowHTTPMethod(Exception):
        pass


print parse_request_line(requestline)

requestline2 = "ASD / HTTP/1.1"

print parse_request_line(requestline2)
