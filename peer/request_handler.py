import records
import utils
from connection import *
import commons


def rs_req_resp(server_ip, server_port, command, data):
    commons.debug("Entering peer.rs_req_resp")
    sock = connect2server(server_ip, server_port)

    # Encode the request
    request = records.Peer2Server(command, commons.get_ip_address(), data)
    utils.req_print(request)

    # Send request to server
    try:
        sock.sendall(request.encode())
        commons.debug("Request sent %s" % request.encode())
    except socket.error as err:
        raise Exception("\nFailed to send %s request to server with error %s" % command, err)

    # Receive response from server
    try:
        msg_str = sock.recv(1024)
        commons.debug("Response received %s" % msg_str)
    except socket.error as err:
        raise Exception("\nFailed to receive %s response from server with error %s" % command, err)

    # Decode the response
    response = records.Peer2Server(msg_str)
    utils.resp_print(response)
    sock.close()

    commons.debug("Exiting peer.rs_req_resp")
    return response


# Register a client with the server
def register(server_ip, server_port, client_port):
    commons.debug("Entering peer.register")
    data = {"port": client_port}
    response = rs_req_resp(server_ip, server_port, "Register", data)
    commons.debug("Exiting peer.register")
    return response.data["cookie"]


def leave(server_ip, server_port, cookie):
    commons.debug("Entering peer.leave")
    data = {"cookie": cookie}
    rs_req_resp(server_ip, server_port, "Leave", data)
    commons.debug("Exiting peer.leave")
    return None


def keep_alive(server_ip, server_port, cookie):
    commons.debug("Entering peer.keep_alive")
    data = {"cookie": cookie}
    rs_req_resp(server_ip, server_port, "KeepAlive", data)
    commons.debug("Exiting peer.keep_alive")
    return None


def p_query(server_ip, server_port, cookie):
    commons.debug("Entering peer.p_query")
    data = {"cookie": cookie}
    response = rs_req_resp(server_ip, server_port, "PQuery", data)
    commons.debug("Exiting peer.p_query")
    return response.data["peers"]