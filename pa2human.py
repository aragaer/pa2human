#!/usr/bin/env python3

from rivescript.rivescript import RiveScript
import sys

if __name__ == '__main__':
    rs = RiveScript(utf8=True)
    rs.load_file("translate.rive")
    rs.load_file("cron.rive")
    rs.sort_replies()
    print(rs.reply("pa", " ".join(sys.argv[1:])))
