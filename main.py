from url_handling.queue import Queue
from web.web_requests import WebRequester
from web.html_parser import HtmlParser
from web.crawler import Crawler
from constants import CONFIG
from web.crawler_api import CrawlerAPI
import time

start_time = time.time()

config = CONFIG
queue = Queue.get_instance()

crawler = Crawler()
crawler.start()

api = CrawlerAPI.get_instance()

while not api.all_done():
    pass

queue.dump()
print("DONE in {}".format(time.time() - start_time))    # 0.412994384765625

