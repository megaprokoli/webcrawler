from url_handling.queue import Queue
from configuration import CONFIG


class Scheduler:

    def __init__(self, worker_type):
        self.thread_count = int(CONFIG.get("WORKER", "threads"))
        self.worker_type = worker_type

        self.workers = list()
        self.subqueues = list()

    def start_workers(self):
        for worker in self.workers:
            worker.start()

    def create_workers(self):
        last_index = 0
        url_list = Queue.get_main_instance().gathered_links
        length = len(url_list)

        if self.thread_count <= 0 or self.thread_count >= length:
            self.thread_count = int(length * 0.0005)

        print(self.thread_count)
        subqueue_size = int(length / self.thread_count)

        for i in range(0, self.thread_count):   # allocate equal pieces from url_list to the new workers
            chunk = last_index + subqueue_size
            self.workers.append(self.worker_type(Queue(url_list[last_index:chunk])))
            last_index = chunk

        self.workers[-1].workload.add(url_list[last_index:])   # fill the rest


