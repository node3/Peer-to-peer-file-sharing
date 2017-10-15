import socket
import encode
from utils import *
import commons


def listening_socket(server_address):
    commons.debug("Entering rserver.listening_socket")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(server_address)
        sock.listen(1)
        commons.debug("Registration server listening on (%s, %s)" % server_address)
    except socket.error as err:
        raise Exception("listening_socket failed with error \n%s\n Possibly the port is busy. Try some other port."
                        % err)
    commons.debug("Exiting rserver.listening_socket")
    return sock


def accept_connection(sock):
    commons.debug("Entering rserver.accept_connection")
    try:
        connection, client_address = sock.accept()
        commons.debug("Received connection request from (%s, %s)" % client_address)
        raw_msg = connection.recv(1024)
        request = encode.Peer2Server(raw_msg)
        commons.debug("Received message %s" % request.formatted())
        req_print(request)
        commons.debug("Exiting rserver.accept_connection")
        return connection, request
    except socket.error as err:
        print "accept_connection failed with error %s" % err


def respond_to_connection(connection, response):
    commons.debug("Entering rserver.respond_to_connection")
    resp_print(response)
    commons.debug("Responding with message %s" % response.formatted())
    try:
        connection.sendall(response.formatted())
        connection.close()
    except socket.error as err:
        print "respond_to_connection failed with error %s" % err
    commons.debug("Connection closed")
    commons.debug("Exiting rserver.respond_to_connection")
