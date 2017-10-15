import socket
import json


DEBUG = True
# Debug = False


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


# Load config file from the given path as a json
def load_config(config_path='../config.json'):
    try:
        with open(config_path) as config_file:
            config = json.load(config_file)
    except ValueError as err:
        raise Exception("Could not load config from %s. Error %s" %(config_path, err))

    return config


def debug(message):
    global DEBUG
    if DEBUG:
        print message
