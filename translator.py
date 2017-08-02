#!/usr/bin/env python3

import argparse
import asyncio
import json
import logging
import os
import signal
import sys

from functools import partial

from rivescript.rivescript import RiveScript


class TranslatorServer(object):

    def __init__(self, path, loop, bots):
        self._path = path
        self._loop = loop
        self._bots = bots
        self._server = None
        self._writers = []

    async def start_server(self):
        if os.path.exists(self._path):
            os.unlink(self._path)
        self._server = await asyncio.start_unix_server(
            self.accept_client, path=self._path)

    def run_forever(self):
        self._loop.create_task(self.start_server())
        self._loop.run_forever()

    async def run_client(self, reader, writer):
        try:
            while True:
                sdata = await reader.readline()
                if not sdata:
                    break
                data = sdata.decode().strip()
                if not data:
                    continue
                event = json.loads(data)
                user = event.get('user', 'user')
                bot = event.get('bot', 'human2pa')
                rs = self._bots[bot]
                rs.set_uservar(user, "name", user)
                event['reply'] = rs.reply(user, event['text'])
                result = json.dumps(event, ensure_ascii=False)
                sresult = "{}\n".format(result).encode()
                writer.write(sresult)
        except asyncio.CancelledError:
            pass

    def accept_client(self, reader, writer):
        self._writers.append(writer)
        task = self._loop.create_task(self.run_client(reader, writer))
        task.add_done_callback(partial(self.close_writer, writer))

    def close_writer(self, writer, task):
        self._writers.remove(writer)
        writer.close()

    def stop(self):
        for writer in self._writers:
            writer.close()
        self._server.close()
        os.unlink(self._path)
        

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    parser = argparse.ArgumentParser(description="pa2human")
    parser.add_argument("--socket", default="/tmp/tr_socket", help="Socket name")
    args = parser.parse_args()
    
    loop = asyncio.get_event_loop()
    for signame in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(signame, loop.stop)

    bots = {}
    for bot_name in ('human2pa', 'pa2human'):
        bot = RiveScript(utf8=True)
        bot.load_directory(bot_name)
        bot.sort_replies()
        bots[bot_name] = bot

    server = TranslatorServer(args.socket, loop, bots)
    server.run_forever()

    server.stop()
