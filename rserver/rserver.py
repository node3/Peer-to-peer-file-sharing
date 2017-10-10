from request_handler import *
import json
import socket


def load_config():
    with open('../config.json') as config_file:
        config = json.load(config_file)
    return config


## Do ttl reduction flow


def main():
    config = load_config()
    head = None

    # Create socket and listen for incoming connections
    try:
        server_address = (config["rs"]["address"], config["rs"]["port"])
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(server_address)
        sock.listen(1)
        print "Started registration server on (%s, %s)" % server_address
    except socket.error as err:
        print "Socket creation failed with error %s" % err

    # Accept incoming connections
    while True:
        connection, client_address = sock.accept()
        try:
            print client_address
            data = connection.recv(1024)
            message = utils.Peer2Server(data)
            data = message.data

            # Peer registration flow
            if message.command == "Register":
                if "port" in data:
                    head, data = register(head, message.ip, data["port"])
                    data["cookie"] = head.peer.cookie
                    response = utils.Peer2Server(message.command, sock.getsockname()[0], data)
                    connection.sendall(response.formatted())
                else:
                    raise Exception("Received register request without port field.\n%s" % message.formatted())

            # Peer exit flow
            if message.command == "Leave":
                if "cookie" in data:
                    head, data = leave(head, data["cookie"])
                    response = utils.Peer2Server(message.command, sock.getsockname()[0], data)
                    connection.sendall(response.formatted())
                else:
                    raise Exception("Received leave request without cookie field.\n%s" % message.formatted())

            # Peer query flow
            if message.command == "PQuery":
                p_query(head)

            # Peer keep alive flow
            if message.command == "KeepAlive":
                keep_alive(message.ip, message.data)
        except socket.error as err:
            print "Accept incoming connections failed with error %s" % err

        finally:
            # Clean up the connection
            connection.close()


if __name__ == "__main__": main()