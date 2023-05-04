from threading import Thread, current_thread, Condition


class HemlockThread(Thread):
    def __init__(self, target, args):
        super().__init__()
        self.grant_value = None
        self.target = target
        self.args = args

    def run(self):
        self.target(*self.args)


class Lock:
    def __init__(self):
        # Initial value: None
        self.tail = None
        self.condition = Condition()

    def lock(self):
        hemlock_thread = current_thread()
        # print(f"thread {hemlock_thread} entered lock")
        # lock is currently empty, append thread to it
        # print(f'{hemlock_counter} entering lock, value of self grant_value is {self.tail}')
        atomic_if = (hemlock_thread, None)
        atomic_else = (self.tail, hemlock_thread)
        
        if self.tail is None:
            # self.tail = hemlock_thread
            # hemlock_thread.grant_value = None
            self.tail, hemlock_thread.grant_value = atomic_if
            # print(f"self is empty, {hemlock_counter} is appending to self")
            return
        # lock is currently occupied by other thread, insert thread after lock
        else:
            hemlock_thread.grant_value, self.tail = atomic_else
            # print(f"self is busy, {hemlock_counter} is appending to self and waiting.")
        # read the grant_value value of its predecessor

        predecessor = hemlock_thread.grant_value
        with self.condition:
            while predecessor.grant_value != self:
                self.condition.wait()
        #     next_grant_value = hemlock_thread.grant_value.grant_value
            # print(f"{hemlock_counter} successor grant_value: {next_grant_value}")
        # Once neighbours grant_value value is self, it means successor has completed critical section update.
        # Update neighbours grant_value value to None
        # print(f"{hemlock_counter} updating predecessor grant_value to None")
        with self.condition:
            predecessor.grant_value = None
            self.condition.notify_all()
        # Set its own grant_value value to None and return from lock to access critical section
        # print(f"{hemlock_counter} updating own grant_value to None")
        predecessor = None
        return

    def unlock(self):
        hemlock_thread = current_thread()
        # If the lock tail address is equal to the hemlock thread, this is the final thread in the queue
        # Set lock tail to None and stop waiting
        if self.tail == hemlock_thread:
            self.tail = None
            return
        
        # Hemlock thread sets its own grant_value to self
        # print(f"{hemlock_counter} updating own grant_value to self")
        with self.condition:
            hemlock_thread.grant_value = self
            self.condition.notify_all()
        # Wait until its grant_value value gets reset to None, or it is the only value in the lock
        # print(f"{hemlock_counter} waiting for own grant_value to update to None")
        with self.condition:
            while hemlock_thread.grant_value is not None:
                self.condition.wait()
        # self.condition.wait_for(predicate=lambda: hemlock_thread.grant_value is None)
        # Once the value is reset to None, it means its successor has acknowledged the unlock method, return
        # print(f"{hemlock_counter} own grant_value updated to None, returning")
        return
