from request_handlers import *
import utils


def server(config, debug, peer_id):
    utils.FuncThread(run_server, config, debug, peer_id)


def run_server(config, debug, peer_id):
    utils.Logging.debug_mode = debug
    sock = utils.listen4clients((utils.get_ip_address(), config["peer"][peer_id]["port"]))

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

