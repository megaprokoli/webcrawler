import random
import threading
from url_handling.queue import Queue
from web.html_parser import HtmlParser
from web.crawler_api import CrawlerAPI
from web.web_requests import WebRequester
from constants import CONFIG


class Crawler(threading.Thread):
    id = 0

    def __init__(self, reproduction_rate=int(CONFIG.get("CRAWLER", "reproductionRate"))):
        super().__init__()

        self.last_pos = None
        self.current_pos = None
        self.current_content = list()
        self.current_urls = list()
        self.parser = HtmlParser()
        self.reproduced = False
        self.requester = WebRequester()
        self.die_reason = "unknown"

        self.id = Crawler.id
        Crawler.id += 1

        self.start_url = CONFIG.get("CRAWLER", "startUrl")
        self.reproduction_rate = reproduction_rate
        self.per_page = int(CONFIG.get("CRAWLER", "reproductionPerPage"))
        self.hop_count = int(CONFIG.get("CRAWLER", "hopCount"))

        CrawlerAPI.get_instance().register(self)

    def run(self):
        print("started {}".format(self.id))

        lock = threading.Lock()
        self.current_pos = self.start_url
        self.request(self.start_url)

        while self.hop_count >= 0:

            if self.no_robots():
                self.die_reason = "no robots allowed"
                break

            self.gather_links()
            self.filter()   # filter invalid urls

            if len(self.current_urls) < 1:
                self.die_reason = "no urls found"
                break   # TODO go to last pos

            if self.reproduced:
                next_url = self.current_urls[random.randint(0, len(self.current_urls) - 1)]
            else:
                self.reproduce()
                next_url = self.current_urls[-1]    # remaining url after reproduce

            # UPDATE POSITIONS
            self.last_pos = self.current_pos
            self.current_pos = next_url

            # ADD URLs
            with lock:
                [(lambda url: Queue.get_instance().add(url))(url) for url in self.current_urls]

            self.request(self.current_pos)
            self.hop_count -= 1

        CrawlerAPI.get_instance().check_out(self.id)
        print("Crawler {} died at {}  reason: {}".format(self.id, self.hop_count, self.die_reason))

    def filter(self):
        for i in range((len(self.current_urls) - 1) * -1, 0):
            if Crawler.invalid_url(self.current_urls[i]):
                self.current_urls.pop(i)


    @staticmethod
    def invalid_url(url):
        split_url = url.split(":")
        # print(split_url, not (split_url[0] == "https" or split_url[0] == "http"))

        return not (split_url[0] == "https" or split_url[0] == "http")

    def request(self, url):     # TODO handle 404
        response = self.requester.exec_url(url)
        self.parser.feed(str(response.content))
        self.current_content = self.parser.lsStartTags

    def reproduce(self):
        if self.reproduced or self.reproduction_rate == 0:
            return

        if self.per_page > len(self.current_urls):
            counter = len(self.current_urls)
        else:
            counter = self.per_page

        i = 0
        while i < counter:  # -1 so this crawler has an url
            new_crawler = Crawler(reproduction_rate=self.reproduction_rate - 1)
            new_crawler.start()
            i += 1
        self.reproduced = True

    def no_robots(self):
        return False

    def gather_links(self):
        self.current_urls = list()

        for tag in self.current_content:
            if tag.tag == "a":
                self.current_urls.append(tag.attrs[0][1])   # [("href", url)]
