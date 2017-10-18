from rfc import display_rfc_list


# PeerRecord holds all the attributes associated with a peer
class PeerRecord:
    cookie_count = 1

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
        self.active = True

    def is_active(self):
        return self.active

    def mark_inactive(self):
        self.active = False

    def decrement_ttl(self, decrement_value):
        if self.ttl > 0:
            self.ttl = self.ttl - decrement_value
            if self.ttl <= 0:
                self.ttl = 0
                self.mark_inactive()

    def update_reg_count(self):
        self.reg_count += 1

    def update_last_reg(self, new_reg_time):
        self.last_reg = new_reg_time


# Peers are the nodes of the linked list. Create the linked list by instantiating this class.
class Peers:
    def __init__(self, peer):
        self.peer = peer
        self.nxt = None


# PeerInfo should be used to store the peer's current state
class PeerInfo:
    def __init__(self):
        self.cookie = None
        self.rfc_index_head = None
        self.peers = []

    def add_new_peers(self, peers):
        peers_to_be_added = []
        for peer in peers:
            if peer not in self.peers:
                peers_to_be_added.append(peer)
        self.peers.extend(peers_to_be_added)


def display_peer_state(peer_info):
    message = "\n\tCurrently the peer is aware of the following :" \
              "\n\tPeer registration id/cookie : %s" \
              "\n\tList of Known peers in the swarm: %s" \
              "\n\n\tLocal rfc index contains following information: " % (peer_info.cookie, peer_info.peers)
    message += display_rfc_list(peer_info.rfc_index_head)
    return message
