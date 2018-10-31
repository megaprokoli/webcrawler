from abc import abstractmethod, ABC


class QueueWorker(ABC):

    def __init__(self, workload):
        super().__init__()
        self.workload = workload
