peer2server_msg_types = ("Register", "Leave", "PQuery", "KeepAlive")


class Peer2Server:
    count = 0

    def __init__(self, command, ip, data):
        if command not in peer2server_msg_types:
            raise "Command %s not in allowed message types" % command
        self.command = command
        self.ip = ip
        self.data = data
        Peer2Server.count += 1

    def formatted(self):
        return "%s %s P2P-DI/1.0\n%s" % (self.command, self.ip, self.data)



