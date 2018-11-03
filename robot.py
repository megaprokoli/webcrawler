from abc import abstractmethod, ABC
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

    @staticmethod
    def invalid_url(url):
        if url is None:
            return True

        split_url = url.split(":")
        return not (split_url[0] == "https" or split_url[0] == "http")

    def request(self, url):
        resp = None

        try:
            resp = requests.get(url)
        except ConnectionRefusedError as err:
            return {"success": False, "error": err, "response": resp}
        except requests.exceptions.MissingSchema as err:
            return {"success": False, "error": err, "response": resp}
        except:
            return {"success": False, "error": "unknown", "response": resp}

        if resp.status_code != 200:
            return {"success": False, "error": "status code not 200", "response": resp}

        self.parser.feed(str(resp.content))
        self.current_content = self.parser.lsStartTags

        return {"success": True, "error": None, "response": resp}


