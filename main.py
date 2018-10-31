from url_handling.queue import Queue
from web.web_requests import WebRequester
from web.html_parser import HtmlParser
from web.crawler import Crawler
import configuration
from web.crawler_api import CrawlerAPI
import time

start_time = time.time()

configuration.initialize("res/config.ini")

queue = Queue.get_instance()
crawler = Crawler(int(configuration.CONFIG.get("CRAWLER", "reproductionRate")))

crawler.start()

api = CrawlerAPI.get_instance()

while not api.all_done():
    pass

queue.dump()
print("DONE in {}".format(time.time() - start_time))

