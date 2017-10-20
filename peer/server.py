from socket import error as socket_error
from time import sleep

import utils
from request_handlers import *
# Server maintains a server thread running
from utils import get_rfc_path


def server(config, peer_info, peer_id, debug):
    utils.Logging.debug_mode = debug
    utils.Logging.info("Starting a peer server in background.")
    run_server(config, peer_info, peer_id)
    utils.Logging.info("Peer server has stopped.")


# This is the thread that serves
def run_server(config, peer_info, peer_id):
    # Open a socket
    sock = None
    while not sock:
        try:
            sock = utils.listen4clients((utils.get_ip_address(), config["peer"][peer_id]["port"]))
        except socket_error as err:
            utils.Logging.debug("Tried to open a socket. %s. Retrying in 3 seconds." % err)
            sleep(3)

    utils.Logging.info("Peer server is now running")

    # Serve incoming connections until failure
    while True:
        try:
            utils.Logging.info("\n\t***** We are listening for requests *****")
            connection, request = utils.accept_request(sock)
            utils.Logging.info("\n\t***** Spawning a new thread the serve the new request *****")
            t = utils.FuncThread(process_request, connection, peer_info, request)
            t.setDaemon(True)
            t.start()
        except KeyboardInterrupt:
            break
        except BaseException as err:
            utils.Logging.info(err)

    sock.close()


# multiplex the request to appropriate command with respective parameters
def process_request(connection, peer_info, request):
    utils.Logging.debug("Entering peer.process_request")
    if request.command == "RFCQuery":
        data = handle_rfcs_query(peer_info.rfc_index_head)
        status = "200"
        utils.send_response(connection, records.P2PResponse(status, data))
    elif request.command == "GetRFC":
        if "rfc" in request.data:
            metadata = read_rfc_metadata()
            if metadata:
                rfc = None
                for rfc_meta in metadata["rfcs"]:
                    if rfc_meta["number"] == request.data["rfc"]:
                        rfc = rfc_meta
                        break
                rfc_file = get_rfc_path(rfc)
                if rfc and os.path.exists(rfc_file):
                    utils.send_rfc(connection, rfc_file, rfc["format"])
                else:
                    status = "100"
                    data = {"message": "Requested RFC %s not found" % request.data["rfc"]}
                    utils.send_response(connection, records.P2PResponse(status, data))
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

