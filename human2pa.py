#!/usr/bin/env python3

from rivescript.rivescript import RiveScript
import sys

if __name__ == '__main__':
    rs = RiveScript(utf8=True)
    rs.load_file("parse.rive")
    user = sys.argv[1]
    phrase = " ".join(sys.argv[2:])
    rs.set_uservar(user, "name", user)
    rs.sort_replies()
    print(rs.reply(user, phrase))
