import configparser

CONFIG = configparser.ConfigParser()
# CONFIG.read("res/config.ini")


def initialize(config_file):
    CONFIG.read(config_file)
