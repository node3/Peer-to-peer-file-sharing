from request_handler import *
import json
import socket


def load_config():
    with open('../config.json') as config_file:
        config = json.load(config_file)
    return config


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
            try:
                data = json.loads(message.data)
            except ValueError:
                print 'Request handler failed to load json'

            if message.command == "Register":
                if "port" in data:
                    head = register(head, message.ip, data["port"])
                    response = utils.Peer2Server("Register", sock.getsockname()[0], "Success")
                    connection.sendall(response.formatted())
                else:
                    raise Exception("Received register request without port field.\n%s" % message.formatted())

            if message.command == "Leave":
                leave(head, message.ip)
            if message.command == "PQuery":
                p_query(head)
            if message.command == "KeepAlive":
                keep_alive(message.ip, message.data)
        except socket.error as err:
            print "Accept incoming connections failed with error %s" % err

        finally:
            # Clean up the connection
            connection.close()


if __name__ == "__main__": main()