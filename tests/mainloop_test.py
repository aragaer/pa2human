import logging
import os
import shutil
import signal
import socket
import sys
import time
import unittest

from multiprocessing import Process
from runner.channel import EndpointClosedException, LineChannel, SocketChannel
from tempfile import mkdtemp

from pa2human import mainloop
from utils import timeout, TimeoutException


def _cleanup(proc):
    proc.terminate()
    proc.join()


def _read_answer(channel, t=0.1):
    try:
        with timeout(t):
            while True:
                line = channel.read()
                if line:
                    return line
    except TimeoutException:
        return None

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class MainloopTest(unittest.TestCase):

    def setUp(self):
        dirname = mkdtemp()
        self.addCleanup(shutil.rmtree, dirname)
        self._socket_path = os.path.join(dirname, "tr")

        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(self._socket_path)
        server.listen()

        self._server_proc = Process(target=mainloop, args=[server])
        self._server_proc.start()

        self.addCleanup(_cleanup, self._server_proc)

    def _connect_client(self):
        local = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.addCleanup(local.close)
        local.connect(self._socket_path)

        return LineChannel(SocketChannel(local))

    def test_one_client(self):
        chan = self._connect_client()
        chan.write('{"text": "Привет", "from": "user"}'.encode()+b'\n')
        self.assertIsNotNone(_read_answer(chan))

    def test_silent_client(self):
        chan = self._connect_client()
        self.assertIsNone(_read_answer(chan), "I didn't write anything")

    def test_incomplete_write(self):
        chan = self._connect_client()

        chan.write(b'{"text":')

        self.assertIsNone(_read_answer(chan), "I didn't write the message yet")

    def test_write_garbage(self):
        chan = self._connect_client()

        chan.write(b'hi\n')
        with self.assertRaises(EndpointClosedException):
            _read_answer(chan)

    def test_write_partial(self):
        chan = self._connect_client()

        chan.write('{"text":"Привет"'.encode())
        chan.write(b',"from":"user"}\n')

        self.assertIsNotNone(_read_answer(chan))

    def test_write_mixed(self):
        chan1 = self._connect_client()
        chan2 = self._connect_client()

        chan1.write('{"text":"Привет"'.encode())
        chan2.write(b',"from":"user"}\n')

        self.assertIsNone(_read_answer(chan1))
        with self.assertRaises(EndpointClosedException):
            _read_answer(chan2)

    def test_write_read_write_incomplete(self):
        chan = self._connect_client()
        chan.write('{"text":"Привет", "from": "user"}\n'.encode())
        _read_answer(chan)

        chan.write(b'{')

        self.assertIsNone(_read_answer(chan))

    def test_write_extra(self):
        chan = self._connect_client()

        chan.write('{"text":"Привет", "from": "user"}\n{'.encode())

        self.assertIsNotNone(_read_answer(chan))

    def test_write_multiple(self):
        chan = self._connect_client()

        chan.write('{"text":"Привет", "from": "user"}\n'.encode() * 3)

        self.assertIsNotNone(_read_answer(chan))
        self.assertIsNotNone(_read_answer(chan))
        self.assertIsNotNone(_read_answer(chan))
