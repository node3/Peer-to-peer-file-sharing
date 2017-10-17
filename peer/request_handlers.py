import pickle
from commands import *


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


# Query a peer for RFCs
def rfcs_query_request(peers):
    utils.Logging.debug("Entering peer.rfcs_query_request")
    rfc_index_head = None
    # Request all peers for RFCs
    for peer in peers:
        sock = utils.send_request(peer["hostname"], peer["port"], "RFCQuery", {})
        response = utils.accept_response(sock)
        if response.status == "200":
            # Create record for each RFC received
            for rfc in response.data["rfcs"]:
                rfc_node = records.RFCs(records.RFC(peer["hostname"], rfc["number"], rfc["title"]))
                rfc_index_head = rfc_node.prepend(rfc_index_head)
    utils.Logging.debug("Exiting peer.rfcs_query_request")
    return rfc_index_head


# Get RFC from a peer
def rfc_request(peer_ip, peer_port, rfc_id, rfc_title):
    utils.Logging.debug("Entering peer.rfc_request")
    sock = utils.send_request(peer_ip, peer_port, "GetRFC", {"rfc": rfc_id})
    rfc_path = os.path.join(get_rfc_dir(), rfc_id + ".txt")
    utils.accept_rfc(sock, rfc_path)
    update_rfc_metadata(rfc_id, rfc_title)
    utils.Logging.debug("Exiting peer.rfc_request")
    return rfc_path


# Handle an rfc query request
def handle_rfcs_query():
    utils.Logging.debug("Entering peer.handle_rfcs_query")
    data = read_rfc_metadata()
    utils.Logging.debug("Exiting peer.handle_rfcs_query")
    return data


# Handle an rfc query request
def handle_get_rfc(rfc_file):
    f = open(rfc_file, "rb")
    data = f.read(1024)
    while data:
        yield data
    f.close()




