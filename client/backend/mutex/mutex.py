from threading import Thread


class HemlockThread:
    def __init__(self, target, args):
        self.grant_value = None
        self.thread = Thread(target=target, args=args)

    def get_thread(self):
        return self.thread


class Lock:
    def __init__(self):
        # Initial value: None
        self.tail = None


def lock(l1, hemlock_thread):
    # lock is currently empty, append thread to it
    # print(f'{hemlock_counter} entering lock, value of l1 grant_value is {l1.tail}')
    atomic_if = (hemlock_thread, 0)
    atomic_else = (l1.tail, hemlock_thread)
    if l1.tail is None:
        # l1.tail = hemlock_thread
        # hemlock_thread.grant_value = 0
        l1.tail, hemlock_thread.grant_value = atomic_if
        # print(f'l1 is empty, {hemlock_counter} is appending to l1')
        return
    # lock is currently occupied by other thread, insert thread after lock
    else:
        hemlock_thread.grant_value, l1.tail = atomic_else
        # print(f'l1 is busy, {hemlock_counter} is appending to l1 and waiting.')
    # read the grant_value value of its predecessor
    next_grant_value = hemlock_thread.grant_value.grant_value
    while next_grant_value != l1:
        next_grant_value = hemlock_thread.grant_value.grant_value
        # print(f'{hemlock_counter} successor grant_value: {next_grant_value}')
    # Once neighbours grant_value value is l1, it means successor has completed critical section update.
    # Update neighbours grant_value value to 0
    # print(f'{hemlock_counter} updating predecessor grant_value to 0')
    hemlock_thread.grant_value.grant_value = 0
    # Set its own grant_value value to 0 and return from lock to access critical section
    # print(f'{hemlock_counter} updating own grant_value to 0')
    hemlock_thread.grant_value = 0
    return


def unlock(l1, hemlock_thread):
    # Hemlock thread sets its own grant_value to l1
    # print(f'{hemlock_counter} updating own grant_value to l1')
    hemlock_thread.grant_value = l1
    # Wait until its grant_value value gets reset to 0, or it is the only value in the lock
    # print(f'{hemlock_counter} waiting for own grant_value to update to 0')

    while hemlock_thread.grant_value != 0:
        # If the lock tail address is equal to the hemlock thread, this is the final thread in the queue
        # Set lock tail to None and stop waiting
        if l1.tail == hemlock_thread:
            l1.tail = None
            break
        continue
    # Once the value is reset to 0, it means its successor has acknowledged the unlock method, return
    # print(f'{hemlock_counter} own grant_value updated to 0, returning')
    return
