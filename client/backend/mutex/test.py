from mutex import HemlockThread, Lock, lock, unlock
from time import sleep, time

# mutex = Lock()
l1 = Lock()


def increase(var, t):
    for i in range(10):
        # mutex.acquire()
        lock(l1, threads[t])
        temp = var['value']
        print(temp)
        sleep(0.0001)
        var['value'] = temp + 1
        unlock(l1, threads[t])
        # mutex.release()


count = {"value": 0}
threads = []
t1 = HemlockThread(target=increase, args=[count, 0])
t2 = HemlockThread(target=increase, args=[count, 1])
threads.append(t1)
threads.append(t2)
thread1 = t1.get_thread()
thread2 = t2.get_thread()
thread1.start()
thread2.start()
thread1.join()
thread2.join()
# t1 = Thread(target=increase, args=[count])
# t2 = Thread(target=increase, args=[count])
# t1.start()
# t2.start()
# t1.join()
# t2.join()
print(count)
