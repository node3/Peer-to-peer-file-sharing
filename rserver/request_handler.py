import records
import commons


# multiplex the request to appropriate command with respective parameters
def process_request(head, request):
    commons.print_msg("Entering rserver.process_request")
    if request.command == "Register":
        if "port" in request.data:
            head, peer_registered = register(head, request.hostname, request.data["port"])
            if peer_registered:
                data = {"cookie": head.peer.cookie}
                status = "200"
            else:
                data = {"message": "Peer already registered with same hostname and port"}
                status = "100"
        else:
            data = {"message": "Received Leave request without port field"}
            status = "300"

    elif request.command == "Leave":
        if "cookie" in request.data:
            head, peer_ejected = leave(head, request.data["cookie"])
            data = {}
            if peer_ejected:
                status = "200"
            else:
                status = "100"
        else:
            data = {"message": "Received Leave request without cookie field"}
            status = "300"

    elif request.command == "PQuery":
        if "cookie" in request.data:
            data = p_query(head, request.data["cookie"])
            status = "200"
        else:
            data = {"message": "Received PQuery request without cookie field"}
            status = "300"

    elif request.command == "KeepAlive":
        if "cookie" in request.data:
            ttl_updated = keep_alive(head, request.data["cookie"])
            data = {}
            if ttl_updated:
                status = "200"
            else:
                status = "100"
        else:
            data = {"message": "Received KeepAlive request without cookie field"}
            status = "300"
    else:
        data = {"message": "Request message has an invalid command"}
        status = "300"

    commons.print_msg("Exiting rserver.process_request")
    response = records.P2PResponse(status, data)
    return head, response


# Register a new peer into the server. Creates a new node and adds it to the linked list.
def register(head, hostname, port):
    commons.print_msg("Entering rserver.register")
    new_peer = records.PeerRecord(hostname, port)
    ptr = head
    peer_already_registered = False
    while ptr:
        if ptr.peer.hostname == new_peer.hostname and ptr.peer.port == new_peer.port:
            peer_already_registered = True
    if not peer_already_registered:
        node = records.Peers(new_peer)
        node.nxt = head
        head = node
        peer_registered = True
    else:
        peer_registered = False
    commons.print_msg("Exiting rserver.register")
    return head, peer_registered


# Leave removes a peer from the linked list
def leave(head, cookie):
    commons.print_msg("Entering rserver.leave")
    prev = None
    ptr = head
    peer_ejected = False
    while ptr:
        if ptr.peer.cookie == cookie:
            if not prev:            # cookie found in first node
                head = ptr
            elif not ptr.nxt:       # cookie found in last node
                prev.nxt = None
            else:                   # cookie in the middle
                prev.nxt = ptr.nxt
            peer_ejected = True
            break
        else:
            ptr = ptr.nxt
    commons.print_msg("Exiting rserver.leave")
    return head, peer_ejected


# Query peers from the server
def p_query(head, cookie):
    commons.print_msg("Entering rserver.p_query")
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
    commons.print_msg("Exiting rserver.p_query")
    return data


# Register a new peer into the server
def keep_alive(head, cookie):
    commons.print_msg("Entering rserver.keep_alive")
    ttl_updated = False
    ptr = head
    while ptr:
        if ptr.peer.cookie == cookie:
            ptr.peer.initialize_ttl()
            ttl_updated = True
            break
        else:
            ptr = ptr.nxt
    commons.print_msg("Exiting rserver.keep_alive")
    return ttl_updated
