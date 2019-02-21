# -*- coding: utf-8 -*-

# https://tools.ietf.org/html/rfc7231#section-4
VALID_HTTP_METHODS = [
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "TRACE",
    "OPTIONS",
    "CONNECT"
]

# Luodaan uusi luokka httprequestille. Keep it simple, ei oteta bodya mukaan ja lisätään muutama yksinkertainen tarkistus
class HttpRequest:
    # luokan konstruktori
    def __init__(self, method, resource="/", headers={}, body=None):
        self.method = method
        self.resource = resource
        self.headers = headers
        # https://tools.ietf.org/html/rfc7230#section-3
        # https://tools.ietf.org/html/rfc7230#section-3.1.1
        if method not in VALID_HTTP_METHODS:
            raise UnknownHttpMethodException("Invalid HTTP method!")
        else:
            print "HTTP method ok, continue"

        # https://tools.ietf.org/html/rfc7230#section-5.4
        if not "Host" in headers.keys(): # keys() metodi palauttaa listan kaikista dictin keystä
            raise NoHostHeaderException()
        else:
            print "Host header ok, continue"

    def write_to(self, f):
        print "write_to method running"
        f.write("%s %s HTTP/1.1\r\n" % (self.method, self.resource)) # https://tools.ietf.org/html/rfc7230#section-3.1.1
        write_headers(f, self.headers) # katso funktio alempaa
        f.write("\r\n")
        f.flush() # kutsutaan file-objectin flush() metodia joka tyhjentää bufferin ja pakottaa kirjoituksen file-objectiin ilman sen sulkemista ( normaalisti close() hoitaa tämän)
        print "request sent"

# Luodaan uusi luokka demonstroimaan http responsea
# tärkeä huomata että statusline eroaa requestlinestä

class HttpResponse:
    # luodaan luokan konstruktori
    def __init__(self, status_code, reason, body, headers = ()):
        self.status_code = status_code
        self.reason = reason
        self.body = body
        self.headers = headers

    # luodaan staattinen metodi responsen lukemiseen
    @staticmethod
    def read_from(f):
        status_code, reason = HttpResponse.read_statusline(f)
        headers = read_headers(f)
        body = "".join(f.readlines())
        return HttpResponse(status_code, reason, body, headers)

    def write_to(self, f):
        f.write("HTTP/1.1 %d %s\r\n" % (self.status_code, self.reason))
        write_headers(f, self.headers)
        f.write("\r\n")
        f.write("%s" % self.body)
        f.flush()

    # luodaan staattinen metodi statusline lukemiseen
    # annetaan parametrina fileobjecti
    # staattisia metodeja voidaan kutsua luokan nimellä ja metodilla
    @staticmethod
    def read_statusline(f):

        # readline metodi palautaa stringinä kaiken ennon \n merkkiä eli rivinvaihtoa ja myös SEN
        # siistitään merkkijonoa strip metodilla, joka poistaa ns. whitespacet alusta ja lopusta
        # jolloin jäljelle jää oikea statusline
        status_line = f.readline().strip()

        # split metodi palauttaa listan kaikista stringin osista erotinmerkkinä eroteltuna
        parts = status_line.split(" ")
        print len(parts)

        # tarkistetaan itemien määrä f vastaako RFC:tä
        # voi olla useampi osa koska käytetään välilyöntiä erotinmerkkinä
        if len(parts) < 3:
            print "MalformedStatusLine"

        version = parts[0]

        # tarkistetaan että on oikea http versio
        if version != "HTTP/1.1":
            print "UnsupportedHTTPVersion"

        # koitetaan muuntaa statuscode str -> int
        try:
            status_code = int(parts[1])
        except ValueError:
            print "Not a number"

        # mikäli reason koostuu useammasta ostasta yhdistetään taulukon arvot
        # merkkijonoa käyttäen join metodilla
        # lopuksi siistitään turhat whitespacet (alussa)
        reason = " ".join(parts[2:])

        return (status_code, reason)


# Write_headers funktio. tarkoituksena kirjoittaa headerit file-objectiin oikeassa syntaksissa
# funktio lukee objectin luonnin yhteydessä annetut headerit (katso ylempää) ja palauttaa/kirjoittaa toistorakenteessa ne file-objectiin
# kutsutaan write_to metodissa (ylempänä)
def write_headers(f, headers):
    print "write_headers method"
    for header,value in headers.iteritems():
        f.write("%s: %s\r\n" % (header, value))

# funktio headereitten lukemiseen file objektista
def read_headers(f):
    headers = {}

    for rawline in f:
        line = rawline.strip()
        if line == " ":
            break

        parts = line.split(":")
        if len(parts) < 2:
            print "MalformedHTTPHeader"

        key = parts[0].strip()
        value = ":".join(parts[1:]).strip()
        headers[key] = value

    return headers

# Luodaan "uudet poikkeukset", pass keywordin avulla saadaan esimerkki ajettua viakka luokat eivät sisällä toiminnallisuutta
# Pythonin code blockit eivät saa olla ikinä tyhjiä (if,except,def, class jne.)
class UnknownHttpMethodException(Exception):
    pass

class NoHostHeaderException(Exception):
    pass
