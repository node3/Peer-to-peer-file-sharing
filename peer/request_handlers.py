import pickle
from commands import *
import records


# Register a client with the server
def register_request(server_ip, server_port, params):
    utils.Logging.debug("Entering peer.register_request")
    sock = utils.send_request(server_ip, server_port, "Register", params)
    response = utils.accept_response(sock)
    if response.status == "200":
        data = response.data["cookie"]
    else:
        data = response.data["message"]
    utils.Logging.debug("Exiting peer.register_request")
    return response.status, data


# De-registeration a client from the server
def leave_request(server_ip, server_port, params):
    utils.Logging.debug("Entering peer.leave_request")
    sock = utils.send_request(server_ip, server_port, "Leave", params)
    response = utils.accept_response(sock)
    utils.Logging.debug("Exiting peer.leave_request")
    return response.status, response.data["message"]


# Query for peers
def peer_query_request(server_ip, server_port, params):
    utils.Logging.debug("Entering peer.peer_query_request")
    sock = utils.send_request(server_ip, server_port, "PQuery", params)
    response = utils.accept_response(sock)
    if response.status == "200":
        data = response.data["peers"]
    else:
        data = response.data["message"]
    utils.Logging.debug("Exiting peer.peer_query_request")
    return response.status, data


# Send keep alive signal
def keep_alive_request(server_ip, server_port, params):
    utils.Logging.debug("Entering peer.keep_alive_request")
    sock = utils.send_request(server_ip, server_port, "KeepAlive", params)
    response = utils.accept_response(sock)
    utils.Logging.debug("Exiting peer.keep_alive_request")
    return response.status, response.data["message"]


# Handle an rfc query request
def handle_rfcs_query(rfc_index_head):
    utils.Logging.debug("Entering peer.handle_rfcs_query")
    node_list = records.encode_rfc_list(rfc_index_head)
    utils.Logging.debug("Exiting peer.handle_rfcs_query")
    return {"rfcs": node_list}


# Handle an rfc query request
def handle_get_rfc(rfc_file):
    f = open(rfc_file, "rb")
    data = f.read(1024)
    while data:
        yield data
    f.close()




