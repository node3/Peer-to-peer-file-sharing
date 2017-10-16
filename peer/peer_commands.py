# from connection import *
import utils
import pickle
import os
import records


# Query a peer for RFCs
def rfc_query(peers):
    utils.Logging.debug("Entering peer.rfc_query")
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
    utils.Logging.debug("Exiting peer.rfc_query")
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
