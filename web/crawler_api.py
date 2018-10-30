

class CrawlerAPI:
    instance = None

    def __init__(self):
        self.crawler_map = dict()

    @staticmethod
    def get_instance():
        if CrawlerAPI.instance is None:
            CrawlerAPI.instance = CrawlerAPI()

        return CrawlerAPI.instance

    def all_done(self):
        return len(self.crawler_map) == 0

    def register(self, crawler):
        self.crawler_map.update({crawler.id: crawler})

    def check_out(self, id):
        self.crawler_map.pop(id)
