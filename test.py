from url_handling.queue import Queue
from url_handling.scheduler import Scheduler
from robot import Robot
from worker.image_worker import ImageWorker
import configuration

configuration.initialize("res/config.ini")

"""
queue = Queue.get_main_instance()
scheduler = Scheduler(configuration.WORKER_TYPE)

for i in range(0, 15000):
    queue.add(str(i))

# queue.read()
scheduler.create_workers()

scheduler.start_workers()
"""

worker = ImageWorker("url")

hash = worker.hash_img(
    worker.request("https://upload.wikimedia.org/wikipedia/commons/a/a2/Prei_bloeiend_winter_Farinto.jpg")["response"].content)

print(hash)
print(Robot.invalid_url("/"))

