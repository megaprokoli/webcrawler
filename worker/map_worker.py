from worker.queue_worker import QueueWorker


class MapWorker(QueueWorker):
    def __init__(self, workload):
        super().__init__(workload)

    def run(self):
        for url in self.workload:
            print(url)
