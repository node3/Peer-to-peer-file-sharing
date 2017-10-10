import socket
import json
import utils


def load_config():
    with open('../config.json') as config_file:
        config = json.load(config_file)
    return config


def main():
    i_am = "1"
    config = load_config()

    # Connect to server
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (config["rs"]["address"], config["rs"]["port"])
        sock.connect(server_address)
    except socket.error as err:
        print "Connect to server failed with error %s" % err

    try:
        # Register
        print "\nRegistering..."
        data = {"port": config["rs"]["port"]}
        message = utils.Peer2Server("Register", sock.getsockname()[0], "%s" % str(data))
        print 'sending "%s"' % message.formatted()
        sock.sendall(message.formatted())

        print "waiting for response"
        data = sock.recv(1024)
        message = utils.Peer2Server(data)
        data = message.data
        print "Received %s" % data
    except socket.error as err:
        print "Communication to server failed with error %s" % err

    try:
        # Leave
        print "\nLeaving"
        message = utils.Peer2Server("Leave", sock.getsockname()[0], "%s" % data)
        print 'sending "%s"' % message.formatted()
        sock.sendall(message.formatted())

        print "waiting for response"
        data = sock.recv(1024)
        print "received response"
        print data
    except socket.error as err:
        print "Communication to server failed with error %s" % err
    #
    # finally:
    #     print >> sys.stderr, 'closing socket'
    #     sock.close()


if __name__ == "__main__": main()