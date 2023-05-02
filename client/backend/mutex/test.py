from mutex import HemlockThread, Lock, lock, unlock
from time import sleep, time

# mutex = Lock()
l1 = Lock()


def increase(var, h):
    for i in range(10):
        # mutex.acquire()
        print(f'Entering {i} lock for {h}')
        lock(l1, hemlocks[h], h)
        temp = var['value']
        print(temp)
        # sleep(1)
        var['value'] = temp + 1
        unlock(l1, hemlocks[h], h, i)
        print(f'Exiting {i} unlock for {h}')
        # mutex.release()


count = {"value": 0}
hemlocks = []
h1 = HemlockThread(target=increase, args=[count, 0])
h2 = HemlockThread(target=increase, args=[count, 1])
h3 = HemlockThread(target=increase, args=[count, 2])
h4 = HemlockThread(target=increase, args=[count, 3])
hemlocks.append(h1)
hemlocks.append(h2)
hemlocks.append(h3)
hemlocks.append(h4)
thread1 = h1.get_thread()
thread2 = h2.get_thread()
thread3 = h3.get_thread()
thread4 = h4.get_thread()
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread1.join()
thread2.join()
thread3.join()
thread4.join()
# t1 = Thread(target=increase, args=[count])
# t2 = Thread(target=increase, args=[count])
# t1.start()
# t2.start()
# t1.join()
# t2.join()
print(count)
