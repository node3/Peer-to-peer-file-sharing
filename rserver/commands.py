import records
import utils


# Register a new peer into the server. Creates a new node and adds it to the linked list.
def handle_registeration(head, hostname, port):
    utils.Logging.debug("Entering rserver.handle_registeration")
    new_peer = records.PeerRecord(hostname, port)
    ptr = head
    peer_already_registered = False
    while ptr:
        if ptr.peer.hostname == new_peer.hostname and ptr.peer.port == new_peer.port:
            peer_already_registered = True
            break
        ptr = ptr.nxt
    if not peer_already_registered:
        node = records.Peers(new_peer)
        node.nxt = head
        head = node
        peer_registered = True
    else:
        peer_registered = False
    utils.Logging.debug("Exiting rserver.handle_registeration")
    return head, peer_registered


# Removes a peer from the linked list
def handle_leaving(head, cookie):
    utils.Logging.debug("Entering rserver.handle_leaving")
    prev = None
    ptr = head
    peer_ejected = False
    while ptr:
        if ptr.peer.cookie == cookie:
            if not prev:            # cookie found in first node
                head = ptr.nxt
            elif not ptr.nxt:       # cookie found in last node
                prev.nxt = None
            else:                   # cookie in the middle
                prev.nxt = ptr.nxt
            peer_ejected = True
            break
        else:
            ptr = ptr.nxt
    utils.Logging.debug("Exiting rserver.handle_leaving")
    return head, peer_ejected


# Query peers from the server
def handle_peer_query(head, cookie):
    utils.Logging.debug("Entering rserver.handle_peer_query")
    ptr = head
    data = {"peers": []}
    while ptr:
        if ptr.peer.cookie != cookie:
            peer = {
                        "hostname": ptr.peer.hostname,
                        "port": ptr.peer.port
                    }
            data["peers"].append(peer)
        ptr = ptr.nxt
    utils.Logging.debug("Exiting rserver.handle_peer_query")
    return data


# Top up the TTL for a peer
def handle_keep_alive(head, cookie):
    utils.Logging.debug("Entering rserver.handle_keep_alive")
    ttl_updated = False
    ptr = head
    while ptr:
        if ptr.peer.cookie == cookie:
            ptr.peer.initialize_ttl()
            ttl_updated = True
            break
        else:
            ptr = ptr.nxt
    utils.Logging.debug("Exiting rserver.handle_keep_alive")
    return ttl_updated
