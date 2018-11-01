

class CrawlerAPI:
    instance = None

    def __init__(self):
        self.crawler_map = dict()

    @staticmethod
    def get_instance():
        if CrawlerAPI.instance is None:
            CrawlerAPI.instance = CrawlerAPI()

        return CrawlerAPI.instance

    def kill_all(self):
        for crawler_id in self.crawler_map:
            self.kill(crawler_id)

    def kill(self, id):
        crawler = self.crawler_map[id]
        crawler.die_reason = "killed by user"
        crawler.hop_count = 0

    def all_done(self):
        return len(self.crawler_map) == 0

    def register(self, crawler):
        self.crawler_map.update({crawler.id: crawler})

    def check_out(self, id):
        self.crawler_map.pop(id)
