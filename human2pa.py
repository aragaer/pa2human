#!/usr/bin/env python3
import sys
import translate


if __name__ == '__main__':
    translate.main(sys.argv[1],
                   'human2pa',
                   " ".join(sys.argv[2:]),
                   '/tmp/tr_socket')
