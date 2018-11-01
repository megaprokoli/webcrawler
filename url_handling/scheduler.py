from url_handling.queue import Queue
from configuration import CONFIG


class Scheduler:

    def __init__(self):
        self.thread_count = int(CONFIG.get("WORKER", "threads"))

        self.workers = list()
        self.subqueues = list()

    def create_workers(self):
        last_index = 0
        url_list = Queue.get_main_instance().gathered_links
        length = len(url_list)
        subqueue_size = int(length / self.thread_count)

        for i in range(0, self.thread_count):
            chunk = last_index + subqueue_size
            self.subqueues.append(Queue(url_list[last_index:chunk]))
            last_index = chunk

        self.subqueues[-1].gathered_links += url_list[last_index:]
