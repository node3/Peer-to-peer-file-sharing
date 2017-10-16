import socket
import commons


# Create a connection object from client to server
def connect2server(ip, port):
    commons.Logging.debug("Entering peer.connect2server")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip, port)

    try:
        sock.connect(server_address)
    except socket.error as err:
        raise Exception("Connect to server (%s, %s) failed with error %s" % (ip, port, err))

    commons.Logging.info("Connected to server (%s, %s)" % server_address)
    commons.Logging.debug("Exiting peer.connect2server")
    return sock

