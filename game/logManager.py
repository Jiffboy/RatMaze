from collections import deque
from vars.globals import log_count


class LogManager:
    def __init__(self):
        self.log_queue = deque()

    def add_log(self, log):
        print(f"Adding log {log}")
        self.log_queue.append(log)
        if len(self.log_queue) > log_count:
            self.log_queue.popleft()

    def get_logs(self):
        return reversed(list(self.log_queue))
