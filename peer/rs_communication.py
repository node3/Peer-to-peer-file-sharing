import records
import utils
from connection import *
import commons


# Handles the request response between client and rs 
def rs_communication(server_ip, server_port, command, data):
    commons.Logging.debug("Entering peer.rs_communication")
    sock = connect2server(server_ip, server_port)

    # Encode the request
    request = records.P2PRequest(command, data)

    # Send request to server
    try:
        commons.Logging.info("Sending request \n%s" % request.display())
        sock.sendall(request.encode())
    except socket.error as err:
        raise Exception("\nFailed to send %s request to server with error %s" % command, err)

    # Receive response from server
    try:
        msg_str = sock.recv(1024)
    except socket.error as err:
        raise Exception("\nFailed to receive %s response from server with error %s" % command, err)

    # Decode the response
    response = records.P2PResponse.decode(msg_str)
    commons.Logging.info("Received response \n%s" % response.display())
    commons.Logging.info("Interpretation of the server response code : %s" % response.status_message())
    sock.close()
    commons.Logging.debug("Exiting peer.rs_communication")
    return response


# Register a client with the server
def register(server_ip, server_port, client_port):
    commons.Logging.debug("Entering peer.register")
    data = {"port": client_port}
    response = rs_communication(server_ip, server_port, "Register", data)
    commons.Logging.debug("Exiting peer.register")
    return response.data["cookie"]


# De-register a client from the server
def leave(server_ip, server_port, cookie):
    commons.Logging.debug("Entering peer.leave")
    data = {"cookie": cookie}
    rs_communication(server_ip, server_port, "Leave", data)
    commons.Logging.debug("Exiting peer.leave")
    return None


# Send keep alive signal
def keep_alive(server_ip, server_port, cookie):
    commons.Logging.debug("Entering peer.keep_alive")
    data = {"cookie": cookie}
    rs_communication(server_ip, server_port, "KeepAlive", data)
    commons.Logging.debug("Exiting peer.keep_alive")
    return None


# Query for peers
def p_query(server_ip, server_port, cookie):
    commons.Logging.debug("Entering peer.p_query")
    data = {"cookie": cookie}
    response = rs_communication(server_ip, server_port, "PQuery", data)
    commons.Logging.debug("Exiting peer.p_query")
    return response.data["peers"]
