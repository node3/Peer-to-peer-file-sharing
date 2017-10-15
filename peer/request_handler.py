import encode
import utils
from connection import *


def rs_req_resp(server_ip, server_port, command, data):
    sock = connect2server(server_ip, server_port)

    # Encode the request
    request = encode.Peer2Server(command, sock.getsockname()[0], data)
    utils.req_print(request)

    # Send request to server
    try:
        sock.sendall(request.formatted())
    except socket.error as err:
        raise Exception("\nFailed to send %s request to server with error %s" % command, err)

    # Receive response from server
    try:
        msg_str = sock.recv(1024)
    except socket.error as err:
        raise Exception("\nFailed to receive %s response from server with error %s" % command, err)

    # Decode the response
    response = encode.Peer2Server(msg_str)
    utils.resp_print(response)
    sock.close()

    return response


# Register a client with the server
def register(server_ip, server_port, client_port):
    data = {"port": client_port}
    response = rs_req_resp(server_ip, server_port, "Register", data)
    return response.data["cookie"]


def leave(server_ip, server_port, cookie):
    data = {"cookie": cookie}
    rs_req_resp(server_ip, server_port, "Leave", data)
    return None


def keep_alive(server_ip, server_port, cookie):
    data = {"cookie": cookie}
    rs_req_resp(server_ip, server_port, "KeepAlive", data)
    return None


def p_query(server_ip, server_port, cookie):
    data = {"cookie": cookie}
    response = rs_req_resp(server_ip, server_port, "PQuery", data)
    return response.data["peers"]