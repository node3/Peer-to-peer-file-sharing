from rfc import display_rfc_list


# PeerInfo is used by a peer to record its "state of awareness"
class PeerInfo:
    def __init__(self):
        self.cookie = None
        self.rfc_index_head = None
        self.peers = []

    def add_new_peers(self, peers):
        # This logic appends any new peers
        # peers_to_be_added = []
        # for peer in peers:
        #     if peer not in self.peers:
        #         peers_to_be_added.append(peer)
        # self.peers.extend(peers_to_be_added)

        # This logic only keeps the new peers and discards any previous ones
        self.peers = self.peers[:0]
        self.peers.extend(peers)

    def display_peer_state(self):
        message = "\n\tCurrently the peer is aware of the following :" \
                  "\n\tPeer registration id/cookie : %s" \
                  "\n\tList of Known peers in the swarm: %s" \
                  "\n\n\tLocal rfc index contains following information: " % (self.cookie, self.peers)
        message += display_rfc_list(self.rfc_index_head)
        return message
