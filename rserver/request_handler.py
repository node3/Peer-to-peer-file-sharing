import utils


# Register a new peer into the server.
# Creates a new node and adds it to the linked list.
def register(head, ip, port):
    peer = utils.PeerRecord(ip, port)
    node = utils.Peers(peer)
    node.nxt = head
    data = {"status": "Success"}
    return node, data


# Leave removes a peer from the linked list
def leave(head, cookie):
    data = {"status": "Failed"}
    prev = None
    ptr = head
    while ptr:
        if ptr.peer.cookie == cookie:
            if not prev:            # cookie found in first node
                head = ptr
            elif not ptr.nxt:       # cookie found in last node
                prev.nxt = None
            else:                   # cookie in the middle
                prev.nxt = ptr.nxt
            data["status"] = "Success"
            break
        else:
            ptr = ptr.nxt
    return head, data


# Query peers from the server
def p_query(head):
    print head
    return


# Register a new peer into the server
def keep_alive(head, cookie):
    print cookie
    return

