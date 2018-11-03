from worker.queue_worker import QueueWorker


class TestWorker(QueueWorker):
    def __init__(self, workload):
        super().__init__(workload)

    def run(self):
        print("worker: ", self.id)

        while self.workload.has_next():
            print(self.workload.next(), end=' ')
        print('\n')
