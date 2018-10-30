from html.parser import HTMLParser
from web.html_tag import HtmlTag


class HtmlParser(HTMLParser):

    def __init__(self):
        super().__init__()

        self.lsStartTags = list()
        self.lsEndTags = list()
        self.lsStartEndTags = list()
        self.lsComments = list()

    def handle_starttag(self, startTag, attrs):
        self.lsStartTags.append(HtmlTag(startTag, attrs))

    def handle_endtag(self, endTag):
        self.lsEndTags.append(endTag)

    def handle_startendtag(self, startendTag, attrs):
        self.lsStartEndTags.append(HtmlTag(startendTag, attrs))

    def handle_comment(self, data):
        self.lsComments.append(data)
