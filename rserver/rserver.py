from request_handlers import *
import argparse
import utils


def main():
    config = utils.load_config(args.config)
    head = None
    # sock = utils.listen4clients((utils.get_ip_address(), config["rs"]["port"]))
    sock = utils.listen4clients((config["rs"]["hostname"], config["rs"]["port"]))
    last_time_updated = int(time.time())

    # Serve incoming connections
    while True:
        try:
            utils.Logging.info(records.display_swarm_table(head))
            connection, request = utils.accept_request(sock)
            periodic_ttl_reduction(head, last_time_updated)
            head, response = process_request(head, request)
            last_time_updated = int(time.time())
            utils.send_response(connection, response)
        except KeyboardInterrupt:
            utils.Logging.exit("Registration server shutting down")
            break
    sock.close()


# multiplex the request to appropriate command with respective parameters
def process_request(head, request):
    utils.Logging.debug("Entering rserver.process_request")
    if request.command == "Register":
        if "cookie" in request.data and request.data["cookie"]:
            handle_keep_alive(head, request.data["cookie"])
            data = {"message": "TTL updated to 7200 seconds."}
            status = "201"
        elif "port" in request.data and request.data["port"]:
            head, cookie = handle_registration(head, request.hostname, request.data["port"])
            data = {"cookie": cookie}
            status = "200"
        else:
            data = {"message": "Received Register request without port or cookie"}
            status = "300"

    elif request.command == "Leave":
        if "cookie" in request.data and request.data["cookie"]:
            head, peer_ejected = handle_leaving(head, request.data["cookie"])
            if peer_ejected:
                data = {"message": "Peer unregistered from the server"}
                status = "201"
            else:
                data = {"message": "Peer not found"}
                status = "100"
        else:
            data = {"message": "Received Leave request without cookie"}
            status = "300"

    elif request.command == "PQuery":
        if "cookie" in request.data and request.data["cookie"]:
            handle_keep_alive(head, request.data["cookie"])
            data = handle_peer_query(head, request.data["cookie"])
            status = "200"
        else:
            data = {"message": "Received PQuery request without cookie"}
            status = "300"

    elif request.command == "KeepAlive":
        if "cookie" in request.data and request.data["cookie"]:
            handle_keep_alive(head, request.data["cookie"])
            data = {"message": "TTL updated to 7200 seconds."}
            status = "201"
        else:
            data = {"message": "Received KeepAlive request without cookie"}
            status = "300"
    else:
        data = {"message": "Request message has an invalid command"}
        status = "300"

    utils.Logging.debug("Exiting rserver.process_request")
    response = records.P2PResponse(status, data)
    # try:
    #     utils.Logging.debug("Exiting rserver.process_request")
    #     response = records.P2PResponse(status, data)
    # except UnboundLocalError:
    #     print "Perhaps *********%s************" % request.command
    #     request.display()

    return head, response


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help="Path to the config file", type=str, required=True)
parser.add_argument("-d", "--debug", help="Enter debug mode", action="store_true", default=False)
args = parser.parse_args()

utils.Logging.debug_mode = args.debug
if __name__ == "__main__":
    main()

