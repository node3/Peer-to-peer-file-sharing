import socket
import protocol
from utils import *


def listening_socket(server_address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(server_address)
        sock.listen(1)
    except socket.error as err:
        print "listening_socket failed with error %s" % err
    print "Registration server listening on (%s, %s)" % server_address
    return sock


def accept_connection(sock):
    try:
        connection, client_address = sock.accept()
        raw_msg = connection.recv(1024)
        request = protocol.Peer2Server(raw_msg)
        req_print(request)
        return connection, request
    except socket.error as err:
        print "accept_connection failed with error %s" % err


def respond_to_connection(connection, response):
    resp_print(response)
    try:
        connection.sendall(response.formatted())
        connection.close()
    except socket.error as err:
        print "respond_to_connection failed with error %s" % err
