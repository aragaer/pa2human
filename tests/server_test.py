import socket
import json
import unittest

from rivescript.rivescript import RiveScript

from pa2human import TranslatorServer
from utils import timeout


class ServerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.bot = RiveScript(utf8=True)
        cls.bot.load_directory("echo")
        cls.bot.sort_replies()

    def setUp(self):
        serv = socket.socket()
        serv.bind(('127.0.0.1', 0))
        serv.listen()
        self.addCleanup(serv.close)
        self.ts = TranslatorServer(socket=serv,
                                   bots={"pa2human": self.bot, "human2pa": self.bot})
        self.client = socket.create_connection(serv.getsockname())
        self.addCleanup(self.client.close)
        self.ts.work(0.1) # accept the client

    def _expect(self, data):
        self.ts.work(0.1)
        with timeout(0.1):
            result = self.client.recv(1024)
        if isinstance(data, dict):
            self.assertEquals(json.loads(result.decode()),
                              data)
        else:
            self.assertEquals(result, data)

    def test_client_sends_message_server_translates_to_intent(self):
        self.client.send(json.dumps({"text": "Привет",
                                     "from": "user"}).encode()+b'\n')

        self._expect({"intent": "echo привет"})

    def test_client_sends_garbage_server_drops_connection(self):
        self.client.send(b"x\n")

        self._expect(b'')

    def test_client_sends_intent_server_translates_to_text(self):
        self.client.send(json.dumps({"intent": "hello",
                                     "user": "user"}).encode()+b'\n')

        self._expect({"text": "echo hello"})

    def test_client_sends_incorrect_json_server_returns_error(self):
        self.client.send(b'{"a": "b"}\n')

        self._expect({"error": "Either 'intent' or 'text' required"})

    def test_client_disconnects(self):
        self.client.close()

        self.ts.work(0.1)
