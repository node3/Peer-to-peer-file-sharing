import records
import time
import utils


def is_peer_registered(head, hostname, port):
    ptr = head
    peer_registered = False
    while ptr:
        if ptr.peer.hostname == hostname and ptr.peer.port == port:
            peer_registered = True
            break
        ptr = ptr.nxt
    return peer_registered


def register_peer(head, hostname, port):
    new_peer = records.PeerRecord(hostname, port)
    node = records.Peers(new_peer)
    node.nxt = head
    return node


def periodic_ttl_reduction(head, last_time_updated):
    if head:
        current_time = int(time.time())
        decrement_value = current_time - last_time_updated
        utils.Logging.debug("TTL reduction by %s" % decrement_value)
        ptr = head
        while ptr:
            ptr.peer.decrement_ttl(decrement_value)
            ptr = ptr.nxt
