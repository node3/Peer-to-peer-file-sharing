import utils


# Register a new peer into the server.
# Creates a new node and adds it to the linked list.
def register(head, ip, port):
    peer = utils.PeerRecord(ip, port)
    node = utils.Peers(peer)
    node.nxt = head
    return node


# Leave removes a peer from the linked list
def leave(head, cookie):
    print cookie
    return


# Query peers from the server
def p_query(head):
    print head
    return


# Register a new peer into the server
def keep_alive(head, cookie):
    print cookie
    return

