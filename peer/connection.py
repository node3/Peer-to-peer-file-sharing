import socket


# Create a connection object from client to server
def connect2server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip, port)

    try:
        sock.connect(server_address)
    except socket.error as err:
        raise Exception("Connect to server failed with error %s" % err)

    return sock

