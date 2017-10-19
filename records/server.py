# This file contains the records that a registration server maintains about the peers


# PeerRecord holds all the attributes associated with a peer on server
class PeerRecord:
    cookie_count = 1

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.cookie = PeerRecord.cookie_count
        self.active = True
        self.ttl = 7200
        self.port = port
        self.reg_count = 1
        self.last_reg = None
        PeerRecord.cookie_count += 1

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

    def show_swarm(self):
        node = self
        table = "\n%-25s %-6s %-6s %-6s %-5s %-18s %-20s" % ("Hostname", "Port", "Cookie", "Active",
                                                             "TTL", "RegistrationCount", "LastRegistered")
        if node:
            while node:
                table += "\n%-25s %-6s %-6s %-6s %-5s %-18s %-20s" % (node.peer.hostname, node.peer.port,
                                                                      str(node.peer.cookie), str(node.peer.active),
                                                                      node.peer.ttl, node.peer.reg_count,
                                                                      node.peer.last_reg)
                node = node.nxt
        else:
            table += "\n%-25s %-6s %-6s %-6s %-5s %-18s %-20s" % ("None", "None", "None", "None",
                                                                  "None", "None", "None")
        return table


def display_swarm_table(head):
    message = "\nThe server is aware of the following : \n"
    breaker = "\n" + "-"*100
    if head:
        swarm_table = head.show_swarm()
    else:
        swarm_table = "\nNo peers registered on this server."
    return breaker + message + swarm_table + breaker
