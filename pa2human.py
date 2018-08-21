#!/usr/bin/env python3
import argparse
import json
import logging
import sys

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor


_LOGGER = logging.getLogger(__name__)


class Translator(LineReceiver):
    delimiter = b'\n'
    def lineReceived(self, line):
        _LOGGER.debug("Got line [%s]", line)
        try:
            json.loads(line.decode())
            self.sendLine('{"intent": "hello"}'.encode())
        except json.JSONDecodeError:
            self.transport.loseConnection()


class TranslatorFactory(Factory):
    def buildProtocol(self, _):
        return Translator()


def main(args):
    reactor.listenUNIX(args.socket, TranslatorFactory())
    reactor.run()


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    parser = argparse.ArgumentParser(description="pa2human")
    parser.add_argument("--socket", help="Socket name", required=True)
    args = parser.parse_args()

    main(args)
