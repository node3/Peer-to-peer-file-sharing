import records
from connection import *
from utils import *
import commons
import pickle


# Handles the request response between peer and peer
def peer_communication(peer_ip, peer_port, command, data):
    commons.Logging.debug("Entering peer.peer_communication")
    sock = connect2server(peer_ip, peer_port)

    # Encode the request
    request = records.P2PRequest(command, data)

    # Send request to peer
    try:
        commons.Logging.info("Sending request \n%s" % request.display())
        sock.sendall(request.encode())
    except socket.error as err:
        raise Exception("\nFailed to send %s request to peer with error %s" % command, err)

    # Receive response from peer
    try:
        msg_str = sock.recv(1024)
    except socket.error as err:
        raise Exception("\nFailed to receive %s response from peer with error %s" % command, err)

    # Decode the response
    response = records.P2PResponse.decode(msg_str)
    commons.Logging.info("Received response \n%s" % response.current_state())

    sock.close()
    commons.Logging.debug("Exiting peer.peer_communication")
    return response


# Query a peer for RFCs
def rfc_query(peers):
    commons.Logging.debug("Entering peer.rfc_query")
    rfc_index_head = None
    data = {}
    # Request all peers for RFCs
    for peer in peers:
        response = peer_communication(peer["hostname"], peer["port"], "RFCQuery", data)
        # Create record for each RFC received
        for rfc in response.data["rfcs"]:
            rfc_node = records.RFCIndex(records.RFC(peer["hostname"], rfc["number"], rfc["title"]))
            # Insert record into a linked list
            if rfc_index_head:
                rfc_node.nxt = rfc_index_head
            rfc_index_head = rfc_node
    commons.Logging.debug("Exiting peer.rfc_query")
    return rfc_index_head


# Get RFC from a peer
def get_rfc(peer_ip, peer_port, rfc_id):
    commons.Logging.debug("Entering peer.get_rfc")
    data = {"rfc": rfc_id}
    response = peer_communication(peer_ip, peer_port, "GetRFC", data)
    rfc_path = os.path.join(get_rfc_dir(), rfc_id + ".txt")
    with open(rfc_path, "w") as f:
        f.writelines(pickle.loads(response.data))
    commons.Logging.debug("Exiting peer.get_rfc")
    return rfc_path
