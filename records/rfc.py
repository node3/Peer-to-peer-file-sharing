# RFC class contains the information about an RFC
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
        return "%-15s %-5s %-40s %-5s" % (self.hostname, self.number, self.title, self.ttl)


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
                print "RFC found and active"
                return ptr.rfc
            ptr = ptr.nxt
        return None

    # Find a node in the linked list and update it if it exists
    def find_and_update(self, rfc):
        ptr = self
        while ptr:
            if ptr.rfc.number == rfc.number:
                self.rfc.title = rfc.title
                self.rfc.hostname = rfc.hostname
                self.rfc.ttl = 7200
                return True
            ptr = ptr.nxt
        return False

    # Prepend a node
    def insert(self, node):
        if node:
            self.nxt = node
        return self


# Merge list b into list a and return the updated a
def merge(a, b):
    if a:
        node = b
        while node:
            if not a.find_and_update(node.rfc):
                a = a.insert(node.rfc)
            node = node.nxt
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
        node = Node(RFC(hostname, rfc["number"], rfc["title"]))
        head = node.insert(head)
    return head


def display_rfc_list(head):
    node = head
    table = "\n%-15s %-5s %-40s %-5s" % ("Hostname", "RFC#", "Title", "TTL")
    if node:
        while node:
            table += "\n%-15s %-5s %-40s %-5s" % (node.rfc.hostname, node.rfc.number, node.rfc.title, node.rfc.ttl)
            node = node.nxt
    else:
        table += "\n%-15s %-5s %-40s %-5s" % ("None", "None", "None", "None")
    return table
