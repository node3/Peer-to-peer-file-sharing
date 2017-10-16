import utils


# Register a client with the server
def register(server_ip, server_port, client_port):
    utils.Logging.debug("Entering peer.handle_registeration")
    sock = utils.send_request(server_ip, server_port, "Register", {"port": client_port})
    response = utils.accept_response(sock)
    if response.status == "200":
        response_ok = True
        data = response.data["cookie"]
    else:
        response_ok = False
        data = response.data["message"]
    utils.Logging.debug("Exiting peer.handle_registeration")
    return response_ok, data


# De-handle_registeration a client from the server
def leave(server_ip, server_port, cookie):
    utils.Logging.debug("Entering peer.handle_leaving")
    data = {"cookie": cookie}
    sock = utils.send_request(server_ip, server_port, "Leave", data)
    response = utils.accept_response(sock)
    if response.status == "201":
        response_ok = True
        data = None
    else:
        response_ok = False
        data = response.data["message"]
    utils.Logging.debug("Exiting peer.handle_leaving")
    return response_ok, data


# Query for peers
def p_query(server_ip, server_port, cookie):
    utils.Logging.debug("Entering peer.handle_peer_query")
    sock = utils.send_request(server_ip, server_port, "PQuery", {"cookie": cookie})
    response = utils.accept_response(sock)
    if response.status == "200":
        response_ok = True
        data = response.data["peers"]
    else:
        response_ok = False
        data = response.data["message"]
    utils.Logging.debug("Exiting peer.handle_peer_query")
    return response_ok, data


# Send keep alive signal
def keep_alive(server_ip, server_port, cookie):
    utils.Logging.debug("Entering peer.handle_keep_alive")
    sock = utils.send_request(server_ip, server_port, "KeepAlive", {"cookie": cookie})
    response = utils.accept_response(sock)
    utils.Logging.debug("Exiting peer.handle_keep_alive")
    if response.status == "201":
        response_ok = True
        data = None
    else:
        response_ok = False
        data = response.data["message"]
    utils.Logging.debug("Exiting peer.handle_leaving")
    return response_ok, data

