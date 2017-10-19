# RFC class contains the information about an RFC.
# This is maintained by the peer server and initially picked up from metadata.json


class RFC:
    def __init__(self, hostname, number, title):
        self.number = number
        self.title = title
        self.hostname = hostname
        self.ttl = 7200

    def decrement_ttl(self, decrement_value):
        if self.hostname != "localhost" and self.ttl > 0:
            self.ttl = self.ttl - decrement_value
            if self.ttl <= 0:
                self.ttl = 0

    def is_active(self):
        if self.ttl == 0:
            return False
        else:
            return True

    def display(self):
        return "%-25s %-5s %-5s %-40s" % (self.hostname, self.ttl, self.number, self.title)


# Node class represents the node in the linked list. Instantiate this class to create nodes
class Node:
    def __init__(self, rfc):
        self.rfc = rfc
        self.nxt = None

    def hash(self):
        return {"number": self.rfc.number,
                "title": self.rfc.title
                }

    # Find a node in the linked list by rfc number and return the rfc object if found
    def find(self, rfc_number):
        ptr = self
        while ptr:
            if ptr.rfc.number == rfc_number and ptr.rfc.is_active():
                return ptr.rfc
            ptr = ptr.nxt
        return None

    # Find a node in the linked list and update it if it exists
    def find_and_update(self, rfc):
        ptr = self
        while ptr:
            if ptr.rfc.number == rfc.number:
                ptr.rfc.title = rfc.title
                ptr.rfc.hostname = rfc.hostname
                ptr.rfc.ttl = 7200
                return True
            ptr = ptr.nxt
        return False

    # Insert an rfc at the end of the list
    def insert(self, rfc):
        node = Node(rfc)
        ptr = self
        while ptr:
            if not ptr.nxt:
                ptr.nxt = node
                break
            ptr = ptr.nxt


# Merge list b into list a and return the updated a
def merge(a, b):
    if a:
        ptr = b
        while ptr:
            rfc = a.find(ptr.rfc.number)
            if not rfc:
                a.insert(ptr.rfc)
            elif rfc.hostname != ptr.rfc.hostname:
                if rfc.hostname != "localhost":
                    a.insert(ptr.rfc)
            ptr = ptr.nxt
        return a
    else:
        return b


# This function returns the hashed representation of the linked list
def encode_rfc_list(head):
    node = head
    hash_list = []
    while node:
        hash_list.append(node.hash())
        node = node.nxt
    return hash_list


# This function returns a linked list for a given hashed representation
def decode_rfc_list(hostname, hash_list):
    head = None
    for rfc in hash_list["rfcs"]:
        rfc = RFC(hostname, rfc["number"], rfc["title"])
        if head:
            head.insert(rfc)
        else:
            head = Node(rfc)
    return head


def display_rfc_list(head):
    node = head
    table = "\n\t%-25s %-5s %-5s %-40s" % ("Hostname", "TTL", "RFC#", "Title")
    if node:
        while node:
            table += "\n\t%-25s %-5s %-5s %-40s" % (node.rfc.hostname, node.rfc.ttl, node.rfc.number, node.rfc.title)
            node = node.nxt
    else:
        table += "\n\t%-25s %-5s %-5s %-40s" % ("None", "None", "None", "None")
    return table
