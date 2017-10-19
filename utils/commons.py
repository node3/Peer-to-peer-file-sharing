import json
import os
import threading


# Load config file from the given path as a json
def load_config(config_path='../config.json'):
    try:
        with open(config_path) as config_file:
            config = json.load(config_file)
    except ValueError as err:
        raise Exception("Could not load config from %s. Error %s" % (config_path, err))

    return config


class Logging:
    debug_mode = True

    def __init__(self):
        return

    @staticmethod
    def debug(message):
        if Logging.debug_mode:
            Logging.info(message)

    @staticmethod
    def info(message):
        print "\n"
        print message

    @staticmethod
    def error(message):
        print "\n"
        print message
        exit(1)

    @staticmethod
    def exit(message):
        print "\n"
        print message
        exit(0)


class FuncThread(threading.Thread):
    thread_number = 1

    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
        FuncThread.thread_number += 1

    def run(self):
        self._target(*self._args)


def get_rfc_dir():
    rfc_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rfc")
    if not os.path.exists(rfc_dir):
        os.makedirs(rfc_dir)
    return rfc_dir


def get_rfc_path(rfc):
    if rfc:
        return os.path.join(get_rfc_dir(), ".".join([rfc["number"], rfc["format"]]))
    else:
        return None

