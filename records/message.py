import platform
import pickle

VALID_COMMANDS = ("Register", "Leave", "PQuery", "KeepAlive", "RFCQuery", "GetRFC")
VALID_STATUS = {
                    "100": "Resource Not Found",
                    "200": "Resource Found",
                    "201": "Resource Updated",
                    "300": "Bad Request"
                }


class P2PMessage:
    def __init__(self):
        self.os = P2PMessage.get_os()
        self.hostname = P2PMessage.get_hostname()
        self.version = P2PMessage.get_version()

    def encode(self):
        try:
            return pickle.dumps(self, -1)
        except pickle.PicklingError:
            raise Exception("Could not encode the object")

    @staticmethod
    def decode(encoded_msg):
        try:
            return pickle.loads(encoded_msg)
        except pickle.UnpicklingError:
            raise Exception("Could not decode the object")

    def display(self):
        # Implement this in the child classes
        return

    @staticmethod
    def get_os():
        return "_".join([platform.system(), platform.release()])

    @staticmethod
    def get_hostname():
        return platform.node()

    @staticmethod
    def get_version():
        return 'P2P-DI/1.0'


# P2RSRequest is used create request messages during client and server communication
class P2PRequest(P2PMessage):
    def __init__(self, command, data):
        P2PMessage.__init__(self)
        self.command = command
        self.data = data
        self.validate()

    def display(self):
        return "%s %s\n%s %s\n%s" % (self.command, self.version, self.hostname, self.os, str(self.data))

    def validate(self):
        if self.command not in VALID_COMMANDS:
            raise Exception("%s not a valid command. Cannot create the P2PRequest object." % self.command)


# P2RSRequest is used create request messages during client and server communication
class P2PResponse(P2PMessage):
    def __init__(self, status, data):
        P2PMessage.__init__(self)
        self.status = status
        self.data = data
        self.validate()

    def display(self):
        return "%s %s\n%s %s\n%s" % (self.status, self.version, self.hostname, self.os, str(self.data))

    # call it after unpickling
    def validate(self):
        if self.status not in VALID_STATUS.keys():
            raise Exception("%s not a valid status. Cannot create the P2PResponse object." % self.status)

    def status_message(self):
        return VALID_STATUS[self.status]

