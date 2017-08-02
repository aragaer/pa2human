#!/usr/bin/env python3
import sys
import translate


if __name__ == '__main__':
    translate.main('pa',
                   'pa2human',
                   " ".join(sys.argv[1:]),
                   '/tmp/tr_socket')
