from rs_communication import *
from peer_communication import *
from utils import *
import records
from os import system
import argparse


def main():
    config = commons.load_config(args.config)
    peer_info = records.PeerInfo()
    while True:
        try:
            choice = user_interaction(peer_info)
            flow_handler(peer_info, config, choice)
        except KeyboardInterrupt:
            print "Client shutting down"


def user_interaction(peer_info):
    system('clear')
    print "\n\t\t\t\t*** Welcome to P2P client ***\n" \
          "\n\t\tMy registration server id : %s" \
          "\n\t\tMy registration peers: %s" % (str(peer_info.cookie), str(peer_info.peers))

    print "\n\n\t\tSelect an action by pressing its serial number" \
          "\n\t\t(1) Register with server" \
          "\n\t\t(2) Leave the registration server" \
          "\n\t\t(3) Query for peers" \
          "\n\t\t(4) Send keep-alive signal to registration server" \
          "\n\t\t(5) Query RFCs from peers" \
          "\n\t\t(6) Get RFC from a peer"   \
          "\n\t\t(7) Exit"
    choice = raw_input()
    return choice


def flow_handler(peer_info, config, choice):
    server_hostname = config["rs"]["hostname"]
    server_port = config["rs"]["port"]

    # Register with server
    if choice == "1":
        if peer_info.cookie:
            continue_or_exit("Peer is already registered with the server with id %s" % peer_info.cookie)
        else:
            peer_info.cookie = register(server_hostname, server_port, config["peer"][CLIENT_UID]["port"])
            continue_or_exit("Registered with the server with id %s" % peer_info.cookie)

    # Leave the registration server
    elif choice == "2":
        if peer_info.cookie:
            leave(server_hostname, server_port, peer_info.cookie)
            peer_info.cookie = None
            continue_or_exit("Peer is unregistered from the server")
        else:
            continue_or_exit("Peer is not registered with the server")

    # Query for peers
    elif choice == "3":
        if peer_info.cookie:
            peer_info.peers = p_query(server_hostname, server_port, peer_info.cookie)
            continue_or_exit("Peer list retrieved from the registration server\n%s" % str(peer_info.peers))
        else:
            continue_or_exit("Peer is not registered with the server")

    # Send keep-alive signal to registration server
    elif choice == "4":
        if peer_info.cookie:
            keep_alive(server_hostname, server_port, peer_info.cookie)
            continue_or_exit("Keep alive signal sent successfully to the server")
        else:
            continue_or_exit("Peer is not registered with the server")

    # Query RFCs from peers
    elif choice == "5":
        if peer_info.peers:
            peer_info.rfc_index_head = rfc_query(peer_info.peers)
            continue_or_exit("Received list of RFCs from peers. Updated the local index.")
        else:
            continue_or_exit("Peer list found empty. Query for peers from registration server first")

    # Get RFC from a peer
    elif choice == "6":
        if peer_info.peers:
            peer_info.show_rfc_index()
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
                        if rfc.hostname == peer.hostname:
                            found_peer_port = True
                            rfc_downloaded = get_rfc(peer.hostname, peer.port, rfc_number)
                            break
            if not found_rfc:
                continue_or_exit("Could not find RFC #%s in the database above" % rfc_number)
            elif not found_peer_port:
                continue_or_exit("Could not find the port for RFC #%s in the peers list received from RS"
                                 % rfc_number)
            elif rfc_downloaded:
                continue_or_exit("RFC downloaded. Check for file %s" % rfc_downloaded)
            else:
                continue_or_exit("RFC could not be downloaded. peer.get_rfc() must have failed.")
            # Update self records on downloading an RFC

    elif choice == "7":
        exit(0)
    else:
        continue_or_exit("Incorrect choice")


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help="Path to the config file", type=str, required=True)
parser.add_argument("-i", "--id", help="Unique id for the peer as used in config", type=str, required=True)
args = parser.parse_args()

CLIENT_UID = args.id
if __name__ == "__main__":
    main()
