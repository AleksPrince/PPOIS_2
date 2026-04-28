import time


class GameTimer:
    def __init__(self, time_limit):
        self.time_limit = time_limit
        self.enabled = True
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def get_remaining(self):
        if not self.start_time:
            return self.time_limit

        elapsed = time.time() - self.start_time
        remaining = max(0, self.time_limit - elapsed)
        return int(remaining)

    def reset(self):
        self.start_time = None