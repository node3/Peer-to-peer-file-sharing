peer2server_msg_types = ("Register", "Leave", "PQuery", "KeepAlive")


# Peer2Server is used create messages during client and server communication
class Peer2Server:
    count = 0

    def __init__(self, command, ip=None, data=None, version='P2P-DI/1.0'):
        # This is to be used to create a message for encoding
        if ip and data:
            if command not in peer2server_msg_types:
                raise "Command %s not in allowed message types" % command
            self.command = command
            self.ip = ip
            if isinstance(data, dict):
                self.data = data
            else:
                self.data = eval(data)
            self.version = version
            Peer2Server.count += 1

        # This is to be used for decoding a message received as string
        elif not (data and ip):
            fields = command.split("\n\t")
            try:
                self.command = fields[1]
                self.ip = fields[2]
                self.version = fields[3]
                self.data = eval(fields[4])
            except IndexError:
                raise Exception("Peer2Server could not decode the message %s" % command)
        else:
            raise Exception("Illegal instantiation of Peer2Server. Check parameters.")

    def encode(self):
        return "\n\t%s\n\t%s\n\t%s\n\t%s" % (self.command, self.ip, self.version, self.data)
