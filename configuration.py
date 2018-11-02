import configparser
from worker.test_worker import TestWorker

__setups = {
            "test": TestWorker
            }

CONFIG = configparser.ConfigParser()
WORKER_TYPE = None


def initialize(config_file):
    global WORKER_TYPE

    CONFIG.read(config_file)
    WORKER_TYPE = __setups[CONFIG.get("WORKER", "type")]
