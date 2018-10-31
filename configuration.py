import configparser
from worker.map_worker import MapWorker

__setups = {
            "default": None,
            "map": MapWorker
            }

CONFIG = configparser.ConfigParser()
WORKER_TYPE = None


def initialize(config_file):
    global WORKER_TYPE

    CONFIG.read(config_file)
    WORKER_TYPE = __setups[CONFIG.get("WORKER", "type")]
