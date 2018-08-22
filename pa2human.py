#!/usr/bin/env python3
import argparse
import json
import logging
import sys

from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver


_LOGGER = logging.getLogger(__name__)


class TranslatorProtocol(LineReceiver):
    delimiter = b'\n'
    def lineReceived(self, line):
        _LOGGER.debug("Got line [%s]", line)
        try:
            request = json.loads(line.decode())
        except json.JSONDecodeError:
            self.transport.loseConnection()
            return
        if 'text' in request:
            result = {"intent": "hello"}
        elif 'intent' in request:
            result = {"text": "Ой, приветик!"}
        else:
            result = {"error": "Either 'intent' or 'text' required"}
        self.sendLine(json.dumps(result).encode())


class TranslatorProtocolFactory(Factory):
    def buildProtocol(self, _):
        return TranslatorProtocol()


def main(args):
    reactor.listenUNIX(args.socket, TranslatorProtocolFactory())
    reactor.run()


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    parser = argparse.ArgumentParser(description="pa2human")
    parser.add_argument("--socket", help="Socket name", required=True)
    args = parser.parse_args()

    main(args)
