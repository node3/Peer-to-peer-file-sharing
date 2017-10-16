import socket
import records
from commons import *


# Create a connection object from client to server
def connect2server(hostname, port):
    Logging.debug("Entering utils.connect2server")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (hostname, port)

    try:
        sock.connect(server_address)
    except socket.error as err:
        raise Exception("Connect to server (%s, %s) failed with error %s" % (hostname, port, err))

    Logging.info("Connected to server (%s, %s)" % server_address)
    Logging.debug("Exiting utils.connect2server")
    return sock


# Send a request to server
def send_request(peer_ip, peer_port, command, data):
    Logging.debug("Entering utils.send_request")
    sock = connect2server(peer_ip, peer_port)

    # Encode the request
    request = records.P2PRequest(command, data)

    # Send request to peer
    try:
        Logging.info("Sending request \n%s" % request.display())
        sock.sendall(request.encode())
    except socket.error as err:
        raise Exception("send_request failed with error %s" % err)
    Logging.debug("Exiting utils.send_request")
    return sock


# Get a response from the server
def accept_response(sock):
    Logging.debug("Entering utils.accept_response")

    # Receive response from peer
    try:
        msg_str = sock.recv(1024)
    except socket.error as err:
        raise Exception("accept_response failed with error %s" % err)

    # Decode the response
    response = records.P2PResponse.decode(msg_str)
    Logging.info("Received response \n%s" % response.display())
    Logging.info("Response code interpretation : %s" % response.status_message())
    sock.close()
    Logging.debug("Exiting utils.accept_response")
    return response

