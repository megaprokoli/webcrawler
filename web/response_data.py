class ResponseData:

    def __init__(self, encoding, headers, content):
        self.encoding = encoding
        self.headers = headers
        self.content = content

    def __str__(self):
        return self.encoding
