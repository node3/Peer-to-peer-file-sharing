import datetime
from os import system
from sys import exit
import commons
import os


def continue_or_exit(message):
    print message
    try:
        print "\nPress any key to go back to the menu. Press Control+C to exit."
        raw_input()
    except KeyboardInterrupt:
        print "Client shutting down"
        exit(0)
    system('clear')


def get_rfc_dir():
    rfc_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rfc")
    if not os.path.exists(rfc_dir):
        os.makedirs(rfc_dir)
    return rfc_dir
