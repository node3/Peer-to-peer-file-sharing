from commands import *
import argparse
import utils


def main():
    config = utils.load_config(args.config)
    head = None
    sock = utils.listen4clients((config["rs"]["hostname"], config["rs"]["port"]))

    # Serve incoming connections
    while True:
        try:
            utils.Logging.info("\n\t--------")
            connection, request = utils.accept_request(sock)
            head, response = process_request(head, request)
            utils.send_response(connection, response)
        except KeyboardInterrupt:
            utils.Logging.exit("Server shutting down")
            break
    sock.close()


# multiplex the request to appropriate command with respective parameters
def process_request(head, request):
    utils.Logging.debug("Entering rserver.process_request")
    if request.command == "Register":
        if "port" in request.data:
            head, peer_registered = handle_registeration(head, request.hostname, request.data["port"])
            if peer_registered:
                data = {"cookie": head.peer.cookie}
                status = "200"
            else:
                data = {"message": "Peer already registered with same hostname and port"}
                status = "100"
        else:
            data = {"message": "Received Leave request without port field"}
            status = "300"

    elif request.command == "Leave":
        if "cookie" in request.data:
            head, peer_ejected = handle_leaving(head, request.data["cookie"])
            data = {}
            if peer_ejected:
                status = "201"
            else:
                status = "100"
        else:
            data = {"message": "Received Leave request without cookie field"}
            status = "300"

    elif request.command == "PQuery":
        if "cookie" in request.data:
            data = handle_peer_query(head, request.data["cookie"])
            status = "200"
        else:
            data = {"message": "Received PQuery request without cookie field"}
            status = "300"

    elif request.command == "KeepAlive":
        if "cookie" in request.data:
            ttl_updated = handle_keep_alive(head, request.data["cookie"])
            data = {}
            if ttl_updated:
                status = "201"
            else:
                status = "100"
        else:
            data = {"message": "Received KeepAlive request without cookie field"}
            status = "300"
    else:
        data = {"message": "Request message has an invalid command"}
        status = "300"

    utils.Logging.debug("Exiting rserver.process_request")
    response = records.P2PResponse(status, data)
    return head, response


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help="Path to the config file", type=str, required=True)
parser.add_argument("-d", "--debug", help="Enter debug mode", action="store_true", default=False)
args = parser.parse_args()

utils.Logging.debug_mode = args.debug
if __name__ == "__main__":
    main()

