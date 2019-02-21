# -*- coding: utf-8 -*-
import socket
from request import HttpRequest, HttpResponse
import sys


def main():

    # määritellään socketin sekä headerin host
    host = "httpbin.org"

    # luodaan uusi socket-objecti (ipv4/tcp)
    sukka = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sukka.connect((host, 80))

    req = HttpRequest("GET", "/", headers={"Host": host, "Connection": "close"})

    # Luodaan aikaisemmin luodun socket-objectin avulla uusi f-niminen fileobjecti makefile() metodia käyttäen
    # makefile() metodi palauttaa siis uuden fileobjectin joka on sidottu socket-objectiin
    f = sukka.makefile()
    req.write_to(f)
    # Kutsutaan HttpRequest-luokassa määriteltyä metodia write_to() (huomaa että ollaan käytetty write() send() sijaan)
    # ts. read and write käännetään sisäisesti send ja recv kutsuiksi

    # tulostellaan kaikki mitä serveri oksentaa takaisin, koska meillä on vain request-toiminnallisuus
    #for line in f:
    #    print line

    '''
    response = HttpResponse.read_from(f)
    print response.status_code
    print "**************************************Tästä alkaa responsen body ***************************************"
    print response.body
    '''

    response = HttpResponse(200, "OK", "Helou\n", headers={"Host": "localhost"})
    response.write_to(sys.stdout)

    # suljetaan file- sekä socket-objecti
    f.close()
    sukka.close()


main()
