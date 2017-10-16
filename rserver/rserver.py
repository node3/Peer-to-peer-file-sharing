from connection import *
from request_handler import *
import argparse
import commons


def main():
    config = commons.load_config(args.config)
    head = None
    sock = listening_socket((config["rs"]["hostname"], config["rs"]["port"]))

    # Serve incoming connections
    while True:
        try:
            commons.Logging.info("\n\t--------")
            connection, request = accept_connection(sock)
            head, response = process_request(head, request)
            respond_to_connection(connection, response)
        except KeyboardInterrupt:
            commons.Logging.exit("Server shutting down")
            break
    sock.close()


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help="Path to the config file", type=str, required=True)
parser.add_argument("-d", "--debug", help="Enter debug mode", type=bool, default=False)
args = parser.parse_args()

commons.Logging.debug_mode = args.debug
if __name__ == "__main__":
    main()

