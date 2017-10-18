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
        if self.rfc.number == rfc_number:
            if self.rfc.is_active():
                return self.rfc
            else:
                return None
        elif self.nxt:
            self.nxt.find(rfc_number)
        else:
            return None

    # Find a node in the linked list and update it if it exists
    def find_and_update(self, rfc):
        if self.rfc.number == rfc.number:
            self.rfc.title = rfc.title
            self.rfc.hostname = rfc.hostname
            self.rfc.ttl = 7200
            return True
        elif self.nxt:
            self.nxt.find_and_update(rfc)
        else:
            return False

    # Prepend a node
    def insert(self, node):
        if node:
            self.nxt = node
        return self

    # Merge a list with another list
    def merge(self, head):
        ptr = head
        new_list = None
        while ptr:
            if not self.find_and_update(ptr.rfc):
                node = Node(RFC(ptr.rfc.hostname, ptr.rfc.number, ptr.rfc.title))
                if not new_list:
                    new_list = node
                else:
                    node.nxt = new_list
                    new_list = node
            ptr = ptr.nxt

        if new_list:
            ptr = new_list
            while ptr:
                if not ptr.nxt:
                    ptr.nxt = head
                    break
                ptr = ptr.nxt

        return new_list


# This function returns the hashed representation of the linked list
def encode_list(head):
    node = head
    hash_list = []
    while node:
        hash_list.append(node.hash())
        node = node.nxt
    return hash_list


# This function returns a linked list for a given hashed representation
def decode_list(hostname, hash_list):
    head = None
    for rfc in hash_list["rfcs"]:
        node = Node(RFC(hostname, rfc["number"], rfc["title"]))
        head = node.insert(head)
    return head
