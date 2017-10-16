import socket
import records
from commons import *


# Open a socket to listen for clients
def listen4clients(server_address):
    Logging.debug("Entering utils.listen4clients")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(server_address)
        sock.listen(1)
        Logging.info("Server listening on (%s, %s)" % server_address)
    except socket.error as err:
        raise Exception("listen4clients failed with error \n%s\n Possibly the port is busy." % err)
    Logging.debug("Exiting utils.listen4clients")
    return sock


# Accept request messages from a client
def accept_request(sock):
    Logging.debug("Entering utils.accept_request")
    try:
        connection, client_address = sock.accept()
        Logging.info("Received connection request from (%s, %s)" % client_address)
        raw_msg = connection.recv(1024)
    except socket.error as err:
        raise Exception("accept_request failed with error %s" % err)
    request = records.P2PRequest.decode(raw_msg)
    Logging.info("Received message \n%s" % request.display())
    Logging.debug("Exiting utils.accept_request")
    return connection, request


# Respond to a client
def send_response(connection, response):
    Logging.debug("Entering utils.send_response")
    Logging.info("Responding with message \n%s" % response.display())
    try:
        connection.sendall(response.encode())
        connection.close()
    except socket.error as err:
        raise Exception("respond_to_connection failed with error %s" % err)
    Logging.debug("Exiting utils.send_response")
