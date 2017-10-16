from message import *

ob1 = P2PRequest("Register", "test data")
en = ob1.encode()
print "ob 1 encode\n%s" % en
ob2 = P2PRequest.decode(en)
print "\n\n\n\n****\nob 1 decode\n%s" % ob2.current_state()
# ob2 = P2PResponse("200", "test data")
# print "ob 1 %s" % ob2.display()