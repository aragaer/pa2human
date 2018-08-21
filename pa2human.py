#!/usr/bin/env python3
import argparse
import atexit
import json
import logging
import os
import signal
import socket
import sys

from select import select

from runner.channel import LineChannel, SocketChannel


_LOGGER = logging.getLogger(__name__)


def mainloop(server):
    sockets = [server]
    channels = {}
    while True:
        r, w, e = select(sockets, [], sockets)
        for sock in e:
            if sock == server:
                return
            else:
                channels[sock].close()
                sockets.remove(sock)
                del channels[sock]

        for sock in r:
            if sock == server:
                client, _ = server.accept()
                sockets.append(client)
                channels[client] = LineChannel(SocketChannel(client))
                _LOGGER.debug("Got client")
            elif sock in channels:
                while True:
                    line = channels[sock].read()
                    if not line:
                        break
                    try:
                        json.loads(line.decode())
                        channels[sock].write(b'\n')
                    except json.JSONDecodeError:
                        _LOGGER.warn("Decode error")
                        channels[sock].close()
                        sockets.remove(sock)
                        del channels[sock]
                        break


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
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    parser = argparse.ArgumentParser(description="pa2human")
    parser.add_argument("--socket", help="Socket name", required=True)
    args = parser.parse_args()

    main(args)
