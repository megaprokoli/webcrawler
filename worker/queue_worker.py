from abc import abstractmethod
from robot import Robot


class QueueWorker(Robot):
    next_id = 0

    def __init__(self, workload):
        super().__init__()
        self.workload = workload

        self.id = QueueWorker.next_id
        QueueWorker.next_id += 1

    @abstractmethod
    def run(self):
        pass
