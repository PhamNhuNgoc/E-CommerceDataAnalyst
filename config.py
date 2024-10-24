import configparser

config = configparser.ConfigParser()
config.read('config.ini')

DRIVER_PATH = config['settings']['DRIVER_PATH']

if DRIVER_PATH is None:
    raise ValueError("DRIVER_PATH is not set in config.ini")
