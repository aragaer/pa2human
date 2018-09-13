import json

from rivescript.rivescript import RiveScript
from twisted.internet.protocol import Factory
from twisted.test.proto_helpers import StringTransportWithDisconnection
from twisted.trial.unittest import TestCase

from pa2human import TranslatorProtocol


class MockFactory(Factory):
    pass


class TestSomeProtocol(TestCase):
    bot = None

    @classmethod
    def setUpClass(cls):
        cls.bot = RiveScript(utf8=True)
        cls.bot.load_directory("echo")
        cls.bot.sort_replies()

    def setUp(self):
        self.sp = TranslatorProtocol({"pa2human": self.bot, "human2pa": self.bot})
        self.transport = StringTransportWithDisconnection()
        self.sp.makeConnection(self.transport)
        self.transport.protocol = self.sp
        self.sp.factory = MockFactory()

    def test_client_sends_message_server_translates_to_intent(self):
        self.sp.dataReceived(json.dumps({"text": "Привет",
                                         "from": "user"}).encode()+b'\n')

        self.assertEquals(json.loads(self.transport.value().decode()),
                          {"intent": "echo привет"})

    def test_client_sends_garbage_server_drops_connection(self):
        self.sp.dataReceived(b"x\n")
        self.assertFalse(self.transport.connected)

    def test_client_sends_intent_server_translates_to_text(self):
        self.sp.dataReceived(json.dumps({"intent": "hello",
                                         "user": "user"}).encode()+b'\n')

        self.assertEquals(json.loads(self.transport.value().decode()),
                          {"text": "echo hello"})

    def test_client_sends_incorrect_json_server_returns_error(self):
        self.sp.dataReceived(b'{"a": "b"}\n')

        self.assertEquals(json.loads(self.transport.value().decode()),
                          {"error": "Either 'intent' or 'text' required"})
