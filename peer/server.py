from request_handlers import *
import argparse
import utils


def main():
    config = utils.load_config(args.config)
    sock = utils.listen4clients((utils.get_ip_address(), config["peer"][CLIENT_UID]["port"]))

    # Serve incoming connections
    while True:
        try:
            utils.Logging.info("\n\t--------")
            connection, request = utils.accept_request(sock)
            process_request(connection, request)
        except KeyboardInterrupt:
            utils.Logging.exit("Peer server shutting down")
            break
    sock.close()


# multiplex the request to appropriate command with respective parameters
def process_request(connection, request):
    utils.Logging.debug("Entering peer.process_request")
    if request.command == "RFCQuery":
        data = handle_rfcs_query()
        if data:
            status = "200"
        else:
            data = {"message": "No RFCs found on %s" % utils.get_ip_address()}
            status = "100"
        utils.send_response(connection, records.P2PResponse(status, data))
    elif request.command == "GetRFC":
        if "rfc" in request.data:
            rfc_file = os.path.join(get_rfc_dir(), request.data["rfc"] + ".txt")
            if os.path.exists(rfc_file):
                utils.send_rfc(connection, rfc_file)
            else:
                status = "100"
                data = {"message": "Requested RFC %s not found" % request.data["rfc"]}
                utils.send_response(connection, records.P2PResponse(status, data))
        else:
            data = {"message": "Received GetRFC request without rfc field"}
            status = "300"
            utils.send_response(connection, records.P2PResponse(status, data))
    else:
        data = {"message": "Request message has an invalid command"}
        status = "300"
        utils.send_response(connection, records.P2PResponse(status, data))


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help="Path to the config file", type=str, required=True)
parser.add_argument("-d", "--debug", help="Enter debug mode", action="store_true", default=False)
parser.add_argument("-i", "--id", help="Unique id for the peer as used in config", type=str, required=True)
args = parser.parse_args()

CLIENT_UID = args.id
utils.Logging.debug_mode = args.debug
if __name__ == "__main__":
    main()

