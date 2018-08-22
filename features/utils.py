import signal

from contextlib import contextmanager


TimeoutException = type("TimeoutException", (Exception,), {})


def _timeout(signum, flame):
    raise TimeoutException()


@contextmanager
def timeout(timeout):
    signal.signal(signal.SIGALRM, _timeout)
    signal.setitimer(signal.ITIMER_REAL, timeout)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
