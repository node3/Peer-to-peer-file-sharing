from commands import *
import datetime


# Register a new peer into the server. Creates a new node and adds it to the linked list.
def handle_registration(head, hostname, port):
    utils.Logging.debug("Entering rserver.handle_registration")
    registry_id = is_peer_registered(head, hostname, port)
    if registry_id == 0:
        head = register_peer(head, hostname, port)
        cookie = head.peer.cookie
        head.peer.last_reg = datetime.datetime.now()
    # This flow is when the peer forgets it cookie and tries to re-register.
    # The server will return its old cookie after recognising it with the hostname and port combination
    else:
        cookie = registry_id
        handle_keep_alive(head, cookie)
    utils.Logging.debug("Exiting rserver.handle_registration")
    return head, cookie


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
            prev = ptr
            ptr = ptr.nxt
    utils.Logging.debug("Exiting rserver.handle_leaving")
    return head, peer_ejected


# Query peers from the server
def handle_peer_query(head, cookie):
    utils.Logging.debug("Entering rserver.handle_peer_query")
    ptr = head
    data = {"peers": []}
    while ptr:
        # Return only active peers
        if ptr.peer.is_active() and ptr.peer.cookie != cookie:
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
            ptr.peer.last_reg = datetime.datetime.now()
            ptr.peer.reg_count += 1
            ttl_updated = True
            break
        else:
            ptr = ptr.nxt
    utils.Logging.debug("Exiting rserver.handle_keep_alive")
    return ttl_updated
