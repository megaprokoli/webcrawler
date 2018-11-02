from configuration import CONFIG


class Queue:
    instance = None

    def __init__(self, list=None):
        self.gathered_links = list if Queue.instance is not None else []   # FIFO
        self.dump_seperater = ",\n"
        self.dump_file = CONFIG.get("QUEUE", "dumpFile")
        self.overwrite = bool(CONFIG.get("QUEUE", "overwrite"))
        self.direct_dump = bool(CONFIG.get("QUEUE", "directDump"))

    @classmethod
    def get_main_instance(cls):
        if cls.instance is None:
            cls.instance = Queue()

        return cls.instance

    @classmethod
    def get_subqueue(cls, list):
        return Queue(list)

    def has_next(self):
        if len(self.gathered_links) == 0:
            return False
        return True

    def next(self):
        return self.gathered_links.pop(0)

    def is_duplicate(self, url):
        return url in self.gathered_links

    def add(self, url):
        if self.is_duplicate(url):
            return
        elif isinstance(url, list):
            self.gathered_links += url
        else:
            self.gathered_links.append(url)

    def read(self):
        with open(self.dump_file) as file:
            self.gathered_links += file.read().split(self.dump_seperater)

    def dump(self):
        with open(self.dump_file, "w" if self.overwrite else "a") as file:
            if not file.writable():
                raise Exception("dump file not writable")

            while self.has_next():
                file.write(self.next() + self.dump_seperater)
