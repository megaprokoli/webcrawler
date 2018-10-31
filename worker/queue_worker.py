from abc import abstractmethod, ABC
from threading import Thread
from web.html_parser import HtmlParser
from web.web_requests import WebRequester


class QueueWorker(ABC, Thread):

    def __init__(self, workload):
        super().__init__()
        self.workload = workload

        self.parser = HtmlParser()
        self.requester = WebRequester()
        self.current_page = list()

    @abstractmethod
    def run(self):
        pass

    def request(self, url):     # TODO is same as in crawler
        try:
            response = self.requester.exec_url(url)
        except ConnectionRefusedError as err:
            return {"success": False, "error": err}
        except:
            return {"success": False, "error": "unknown"}

        if response is None:
            return {"success": False, "error": "status code not 200"}

        self.parser.feed(str(response.content))
        self.current_page = self.parser.lsStartTags

        return {"success": True, "error": None}
