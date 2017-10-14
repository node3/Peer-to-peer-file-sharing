from connection import *
from request_handler import *
import commons


def main():
    client_id = "1"
    config = commons.load_config('../config.json')

    sock = connect2server(config["rs"]["address"], config["rs"]["port"])
    cookie = register(sock, config["peer"][client_id]["port"])
    sock.close()

    sock = connect2server(config["rs"]["address"], config["rs"]["port"])
    leave(sock, cookie)
    sock.close()


if __name__ == "__main__":
    main()
