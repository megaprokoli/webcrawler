import random
import threading
from url_handling.queue import Queue
from web.crawler_api import CrawlerAPI
from configuration import CONFIG
from robot import Robot


class Crawler(Robot):
    id = 0

    def __init__(self, reproduction_rate, start_url=None):
        super().__init__()

        self.last_pos = None
        self.current_pos = None
        self.current_urls = list()
        self.reproduced = False
        self.die_reason = "unknown"

        self.id = Crawler.id
        Crawler.id += 1

        self.reproduction_rate = reproduction_rate
        self.per_page = int(CONFIG.get("CRAWLER", "reproductionPerPage"))
        self.hop_count = int(CONFIG.get("CRAWLER", "hopCount"))
        self.retries = int(CONFIG.get("CRAWLER", "retries"))

        if start_url is None:
            self.start_url = CONFIG.get("CRAWLER", "startUrl")
        else:
            self.start_url = start_url

        CrawlerAPI.get_instance().register(self)

    def run(self):
        lock = threading.Lock()
        self.current_pos = self.start_url
        self.request(self.start_url)    # TODO fix url=/ isnt filtered

        print("started {} at {}".format(self.id, self.current_pos))

        while self.hop_count > 0:

            if self.no_robots():
                self.die_reason = "no robots allowed at {}".format(self.current_pos)
                break

            self.gather_links()
            self.filter()   # filter invalid urls

            if len(self.current_urls) < 1:  # TODO go to last pos
                """
                if self.retries > 0:
                    next_url = self.last_pos
                    self.last_pos = self.current_pos
                    self.current_pos = next_url

                    self.retries -= 1
                    continue
                """

                self.die_reason = "no urls found at {}".format(self.current_pos)
                break

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
                [(lambda url: Queue.get_main_instance().add(url))(url) for url in self.current_urls]

            result = self.request(self.current_pos)

            if not result["success"]:
                self.die_reason = "{} at {}".format(result["error"], self.current_pos)
                break
            self.hop_count -= 1

        if self.hop_count <= 0:
            self.die_reason = "done"

        CrawlerAPI.get_instance().check_out(self.id)
        print("Crawler {} died at hop {}  reason: {}".format(self.id, self.hop_count, self.die_reason))

    def filter(self):
        for i in range((len(self.current_urls)) * -1, 0):   # backwards because pop while iterating
            if Robot.invalid_url(self.current_urls[i]):
                self.current_urls.pop(i)

    def reproduce(self):
        if self.reproduced or self.reproduction_rate == 0:
            return

        if self.per_page > len(self.current_urls):
            counter = len(self.current_urls)
        else:
            counter = self.per_page

        i = 0
        while i < counter:  # -1 so this crawler has an url
            new_crawler = Crawler(reproduction_rate=self.reproduction_rate - 1,
                                  start_url=self.current_urls[i])
            new_crawler.start()
            i += 1
        self.reproduced = True

    def no_robots(self):    # TODO implement no_robots()
        return False

    def gather_links(self):
        self.current_urls = list()

        for tag in self.current_content:
            if tag.tag == "a":
                try:
                    self.current_urls.append(tag.attrs[0][1])   # [("href", url)]
                except IndexError:
                    continue
