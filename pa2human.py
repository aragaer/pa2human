#!/usr/bin/env python3
import argparse
import json
import logging
import sys

from rivescript.rivescript import RiveScript
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver


_LOGGER = logging.getLogger(__name__)


class TranslatorProtocol(LineReceiver):
    def __init__(self, bots):
        self._bots = bots

    delimiter = b'\n'
    def lineReceived(self, line):
        _LOGGER.debug("Got line [%s]", line)
        try:
            request = json.loads(line.decode())
        except json.JSONDecodeError:
            self.transport.loseConnection()
            return
        if 'text' in request:
            rs = self._bots['human2pa']
            result = {"intent": rs.reply('human', request['text'])}
        elif 'intent' in request:
            rs = self._bots['pa2human']
            result = {"text": rs.reply('pa', request['intent'])}
        else:
            result = {"error": "Either 'intent' or 'text' required"}
        self.sendLine(json.dumps(result).encode())


class TranslatorProtocolFactory(Factory):
    def __init__(self, bots):
        self._bots = bots

    def buildProtocol(self, _):
        return TranslatorProtocol(self._bots)


def main(args):
    bots = {}
    for bot_name in ('human2pa', 'pa2human'):
        bot = RiveScript(utf8=True)
        bot.load_directory(bot_name)
        bot.sort_replies()
        bots[bot_name] = bot

    reactor.listenUNIX(args.socket,
                       TranslatorProtocolFactory(bots))
    reactor.run()


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    parser = argparse.ArgumentParser(description="pa2human")
    parser.add_argument("--socket", help="Socket name", required=True)
    args = parser.parse_args()

    main(args)
