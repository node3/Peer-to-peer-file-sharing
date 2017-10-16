import socket
import records
import commons


def listening_socket(server_address):
    commons.Logging.debug("Entering rserver.listening_socket")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(server_address)
        sock.listen(1)
        commons.Logging.info("Registration server listening on (%s, %s)" % server_address)
    except socket.error as err:
        raise Exception("listening_socket failed with error \n%s\n Possibly the port is busy. Try some other port."
                        % err)
    commons.Logging.debug("Exiting rserver.listening_socket")
    return sock


def accept_connection(sock):
    commons.Logging.debug("Entering rserver.accept_connection")
    try:
        connection, client_address = sock.accept()
        commons.Logging.info("Received connection request from (%s, %s)" % client_address)
        raw_msg = connection.recv(1024)
        request = records.P2PRequest.decode(raw_msg)
        commons.Logging.info("Received message \n%s" % request.display())
        commons.Logging.debug("Exiting rserver.accept_connection")
        return connection, request
    except socket.error as err:
        raise Exception("accept_connection failed with error %s" % err)


def respond_to_connection(connection, response):
    commons.Logging.debug("Entering rserver.respond_to_connection")
    commons.Logging.info("Responding with message \n%s" % response.display())
    try:
        connection.sendall(response.encode())
        connection.close()
    except socket.error as err:
        raise Exception("respond_to_connection failed with error %s" % err)
    commons.Logging.debug("Exiting rserver.respond_to_connection")
