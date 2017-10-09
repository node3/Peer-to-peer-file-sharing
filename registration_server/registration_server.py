class PeerRecord:
    cookie_count = 0
    ttl_decrement_value = 5

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.cookie = PeerRecord.cookie_count
        PeerRecord.cookie_count += 1
        self.active = True
        self.ttl = 7200
        self.port = port
        self.reg_count = 1
        self.last_reg = None

    def initialize_ttl(self):
        self.ttl = 7200

    def mark_inactive(self):
        self.active = False

    def decrement_ttl(self):
        if self.ttl > 0:
            self.ttl = self.ttl - PeerRecord.ttl_decrement_value
            if self.ttl <= 0:
                self.ttl = 0
                self.mark_inactive()

    def update_reg_count(self):
        self.reg_count += 1

    def update_last_reg(self, new_reg_time):
        self.last_reg = new_reg_time


class Peers:
    def __init__(self, peer_record):
        self.peer_record = peer_record
        self.nxt = None

    def decrement_all_ttl(self):
        self.peer_record.decrement_ttl()
        if self.nxt:
            self.nxt.decrement_all_ttl()

