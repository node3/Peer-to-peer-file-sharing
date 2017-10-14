import protocol
import socket
import utils


# Register a client with the server
def register(sock, client_port):
    data = {"port": client_port}

    # Encode the request to register
    request = protocol.Peer2Server("Register", sock.getsockname()[0], "%s" % str(data))
    utils.req_print(request)

    # Send register request to server
    try:
        sock.sendall(request.formatted())
    except socket.error as err:
        raise Exception("\nFailed to send registration request to server with error %s" % err)

    # Receive register response
    try:
        msg_str = sock.recv(1024)
    except socket.error as err:
        raise Exception("\nFailed to receive registration response from server with error %s" % err)

    # Decode the response from server
    response = protocol.Peer2Server(msg_str)
    utils.resp_print(response)
    return response.data["cookie"]


def leave(sock, cookie):
    data = {"cookie": cookie}

    # Encode the request to leave
    request = protocol.Peer2Server("Leave", sock.getsockname()[0], "%s" % data)
    utils.req_print(request)

    # Send leave request to server
    try:
        sock.sendall(request.formatted())
    except socket.error as err:
        raise Exception("\nFailed to send leave request to server with error %s" % err)

    # Receive leave response
    try:
        msg_str = sock.recv(1024)
    except socket.error as err:
        raise Exception("\nFailed to receive leave response from server with error %s" % err)

    # Decode the response from server
    response = protocol.Peer2Server(msg_str)
    utils.resp_print(response)
