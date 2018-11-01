from url_handling.queue import Queue
from url_handling.scheduler import Scheduler
import configuration

configuration.initialize("res/config.ini")

queue = Queue.get_main_instance()
scheduler = Scheduler()

# for i in range(0, 100):
    # queue.add(str(i))

queue.read()
scheduler.create_workers()

print(len(queue.gathered_links))

for sub in scheduler.subqueues:
    print(len(sub.gathered_links), " ", sub.gathered_links)
