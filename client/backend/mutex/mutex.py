from threading import Thread


class HemlockThread:
    def __init__(self, target, args):
        self.grant = None
        self.thread = Thread(target=target, args=args)

    # def swap(self, tail):
    #     self.grant = tail

    def get_thread(self):
        return self.thread


class Lock:
    def __init__(self):
        self.value = 1
        self.tail = None

    def swap(self, thread):
        if self.tail is None:
            self.tail = thread
            return 0
        else:
            prev = self.tail
            self.tail = thread
            return prev


def lock(l1, thread):
    # l1.tail = thread.swap(l1.tail)
    thread.grant = l1.swap(thread)
    if thread.grant == 0:
        return
    while thread.grant != 0:
        if thread.grant == 0:
            break
            # thread.thread.start()  # access critical section
    return
    # thread.grant = 0
    # unlock(l1, thread)


def unlock(l1, thread):
    thread.grant = 0
    if l1.tail == thread:
        l1.tail = None  # lock has been completely released

