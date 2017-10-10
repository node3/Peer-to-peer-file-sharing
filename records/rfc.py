# RFC class contains the information about an RFC
class RFC:
    ttl_decrement_value = 5

    def __init__(self, number, title, hostname):
        self.number = number
        self.title = title
        self.hostname = hostname
        self.ttl = 7200

    def decrement_ttl(self):
        if self.ttl > 0:
            self.ttl = self.ttl - RFC.ttl_decrement_value
            if self.ttl <= 0:
                self.ttl = 0
                self.mark_inactive()


# RFCIndex class represents the node in the linked list. Instantiate this class to create nodes
class RFCIndex:
    def __init__(self, rfc):
        self.rfc = rfc
        self.nxt = None

    def decrement_all_ttl(self):
        self.peer_record.decrement_ttl()
        if self.nxt:
            self.nxt.decrement_all_ttl()