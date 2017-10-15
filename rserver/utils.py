import datetime
import commons


def req_print(message):
    if not commons.DEBUG:
        print "\n%s : received %s request : %s" % (datetime.datetime.now(),
                                               message.command,
                                               message.data)


def resp_print(message):
    if not commons.DEBUG:
        print "\n%s : sending %s response: %s" % (datetime.datetime.now(),
                                              message.command,
                                              message.data)

