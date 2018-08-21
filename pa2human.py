#!/usr/bin/env python3
import argparse
import atexit
import os
import signal
import socket
import sys


def mainloop(sock):
    while True:
        sock.accept()


def main(args):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    atexit.register(s.close)
    s.bind(args.socket)
    atexit.register(os.unlink, args.socket)
    s.listen()
    atexit.register(s.shutdown, socket.SHUT_RDWR)
    mainloop(s)


def _exit(signum, flame):
    sys.exit()


if __name__ == '__main__':
    # needed for atexit to work properly
    signal.signal(signal.SIGTERM, _exit)

    parser = argparse.ArgumentParser(description="pa2human")
    parser.add_argument("--socket", help="Socket name", required=True)
    args = parser.parse_args()

    main(args)
