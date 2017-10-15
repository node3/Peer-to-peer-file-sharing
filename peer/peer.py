from request_handler import *
import commons
from utils import *

COOKIE = None
HEAD = None
PEERS = []


def main():
    while True:
        try:
            choice = interactive_guide()
            choice_handler(choice)
        except KeyboardInterrupt:
            print "Client shutting down"


def interactive_guide():
    print "\n\t\t\t\t*** Welcome to P2P client ***\n" \
          "\n\t\tSelect an action by pressing its serial number" \
          "\n\t\t(1) Register with server" \
          "\n\t\t(2) Leave the registration server" \
          "\n\t\t(3) Query for peers" \
          "\n\t\t(4) Send keep-alive signal to registration server" \
          "\n\t\t(5) Request RFC from peers"
    choice = raw_input()
    return choice


def choice_handler(choice):
    if choice in ["1", "2", "3", "4", "5"]:
        global COOKIE
        global PEERS
        client_id = "1"
        config = commons.load_config('../config.json')

        # Register with server
        if choice == "1":
            if COOKIE:
                continue_or_exit("Peer is already registered with the server with id %s" % COOKIE)
            else:
                COOKIE = register(config["rs"]["address"], config["rs"]["port"], config["peer"][client_id]["port"])
                continue_or_exit("Registered with the server with id %s" % COOKIE)

        # Leave the registration server
        elif choice == "2":
            if COOKIE:
                leave(config["rs"]["address"], config["rs"]["port"], COOKIE)
                continue_or_exit("Peer is unregistered from the server")
            else:
                continue_or_exit("Peer is not registered with the server")

        # Query for peers
        elif choice == "3":
            if COOKIE:
                PEERS = p_query(config["rs"]["address"], config["rs"]["port"], COOKIE)
                continue_or_exit("Peer list retrieved from the registration server \n[ %s ]" % ",".join(PEERS))
            else:
                continue_or_exit("Peer is not registered with the server")

        # Send keep-alive signal to registration server
        elif choice == "4":
            if COOKIE:
                keep_alive(config["rs"]["address"], config["rs"]["port"], COOKIE)
                continue_or_exit("Keep alive signal sent successfully to the server")
            else:
                continue_or_exit("Peer is not registered with the server")

        # Request RFC from peers
        elif choice == "5":
            if PEERS:
                continue_or_exit("Not implemented yet")
            else:
                continue_or_exit("Peer list found empty. Query for peers from registration server first")

    else:
        continue_or_exit("Incorrect choice")


if __name__ == "__main__":
    main()
