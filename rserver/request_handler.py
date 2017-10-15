import record
import encode
import commons


# multiplex the request to appropriate command with respective parameters
def process_request(head, request):
    if request.command == "Register":
        if "port" in request.data:
            head, data = register(head, request.ip, request.data["port"])
            data["cookie"] = head.peer.cookie
            return head, encode.Peer2Server(request.command, commons.get_ip_address(), data)
        else:
            raise Exception("Received register request without port field.\n%s" % request.formatted())

    elif request.command == "Leave":
        if "cookie" in request.data:
            head, data = leave(head, request.data["cookie"])
            return head, encode.Peer2Server(request.command, commons.get_ip_address(), data)
        else:
            raise Exception("Received leave request without cookie field.\n%s" % request.formatted())

    elif request.command == "PQuery":
        if "cookie" in request.data:
            data = p_query(head, request.data["cookie"])
            return head, encode.Peer2Server(request.command, commons.get_ip_address(), data)
        else:
            raise Exception("Received pquery request without cookie field.\n%s" % request.formatted())

    elif request.command == "KeepAlive":
        if "cookie" in request.data:
            data = keep_alive(head, request.data["cookie"])
            return head, encode.Peer2Server(request.command, commons.get_ip_address(), data)
        else:
            raise Exception("Received pquery request without cookie field.\n%s" % request.formatted())

    else:
        raise Exception("Request has an invalid command. See encode package for message format.")


# Register a new peer into the server. Creates a new node and adds it to the linked list.
def register(head, ip, port):
    peer = record.PeerRecord(ip, port)
    node = record.Peers(peer)
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
def p_query(head, cookie):
    ptr = head
    data = {"peers": [1, 3, 2, 4]}
    # data = {"peers": []}
    while ptr:
        if ptr.peer.cookie != cookie:
            data["peers"].append(ptr.peer.ip)
        ptr = ptr.nxt
    return data


# Register a new peer into the server
def keep_alive(head, cookie):
    data = {"status": "Failed"}
    ptr = head
    while ptr:
        if ptr.peer.cookie == cookie:
            ptr.peer.initialize_ttl()
            data["status"] = "Success"
            break
        else:
            ptr = ptr.nxt
    return data
