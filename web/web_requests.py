import requests
from web.response_data import ResponseData


class WebRequester:     # TODO requests direct in classes

    def __init__(self):
        pass

    def exec_url(self, url):
        resp = requests.get(url)

        if resp.status_code != 200:
            return None

        return ResponseData(resp.encoding, resp.headers, resp.content)
