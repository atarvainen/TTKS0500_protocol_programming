import threading
import time
import logging

total = 0
lock = threading.Lock()

logging.basicConfig(level=logging.DEBUG, format="(%(threadName)s %(message)s)")
def kasvata_summaa(summa):
    global total
    lock.acquire()
    logging.debug("lukko asetettu")
    try:
        total += summa
    finally:
        print total
        lock.release()
        logging.debug("lukko vapautettu")

def main():
    print "hello"
    for x in range(10):
        oma_threadi = threading.Thread(target=kasvata_summaa, args=(5,))
        oma_threadi.start()
        time.sleep(1)

main()
