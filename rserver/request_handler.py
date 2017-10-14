import record
import protocol
import commons


# multiplex the request to appropriate command with respective parameters
def process_request(head, request):
    if request.command == "Register":
        if "port" in request.data:
            head, data = register(head, request.ip, request.data["port"])
            data["cookie"] = head.peer.cookie
            return head, protocol.Peer2Server(request.command, commons.get_ip_address(), data)
        else:
            raise Exception("Received register request without port field.\n%s" % request.formatted())

    elif request.command == "Leave":
        if "cookie" in request.data:
            head, data = leave(head, request.data["cookie"])
            return head, protocol.Peer2Server(request.command, commons.get_ip_address(), data)
        else:
            raise Exception("Received leave request without cookie field.\n%s" % request.formatted())

    # Peer query flow
    elif request.command == "PQuery":
        p_query(head)

    # Peer keep alive flow
    elif request.command == "KeepAlive":
        keep_alive(request.ip, request.data)

    else:
        print "Request has an invalid command. See protocol package for message format."


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
def p_query(head):
    print head
    return


# Register a new peer into the server
def keep_alive(head, cookie):
    print cookie
    return

