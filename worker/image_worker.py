from worker.queue_worker import QueueWorker
import hashlib


class ImageWorker(QueueWorker):

    def __init__(self, workload):
        super().__init__(workload)

        self.hash_func = hashlib.new("md5")

    def run(self):
        pass

    def hash_img(self, img):
        self.hash_func.update(img)
        return self.hash_func.hexdigest()
