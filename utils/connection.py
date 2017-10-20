import socket
import records
from commons import *
from time import sleep
import utils

CONNECT_TIMEOUT = 5
BIND_TIMEOUT = 120


# Create a connection object from client to server
def connect2server(hostname, port):
    Logging.debug("Entering utils.connect2server")
    socket.setdefaulttimeout(CONNECT_TIMEOUT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (hostname, port)

    try:
        sock.connect(server_address)
    except socket.error as err:
        raise Exception("Connect to server (%s, %s) failed due to %s" % (hostname, port, err))

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
        sock.close()
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


# Open a socket to listen for clients
def listen4clients(server_address):
    Logging.debug("Entering utils.listen4clients")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    timeout = BIND_TIMEOUT
    while timeout > 0:
        try:
            sock.bind(server_address)
            sock.listen(1)
            Logging.info("Server listening on %s" % str(server_address))
            break
        except socket.error as err:
            Logging.info("%s. Retrying..." % err)
            sleep(5)
            timeout -= 5
    if timeout <= 0:
        raise Exception("Could not bind to %s within %d seconds. Server could not be started."
                        % (str(server_address), BIND_TIMEOUT))
    else:
        Logging.debug("Exiting utils.listen4clients")
        return sock


# Accept request messages from a client
def accept_request(sock):
    Logging.debug("Entering utils.accept_request")
    try:
        connection, client_address = sock.accept()
        Logging.info("Received connection request from %s" % str(client_address))
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
        raise Exception("send_response failed with error %s" % err)
    Logging.debug("Exiting utils.send_response")


# Accept rfc
def accept_rfc(sock, rfc_number):
    Logging.debug("Entering utils.accept_rfc")

    # Accept the first message with the status code and file format
    try:
        msg_str = sock.recv(1024)
    except socket.error as err:
        Logging.info("accept_rfc failed with error %s" % err)
        return None, None
    response = records.P2PResponse.decode(msg_str)
    Logging.info("Received response \n%s" % response.display())

    # Accept the RFC
    rfc_format = None
    if response.status == "200":
        download_path = os.path.join(utils.get_rfc_dir(), ".".join([rfc_number, response.data["format"]]))
        try:
            f = open(download_path, "wb")
            raw_msg = sock.recv(1024)
            while raw_msg:
                Logging.debug(raw_msg)
                f.write(raw_msg)
                raw_msg = sock.recv(1024)
            sock.close()
        except socket.error as err:
            Logging.info("Could not download the complete rfc. %s" % err)
            download_path = None
        f.close()
        rfc_format = response.data["format"]
    else:
        Logging.info("Could not download the rfc. %s" % response.data["message"])
        download_path = None
    Logging.debug("Exiting utils.accept_rfc")
    return download_path, rfc_format


# Send rfc
def send_rfc(connection, file_path, rfc_format):
    Logging.debug("Entering utils.send_rfc")

    # Send the file found and format message
    response = records.P2PResponse("200", {"format": rfc_format})
    Logging.info("Responding with message \n%s" % response.display())
    try:
        connection.sendall(response.encode())
    except socket.error as err:
        raise Exception("send_rfc failed with error %s" % err)

    # Send the rfc
    try:
        f = open(file_path, "rb")
        msg = f.read(1024)
        while msg:
            Logging.debug(msg)
            connection.sendall(msg)
            msg = f.read(1024)
        connection.shutdown(socket.SHUT_WR)
        f.close()
        connection.close()
    except socket.error as err:
        Logging.info("Could not send the complete rfc. %s" % err)
    Logging.debug("Exiting utils.send_rfc")
    return


# Get local ip address
def get_ip_address():
    return "localhost"
    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.connect(("8.8.8.8", 80))
    # ip = s.getsockname()[0]
    # s.close()
    # return ip
