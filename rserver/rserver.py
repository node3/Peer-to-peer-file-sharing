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
            commons.print_msg("\n\t--------")
            connection, request = accept_connection(sock)
            head, response = process_request(head, request)
            respond_to_connection(connection, response)
        except KeyboardInterrupt:
            print "Server shutting down"
            break
    sock.close()


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help="Path to the config file", type=str, required=True)
args = parser.parse_args()
if __name__ == "__main__":
    main()

