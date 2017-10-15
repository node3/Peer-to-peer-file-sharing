from connection import *
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
    if choice in [1, 2, 3, 4, 5]:
        global COOKIE
        global PEERS
        client_id = "1"
        config = commons.load_config('../config.json')
        sock = connect2server(config["rs"]["address"], config["rs"]["port"])

        # Register with server
        if choice == 1:
            if COOKIE:
                print "User is already registered with the server with id %s" % COOKIE
            else:
                COOKIE = register(config["rs"]["address"], config["rs"]["port"], config["peer"][client_id]["port"])

        # Leave the registration server
        elif choice == 2:
            if COOKIE:
                leave(sock, COOKIE)
            else:
                print "User is not registered with the server"

        # Query for peers
        elif choice == 3:
            if COOKIE:
                PEERS = p_query(sock, COOKIE)
            else:
                print "User is not registered with the server"

        # Send keep-alive signal to registration server
        elif choice == 4:
            if COOKIE:
                keep_alive(sock, COOKIE)
            else:
                print "User is not registered with the server"

        # Request RFC from peers
        elif choice == 5:
            if PEERS:
                p_query(sock, PEERS)
            else:
                print "Peer list found empty. Query for peers from registration server first."

    else:
        print ""
        continue_or_exit()


if __name__ == "__main__":
    main()
