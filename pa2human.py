#!/usr/bin/env python3
import argparse
import atexit
import json
import logging
import os
import signal
import socket
import sys

from channels.poller import Poller
from rivescript.rivescript import RiveScript


_LOGGER = logging.getLogger(__name__)


try:
    _JSON_EXCEPTION = json.JSONDecodeError
except AttributeError:
    _JSON_EXCEPTION = ValueError


class TranslatorServer:
    def __init__(self, socket, bots):
        self._bots = bots
        self._poller = Poller()
        self._socket = socket
        self._poller.add_server(socket)

    def _translate(self, message):
        if 'text' in message:
            rs = self._bots['human2pa']
            return {"intent": rs.reply('pa', message['text'])}
        elif 'intent' in message:
            rs = self._bots['pa2human']
            return {"text": rs.reply('human', message['intent'])}
        return {"error": "Either 'intent' or 'text' required"}

    def work(self, timeout=None):
        for data, channel in self._poller.poll(timeout):
            if channel == self._socket:
                _LOGGER.debug("Client connected")
            else:
                _LOGGER.debug("Got line [%s]", data.decode())
                try:
                    request = json.loads(data.decode())
                except _JSON_EXCEPTION:
                    self._poller.unregister(channel)
                    channel.close()
                    continue
                result = self._translate(request)
                channel.write(json.dumps(result).encode(), b'\n')

    def run(self):
        while True:
            self.work()


def term(*_):
    exit(0)


def main(args):
    signal.signal(signal.SIGTERM, term)
    bots = {}
    for bot_name in ('human2pa', 'pa2human'):
        bot = RiveScript(utf8=True)
        bot.load_directory(bot_name)
        bot.sort_replies()
        bots[bot_name] = bot

    if ':' in args.socket:
        host, port = args.socket.split(':')
        serv = socket.socket(socket.AF_INET)
        serv.bind((host, int(port)))
        addr = serv.getsockname()
        print("Pa2human listening on", "{}:{}".format(*addr))
        sys.stdout.flush()
    else:
        serv = socket.socket(socket.AF_UNIX)
        serv.bind(args.socket)
        atexit.register(os.unlink, args.socket)
    serv.listen(0)

    server = TranslatorServer(serv, bots)
    server.run()


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    parser = argparse.ArgumentParser(description="pa2human")
    parser.add_argument("--socket", help="Socket name", required=True)
    args = parser.parse_args()

    main(args)
