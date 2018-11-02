from abc import abstractmethod, ABC
from web.response_data import ResponseData
from web.html_parser import HtmlParser
from threading import Thread
import requests


class Robot(ABC, Thread):

    def __init__(self):
        super().__init__()

        self.parser = HtmlParser()
        self.current_content = list()

    @abstractmethod
    def run(self):
        pass

    def request(self, url):
        try:
            resp = requests.get(url)
        except ConnectionRefusedError as err:
            return {"success": False, "error": err}
        except:
            return {"success": False, "error": "unknown"}

        if resp.status_code != 200:
            return {"success": False, "error": "status code not 200"}

        self.parser.feed(str(resp.content))
        self.current_content = self.parser.lsStartTags

        return {"success": True, "error": None}


