import record
import encode
import commons


# multiplex the request to appropriate command with respective parameters
def process_request(head, request):
    commons.debug("Entering rserver.process_request")
    if request.command == "Register":
        if "port" in request.data:
            head, data = register(head, request.ip, request.data["port"])
            data["cookie"] = head.peer.cookie
            message = encode.Peer2Server(request.command, commons.get_ip_address(), data)
        else:
            raise Exception("Received Register request without port field.\n%s" % request.formatted())

    elif request.command == "Leave":
        if "cookie" in request.data:
            head, data = leave(head, request.data["cookie"])
            message = encode.Peer2Server(request.command, commons.get_ip_address(), data)
        else:
            raise Exception("Received Leave request without cookie field.\n%s" % request.formatted())

    elif request.command == "PQuery":
        if "cookie" in request.data:
            data = p_query(head, request.data["cookie"])
            message = encode.Peer2Server(request.command, commons.get_ip_address(), data)
        else:
            raise Exception("Received PQuery request without cookie field.\n%s" % request.formatted())

    elif request.command == "KeepAlive":
        if "cookie" in request.data:
            data = keep_alive(head, request.data["cookie"])
            message = encode.Peer2Server(request.command, commons.get_ip_address(), data)
        else:
            raise Exception("Received KeepAlive request without cookie field.\n%s" % request.formatted())

    else:
        raise Exception("Request has an invalid command. See encode package for message format.")

    commons.debug("Exiting rserver.process_request")
    return head, message


# Register a new peer into the server. Creates a new node and adds it to the linked list.
def register(head, ip, port):
    commons.debug("Entering rserver.register")
    peer = record.PeerRecord(ip, port)
    node = record.Peers(peer)
    node.nxt = head
    data = {"status": "Success"}
    commons.debug("Exiting rserver.register")
    return node, data


# Leave removes a peer from the linked list
def leave(head, cookie):
    commons.debug("Entering rserver.leave")
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
    commons.debug("Exiting rserver.leave")
    return head, data


# Query peers from the server
def p_query(head, cookie):
    commons.debug("Entering rserver.p_query")
    ptr = head
    data = {"peers": [1, 3, 2, 4]}
    # data = {"peers": []}
    while ptr:
        if ptr.peer.cookie != cookie:
            data["peers"].append(ptr.peer.ip)
        ptr = ptr.nxt
    commons.debug("Exiting rserver.p_query")
    return data


# Register a new peer into the server
def keep_alive(head, cookie):
    commons.debug("Entering rserver.keep_alive")
    data = {"status": "Failed"}
    ptr = head
    while ptr:
        if ptr.peer.cookie == cookie:
            ptr.peer.initialize_ttl()
            data["status"] = "Success"
            break
        else:
            ptr = ptr.nxt
    commons.debug("Exiting rserver.keep_alive")
    return data
