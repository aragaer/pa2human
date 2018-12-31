import io
import signal
import sys

from contextlib import contextmanager


def _timeout(signum, flame):
    raise Exception("timeout")


@contextmanager
def timeout(timeout):
    signal.signal(signal.SIGALRM, _timeout)
    signal.setitimer(signal.ITIMER_REAL, timeout)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


@contextmanager
def capture():
    oldout,olderr = sys.stdout, sys.stderr
    try:
        out=[io.StringIO(), io.StringIO()]
        sys.stdout,sys.stderr = out
        yield out
    finally:
        sys.stdout,sys.stderr = oldout, olderr
        out[0] = out[0].getvalue()
        out[1] = out[1].getvalue()
