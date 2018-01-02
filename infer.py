#!/usr/bin/env python3

import argparse
import atexit
import os
import sys

import nmt
import tensorflow as tf

from nmt.nmt.nmt import main as nmt_main, add_arguments

from vocab import make_vocabs

def print_result(out):
    with open(out) as f:
        for l in f:
            print(l)


def main():
    base_dir = os.path.dirname(__file__)
    inp = os.path.join(base_dir, "input")
    out = os.path.join(base_dir, "output")
    atexit.register(print_result, out)

    with open(inp, "w") as f:
        f.write(" ".join(sys.argv[1:]))

    parser = argparse.ArgumentParser()
    add_arguments(parser)
    nmt.nmt.nmt.FLAGS, unparsed = parser.parse_known_args([
        "--out_dir={}".format(os.path.join(base_dir, "model")),
        "--inference_input_file={}".format(inp),
        "--inference_output_file={}".format(out)])
    tf.app.run(main=nmt_main, argv=[sys.argv[0]]+unparsed)
    

if __name__ == '__main__':
    main()
