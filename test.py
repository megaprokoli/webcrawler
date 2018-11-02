from url_handling.queue import Queue
from url_handling.scheduler import Scheduler
import configuration

configuration.initialize("res/config.ini")

queue = Queue.get_main_instance()
scheduler = Scheduler(configuration.WORKER_TYPE)

for i in range(0, 15000):
    queue.add(str(i))

# queue.read()
scheduler.create_workers()

scheduler.start_workers()
