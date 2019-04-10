#import thread
import threading
import time
import Queue


def service1():
    print threading.currentThread().getName(), " Kaynnistyy"
    time.sleep(1)
    print threading.currentThread().getName(), " Sulkeutuu"

def main():
    thread1 = threading.Timer(5, service1)
    thread2 = threading.Thread(name="own_thread", target=service1)

    thread1.start()
    thread2.start()

main()

#def own_thread2(q):
#    Lock.acquire([q])
#    for x in range(5):
#        q.put("thread2")
#        time.sleep(1)
#    Lock.release()

#def own_thread(q):
#    Lock.acquire([q])
#    for x in range(5):
#        q.put("thread1")
#        time.sleep(1)
#    Lock.release()

#def main():
#    q = Queue.Queue()

#    thread = threading.Thread(target=own_thread, args=(q,))
#    thread2 = threading.Thread(target=own_thread2, args=(q,))

#    thread.start()
#    thread2.start()

#    for x in range(10):
#        msg = q.get()
#        print(msg)

main()
