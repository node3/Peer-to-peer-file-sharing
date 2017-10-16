from commands import *
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
            response = process_request(request)
            utils.send_response(connection, response)
        except KeyboardInterrupt:
            utils.Logging.exit("Peer server shutting down")
            break
    sock.close()


# multiplex the request to appropriate command with respective parameters
def process_request(request):
    utils.Logging.debug("Entering peer.process_request")
    if request.command == "RFCQuery":
        data = handle_rfcs_query()
        if data:
            status = "200"
        else:
            data = {"message": "No RFCs found on %s" % utils.get_ip_address()}
            status = "100"

    elif request.command == "GetRFC":
        if "rfc_number" in request.data:
            rfc = handle_get_rfc(request.data["rfc_number"])
            data = {}
            if rfc:
                status = "200"
            else:
                status = "100"
        else:
            data = {"message": "Received GetRFC request without rfc_number field"}
            status = "300"
    else:
        data = {"message": "Request message has an invalid command"}
        status = "300"

    utils.Logging.debug("Exiting peer.process_request")
    response = records.P2PResponse(status, data)
    return response


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help="Path to the config file", type=str, required=True)
parser.add_argument("-d", "--debug", help="Enter debug mode", action="store_true", default=False)
parser.add_argument("-i", "--id", help="Unique id for the peer as used in config", type=str, required=True)
args = parser.parse_args()

CLIENT_UID = args.id
utils.Logging.debug_mode = args.debug
if __name__ == "__main__":
    main()

