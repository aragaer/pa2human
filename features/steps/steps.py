import logging
import os
import shutil
import socket
import stat
import time

from tempfile import mkdtemp

from behave import *
from nose.tools import eq_, ok_

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


@when(u'I start pa2human with that path')
def step_impl(context):
    context.runner.add("pa2human", command="./pa2human.py")
    context.runner.start("pa2human", with_args=['--socket', context.socket_path])
    context.add_cleanup(_terminate, context, "pa2human")


@when('I wait for socket to appear')
@then(u'the socket appears')
def step_impl(context):
    for _ in range(100):
        if os.path.exists(context.socket_path):
            break
        time.sleep(0.01)
    else:
        ok_(False, "{} not found".format(context.socket_path))
    ok_(stat.S_ISSOCK(os.stat(context.socket_path).st_mode),
        "{} is not a socket".format(context.socket_path))


@then(u'the socket accepts connections')
@then(u'the socket accepts a connection')
@then(u'the socket accepts another connection')
def step_impl(context):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(context.socket_path)


@when(u'I stop pa2human')
def step_impl(context):
    context.runner.terminate("pa2human")


@then(u'the socket doesn\'t exist')
def step_impl(context):
    for _ in range(100):
        if not os.path.exists(context.socket_path):
            return
        time.sleep(0.01)
    ok_(False, "{} still exists".format(context.socket_path))
