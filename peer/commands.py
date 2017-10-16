import utils
import pickle
import os
import records


# Register a client with the server
def register_request(server_ip, server_port, client_port):
    utils.Logging.debug("Entering peer.handle_registeration")
    sock = utils.send_request(server_ip, server_port, "Register", {"port": client_port})
    response = utils.accept_response(sock)
    if response.status == "200":
        response_ok = True
        data = response.data["cookie"]
    else:
        response_ok = False
        data = response.data["message"]
    utils.Logging.debug("Exiting peer.handle_registeration")
    return response_ok, data


# De-handle_registeration a client from the server
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
def rfc_query_request(peers):
    utils.Logging.debug("Entering peer.rfc_query_request")
    rfc_index_head = None
    data = {}
    # Request all peers for RFCs
    for peer in peers:
        sock = utils.send_request(peer["hostname"], peer["port"], "RFCQuery", data)
        response = utils.accept_response(sock)
        # Create record for each RFC received
        for rfc in response.data["rfcs"]:
            rfc_node = records.RFCIndex(records.RFC(peer["hostname"], rfc["number"], rfc["title"]))
            # Insert record into a linked list
            if rfc_index_head:
                rfc_node.nxt = rfc_index_head
            rfc_index_head = rfc_node
    utils.Logging.debug("Exiting peer.rfc_query_request")
    return rfc_index_head


# Get RFC from a peer
def get_rfc(peer_ip, peer_port, rfc_id):
    utils.Logging.debug("Entering peer.get_rfc")
    data = {"rfc": rfc_id}
    sock = utils.send_request(peer_ip, peer_port, "GetRFC", data)
    response = utils.accept_response(sock)
    rfc_path = os.path.join(get_rfc_dir(), rfc_id + ".txt")
    with open(rfc_path, "w") as f:
        f.writelines(pickle.loads(response.data))
    utils.Logging.debug("Exiting peer.get_rfc")
    return rfc_path


def get_rfc_dir():
    rfc_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rfc")
    if not os.path.exists(rfc_dir):
        os.makedirs(rfc_dir)
    return rfc_dir
