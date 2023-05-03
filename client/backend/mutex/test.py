from mutex import HemlockThread, Lock
from time import sleep

# mutex = Lock()
l1 = Lock()


def increase(var):
    for i in range(10):
        # mutex.acquire()
        # l1.lock(hemlocks[h])
        # l1.lock(hemlocks[h])
        l1.lock()
        # lock(l1, hemlocks[h])
        temp = var['value']
        # print(temp)
        sleep(0.001)
        var['value'] = temp + 1
        # unlock(l1, hemlocks[h])
        # l1.unlock(hemlocks[h])
        l1.unlock()
        # mutex.release()


count = {"value": 0}
h1 = HemlockThread(target=increase, args=[count])
h2 = HemlockThread(target=increase, args=[count])
h3 = HemlockThread(target=increase, args=[count])
h4 = HemlockThread(target=increase, args=[count])
h1.start()
h2.start()
h3.start()
h4.start()
h1.join()
h2.join()
h3.join()
h4.join()
# t1 = Thread(target=increase, args=[count])
# t2 = Thread(target=increase, args=[count])
# t1.start()
# t2.start()
# t1.join()
# t2.join()
print(count)
