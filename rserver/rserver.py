from connection import *
from request_handler import *


def main():
    config = commons.load_config('../config.json')
    head = None
    sock = listening_socket((config["rs"]["address"], config["rs"]["port"]))

    # Serve incoming connections
    while True:
        try:

            connection, request = accept_connection(sock)
            head, response = process_request(head, request)
            respond_to_connection(connection, response)
        except KeyboardInterrupt:
            print "Server shutting down"
            break
    sock.close()


if __name__ == "__main__":
    main()

