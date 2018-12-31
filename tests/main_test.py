import argparse
import socket
import unittest

from unittest.mock import patch

import pa2human

from utils import capture


class MainTest(unittest.TestCase):

    def setUp(self):
        self._parser = argparse.ArgumentParser()
        self._parser.add_argument("--socket", help="Socket name", required=True)
        patcher = patch('pa2human.TranslatorServer')
        self._server = patcher.start()
        self.addCleanup(patcher.stop)

    def test_unix_socket(self):
        args = self._parser.parse_args(["--socket", "foo"])

        pa2human.main(args)

        self.assertEqual(self._server.call_count, 1)
        sock = self._server.call_args[0][0]
        self.assertIsInstance(sock, socket.socket)
        self.assertEqual(sock.getsockname(), "foo")
        sock.close()

    def test_tcp_socket(self):
        # FIXME: using a hardcoded port
        try:
            socket.connect(('127.0.0.1', 18081))
            self.skip("Port 18081 is taken")
        except:
            pass
        args = self._parser.parse_args(["--socket", "0.0.0.0:18081"])

        with capture() as out:
            pa2human.main(args)

        self.assertEqual(self._server.call_count, 1)
        sock = self._server.call_args[0][0]
        self.assertIsInstance(sock, socket.socket)
        self.assertEqual(sock.getsockname(), ('0.0.0.0', 18081))

        self.assertEquals(out[0], "Pa2human listening on 0.0.0.0:18081\n")

    def test_tcp_dynamic_bind(self):
        args = self._parser.parse_args(["--socket", "0.0.0.0:0"])

        with capture() as out:
            pa2human.main(args)

        self.assertEqual(self._server.call_count, 1)
        sock = self._server.call_args[0][0]
        self.assertIsInstance(sock, socket.socket)
        host, port = sock.getsockname()

        self.assertEquals(out[0], "Pa2human listening on 0.0.0.0:{}\n".format(port))
