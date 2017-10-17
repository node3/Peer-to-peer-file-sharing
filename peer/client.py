from request_handlers import *
from commands import *
import records
from os import system
from server import server
import argparse
import utils


def main():
    config = utils.load_config(args.config)
    peer_info = records.PeerInfo()
    peer_info.rfc_index_head = build_rfc_index()
    utils.FuncThread(server, config, args.debug, PEER_ID)
    while True:
        try:
            choice = user_interaction()
            flow_handler(peer_info, config, choice)
        except KeyboardInterrupt:
            utils.Logging.exit("Client shutting down")


def user_interaction():
    system('clear')
    guide = "\n\t\t\t\t*** Welcome to P2P client ***\n" \
            "\n\n\t\tSelect an action by pressing its serial number" \
            "\n\t\t(1) Register with server" \
            "\n\t\t(2) Leave the registration server" \
            "\n\t\t(3) Query for peers" \
            "\n\t\t(4) Send keep-alive signal to registration server" \
            "\n\t\t(5) Query RFCs from peers" \
            "\n\t\t(6) Get RFC from a peer" \
            "\n\t\t(7) View current state of the peer" \
            "\n\t\t(0) Exit"
    utils.Logging.info(guide)
    choice = raw_input()
    return choice


def flow_handler(peer_info, config, choice):
    server_hostname = config["rs"]["hostname"]
    server_port = config["rs"]["port"]
    params = create_data_field(peer_info.cookie, config["peer"][PEER_ID]["port"])

    # Register with server
    if choice == "1":
        status, data = register_request(server_hostname, server_port, params)
        if status == "200":
            peer_info.cookie = data
            continue_or_exit("Peer registered with the server with id %s" % peer_info.cookie)
        else:
            continue_or_exit(data)

    # Leave the registration server
    elif choice == "2":
            status, data = leave_request(server_hostname, server_port, params)
            if status == "201":
                peer_info.cookie = None
            continue_or_exit(data)

    # Query for peers
    elif choice == "3":
        status, data = peer_query_request(server_hostname, server_port, params)
        if status == "200":
            peer_info.peers = data
            continue_or_exit("Peer list retrieved from the registration server\n%s" % str(data))
        else:
            continue_or_exit(data)

    # Send keep-alive signal to registration server
    elif choice == "4":
        status, data = keep_alive_request(server_hostname, server_port, params)
        continue_or_exit(data)


    # Query RFCs from peers
    elif choice == "5":
        peer_info.peers = [{"hostname": "192.168.0.15", "port": 1281}]
        if peer_info.peers:
            peer_info.rfc_index_head = rfcs_query_request(peer_info.peers)
            continue_or_exit("Updated the local index")
        else:
            continue_or_exit("Peer list found empty. Query for peers from registration server first")

    # Get RFC from a peer
    elif choice == "6":
        if peer_info.peers:
            rfc_number = raw_input("Enter the rfc # to be downloaded")
            ptr = peer_info.rfc_index_head
            found_rfc = False
            found_peer_port = False
            rfc_downloaded = False
            while ptr:
                if ptr.rfc.number == rfc_number:
                    found_rfc = True
                    rfc = ptr.rfc
                    for peer in peer_info.peers:
                        if rfc.hostname == peer["hostname"]:
                            found_peer_port = True
                            rfc_downloaded = rfc_request(peer["hostname"], peer["port"], rfc_number, ptr.rfc.title)
                            break
                ptr = ptr.nxt
            if not found_rfc:
                continue_or_exit("Could not find RFC #%s in peer database. Check current state of peer." % rfc_number)
            elif not found_peer_port:
                continue_or_exit("Could not find the port for RFC #%s in the peers list received from RS"
                                 % rfc_number)
            elif rfc_downloaded:
                continue_or_exit("RFC downloaded. Check for file %s" % rfc_downloaded)
            else:
                continue_or_exit("RFC could not be downloaded. peer.rfc_request() must have failed.")
            # Update self records on downloading an RFC
    elif choice == "7":
        continue_or_exit(peer_info.current_state())
    elif choice == "0":
        utils.Logging.exit("Bye!")
    else:
        continue_or_exit("Incorrect choice")


def continue_or_exit(message):
    utils.Logging.info(message)
    try:
        utils.Logging.info("\nPress any key to go back to the menu. Press Control+C to exit.")
        raw_input()
        system('clear')
    except KeyboardInterrupt:
        utils.Logging.info("Client shutting down")
        exit(0)


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help="Path to the config file", type=str, required=True)
parser.add_argument("-i", "--id", help="Unique id for the peer as used in config", type=str, required=True)
parser.add_argument("-d", "--debug", help="Enter debug mode", action="store_true", default=False)
args = parser.parse_args()

PEER_ID = args.id
utils.Logging.debug_mode = args.debug
if __name__ == "__main__":
    main()
