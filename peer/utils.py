import datetime
from os import system
from sys import exit
import commons


def req_print(message):
    if not commons.DEBUG:
        print "\n%s : sending %s request : %s" % (datetime.datetime.now(),
                                                  message.command,
                                                  message.data)


def resp_print(message):
    if not commons.DEBUG:
        print "\n%s : received %s response: %s" % (datetime.datetime.now(),
                                                   message.command,
                                                   message.data)


def continue_or_exit(message):
    print message
    try:
        print "\nPress any key to go back to the menu. Press Control+C to exit."
        raw_input()
    except KeyboardInterrupt:
        print "Client shutting down"
        exit(0)
    system('clear')

