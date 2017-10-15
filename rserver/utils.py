import datetime


def req_print(message):
    print "\n%s : received %s request : %s" % (datetime.datetime.now(),
                                               message.command,
                                               message.data)


def resp_print(message):
    print "\n%s : sending %s response: %s" % (datetime.datetime.now(),
                                              message.command,
                                              message.data)

