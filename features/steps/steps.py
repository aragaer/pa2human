import logging
import json
import os
import shutil
import socket
import stat
import time

from tempfile import mkdtemp

from behave import *
from nose.tools import eq_, ok_

from utils import timeout


_LOGGER = logging.getLogger(__name__)


def _terminate(context, alias):
    try:
        context.runner.terminate(alias)
    except KeyError:
        _LOGGER.debug("%s was not started", alias)


@given(u'I have a socket path to use')
def step_impl(context):
    dirname = mkdtemp()
    context.add_cleanup(shutil.rmtree, dirname)
    context.socket_path = os.path.join(dirname, "tr")


@step(u'I start pa2human with that path')
def step_impl(context):
    context.runner.add("pa2human", command="./pa2human.py")
    context.runner.start("pa2human", with_args=['--socket', context.socket_path])
    context.add_cleanup(_terminate, context, "pa2human")


@given('the socket is created')
@when('I wait for socket to appear')
@then('the socket appears')
def step_impl(context):
    for _ in range(100):
        if os.path.exists(context.socket_path):
            break
        time.sleep(0.01)
    else:
        ok_(False, "{} not found".format(context.socket_path))
    ok_(stat.S_ISSOCK(os.stat(context.socket_path).st_mode),
        "{} is not a socket".format(context.socket_path))


def _connect(context):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(context.socket_path)
    return s


@then('the socket accepts connections')
@then('the socket accepts a connection')
@then('the socket accepts another connection')
def step_impl(context):
    _connect(context)


@when('I stop pa2human')
def step_impl(context):
    context.runner.terminate("pa2human")


@then('the socket doesn\'t exist')
def step_impl(context):
    for _ in range(100):
        if not os.path.exists(context.socket_path):
            return
        time.sleep(0.01)
    ok_(False, "{} still exists".format(context.socket_path))


@given('the service is started')
def step_impl(context):
    context.execute_steps("Given I have a socket path to use")
    context.runner.add("pa2human", command="./pa2human.py",
                       type="socket", buffering="line")
    context.runner.start("pa2human",
                         with_args=['--socket', context.socket_path],
                         socket=context.socket_path)
    context.add_cleanup(_terminate, context, "pa2human")


@given(u'brain is connected')
def step_impl(context):
    context.socket = context.runner.get_channel("pa2human")

@when(u'brain asks to translate "{intent}" to {recipient}')
def step_impl(context, intent, recipient):
    context.socket.write(json.dumps({"intent": intent, "to": recipient}).encode()+b'\n')

@when(u'brain asks to translate "{text}" from {source}')
def step_impl(context, text, source):
    context.socket.write(json.dumps({"text": text, "from": source}).encode()+b'\n')


@then(u'the result is {field} "{value}"')
def step_impl(context, field, value):
    with timeout(1):
        while True:
            line = context.socket.read()
            if line:
                break
    message = json.loads(line.decode())
    expected = {field: value}
    eq_(message, expected,
        "Expected translation '{}', got '{}'".format(expected, message))
