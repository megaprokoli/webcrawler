from constants import CONFIG


class Queue:
    instance = None

    def __init__(self):
        self.gattered_links = []    # FIFO
        self.dump_seperater = ",\n"
        self.dump_file = CONFIG.get("QUEUE", "dumpFile")
        self.overwrite = bool(CONFIG.get("QUEUE", "overwrite"))
        self.direct_dump = bool(CONFIG.get("QUEUE", "directDump"))

    @staticmethod
    def get_instance():
        if Queue.instance is None:
            Queue.instance = Queue()

        return Queue.instance

    def has_next(self):
        if len(self.gattered_links) == 0:
            return False
        return True

    def next(self):
        return self.gattered_links.pop(0)

    def is_duplicate(self, url):
        return url in self.gattered_links

    def add(self, url):
        if self.is_duplicate(url):
            return
        self.gattered_links.append(url)

    def dump(self):     # TODO dump all when crawlers are done
        with open(self.dump_file, "w" if self.overwrite else "a") as file:
            if not file.writable():
                print("dump file not writable")  # TODO raise some exception
                return

            while self.has_next():
                file.write(self.next() + self.dump_seperater)
            # for url in self.gattered_links:
                # file.write(url + self.dump_seperater)
