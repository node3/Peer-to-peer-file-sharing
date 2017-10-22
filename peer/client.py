from request_handlers import *
from commands import *
import records
from server import server
import argparse
import utils
from os import system


def main():
    config = utils.load_config(args.config)
    peer_info = records.PeerInfo()
    peer_info.rfc_index_head = build_rfc_index()
    t1 = utils.FuncThread(server, config, peer_info, PEER_ID, args.debug)
    t1.setDaemon(True)
    t1.start()

    t2 = utils.FuncThread(periodic_keep_alive, peer_info, config["rs"]["hostname"], config["rs"]["port"])
    t2.setDaemon(True)
    t2.start()

    last_time_updated = int(time.time())
    while True:
        try:
            choice = user_interaction()
            periodic_ttl_reduction(peer_info.rfc_index_head, last_time_updated)
            last_time_updated = int(time.time())
            flow_handler(peer_info, config, choice)
        except KeyboardInterrupt:
            utils.Logging.exit("Client shutting down")
        except BaseException as err:
            utils.Logging.info(err)


def user_interaction():
    guide = "\n\t\t\t\t*** Welcome to P2P client ***\n" \
            "\n\t\t(1) Register with server" \
            "\n\t\t(2) Leave the registration server" \
            "\n\t\t(3) Query for peers" \
            "\n\t\t(4) Send keep-alive signal to registration server" \
            "\n\t\t(5) Get an RFC" \
            "\n\t\t(6) View current state of the peer" \
            "\n\t\t(0) Exit" \
            "\n\n\t\tSelect an action by pressing its serial number : "
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
            print_and_continue("Peer registered with the server with id %s" % peer_info.cookie)
        else:
            print_and_continue(data)

    # Leave the registration server
    elif choice == "2":
            status, data = leave_request(server_hostname, server_port, params)
            if status == "201":
                peer_info.cookie = None
            print_and_continue(data)

    # Query for peers
    elif choice == "3":
        status, data = peer_query_request(server_hostname, server_port, params)
        if status == "200":
            peer_info.add_new_peers(data)
            print_and_continue("Peer list retrieved from the registration server :\n%s" % str(data))
        else:
            print_and_continue(data)

    # Send keep-alive signal to registration server
    elif choice == "4":
        status, data = keep_alive_request(server_hostname, server_port, params)
        print_and_continue(data)

    # Get RFC
    elif choice == "5":
        if peer_info.peers:
            rfc_number = raw_input("Enter the rfc # to be downloaded : ")
            if rfc_number == "":
                print_and_continue("Invalid input! Please ensure that a you insert a valid number.")
            else:
                local_rfc = check_rfc_metadata(rfc_number)
                if local_rfc:
                    print_and_continue("RFC locally available at %s" % local_rfc)
                else:
                    downloaded_rfc = get_rfc_from_peers(peer_info, rfc_number)
                    if downloaded_rfc:
                        print_and_continue("RFC now available at %s" % downloaded_rfc)
                    else:
                        print_and_continue("OOPS! RFC %s not found on any peer" % rfc_number)
        else:
            print_and_continue("Peer list found empty. Query for peers from registration server first")

    # Display current state of the peer
    elif choice == "6":
        print_and_continue(peer_info.display_peer_state())

    elif choice == "0":
        utils.Logging.exit("Bye!")

    else:
        print_and_continue("Incorrect choice")


def print_and_continue(message):
    utils.Logging.info(message)
    raw_input("\n\n\t\tPress any key to go back to the interactive menu .... ")
    system('clear')


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help="Path to the config file", type=str, required=True)
parser.add_argument("-i", "--id", help="Unique id for the peer as used in config", type=str, required=True)
parser.add_argument("-d", "--debug", help="Enter debug mode", action="store_true", default=False)
args = parser.parse_args()

PEER_ID = args.id
utils.Logging.debug_mode = args.debug
if __name__ == "__main__":
    main()
