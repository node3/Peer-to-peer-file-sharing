import records
import utils
from connection import *
import commons


# Handles the request response between client and rs 
def rs_communication(server_ip, server_port, command, data):
    commons.print_msg("Entering peer.rs_communication")
    sock = connect2server(server_ip, server_port)

    # Encode the request
    request = records.P2PRequest(command, data)

    # Send request to server
    try:
        commons.print_msg("Sending request \n%s" % request.display())
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
    commons.print_msg("Received response \n%s" % response.display())
    commons.print_msg("Interpretation of the server response code : %s" % response.status_message())
    sock.close()
    commons.print_msg("Exiting peer.rs_communication")
    return response


# Register a client with the server
def register(server_ip, server_port, client_port):
    commons.print_msg("Entering peer.register")
    data = {"port": client_port}
    response = rs_communication(server_ip, server_port, "Register", data)
    commons.print_msg("Exiting peer.register")
    return response.data["cookie"]


# De-register a client from the server
def leave(server_ip, server_port, cookie):
    commons.print_msg("Entering peer.leave")
    data = {"cookie": cookie}
    rs_communication(server_ip, server_port, "Leave", data)
    commons.print_msg("Exiting peer.leave")
    return None


# Send keep alive signal
def keep_alive(server_ip, server_port, cookie):
    commons.print_msg("Entering peer.keep_alive")
    data = {"cookie": cookie}
    rs_communication(server_ip, server_port, "KeepAlive", data)
    commons.print_msg("Exiting peer.keep_alive")
    return None


# Query for peers
def p_query(server_ip, server_port, cookie):
    commons.print_msg("Entering peer.p_query")
    data = {"cookie": cookie}
    response = rs_communication(server_ip, server_port, "PQuery", data)
    commons.print_msg("Exiting peer.p_query")
    return response.data["peers"]
