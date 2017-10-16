import pickle
from commons import *


# Register a client with the server
def register_request(server_ip, server_port, client_port):
    utils.Logging.debug("Entering peer.register_request")
    sock = utils.send_request(server_ip, server_port, "Register", {"port": client_port})
    response = utils.accept_response(sock)
    if response.status == "200":
        response_ok = True
        data = response.data["cookie"]
    else:
        response_ok = False
        data = response.data["message"]
    utils.Logging.debug("Exiting peer.register_request")
    return response_ok, data


# De-registeration a client from the server
def leave_request(server_ip, server_port, cookie):
    utils.Logging.debug("Entering peer.leave_request")
    data = {"cookie": cookie}
    sock = utils.send_request(server_ip, server_port, "Leave", data)
    response = utils.accept_response(sock)
    if response.status == "201":
        response_ok = True
        data = None
    else:
        response_ok = False
        data = response.data["message"]
    utils.Logging.debug("Exiting peer.leave_request")
    return response_ok, data


# Query for peers
def peer_query_request(server_ip, server_port, cookie):
    utils.Logging.debug("Entering peer.peer_query_request")
    sock = utils.send_request(server_ip, server_port, "PQuery", {"cookie": cookie})
    response = utils.accept_response(sock)
    if response.status == "200":
        response_ok = True
        data = response.data["peers"]
    else:
        response_ok = False
        data = response.data["message"]
    utils.Logging.debug("Exiting peer.peer_query_request")
    return response_ok, data


# Send keep alive signal
def keep_alive_request(server_ip, server_port, cookie):
    utils.Logging.debug("Entering peer.keep_alive_request")
    sock = utils.send_request(server_ip, server_port, "KeepAlive", {"cookie": cookie})
    response = utils.accept_response(sock)
    if response.status == "201":
        response_ok = True
        data = None
    else:
        response_ok = False
        data = response.data["message"]
    utils.Logging.debug("Exiting peer.keep_alive_request")
    return response_ok, data


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
def get_rfc(peer_ip, peer_port, rfc_id):
    utils.Logging.debug("Entering peer.get_rfc")
    sock = utils.send_request(peer_ip, peer_port, "GetRFC", {"rfc": rfc_id})
    response = utils.accept_response(sock)
    rfc_path = os.path.join(get_rfc_dir(), rfc_id + ".txt")
    with open(rfc_path, "w") as f:
        f.writelines(pickle.loads(response.data))
    utils.Logging.debug("Exiting peer.get_rfc")
    return rfc_path


# Handle an rfc query request
def handle_rfcs_query():
    utils.Logging.debug("Entering peer.handle_rfcs_query")
    data = read_rfc_metadata()
    utils.Logging.debug("Exiting peer.handle_rfcs_query")
    return data


# Handle an rfc query request
def handle_get_rfc(rfc_number):
    utils.Logging.debug("Entering peer.handle_rfcs_query")
    data = None
    utils.Logging.debug("Exiting peer.handle_rfcs_query")
    return data

