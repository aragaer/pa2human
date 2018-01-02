#!/usr/bin/env python3

import argparse
import os
import sys

from random import shuffle

import nmt
import tensorflow as tf

from nmt.nmt.nmt import main as nmt_main, add_arguments

from vocab import make_vocabs


def make_training(train_dir, samples_dir):
    if not os.path.exists(train_dir):
        os.mkdir(train_dir)
    with open(os.path.join(samples_dir, "human.txt")) as human:
        full_human = human.readlines()
    with open(os.path.join(samples_dir, "bot.txt")) as bot:
        full_bot = bot.readlines()

    filtered = [(h, b) for h, b in zip(full_human, full_bot)
                       if not b.startswith("unintelligible")]
    shuffle(filtered)
    cnt = len(filtered)
    train_cnt = int(cnt * 0.6)
    dev_cnt = int(cnt * 0.2)
    with open(os.path.join(train_dir, "train.human"), "w") as h:
        for i in range(train_cnt):
            h.write(filtered[i][0])

    with open(os.path.join(train_dir, "dev.human"), "w") as h:
        for i in range(train_cnt, train_cnt+dev_cnt):
            h.write(filtered[i][0])

    with open(os.path.join(train_dir, "test.human"), "w") as h:
        for i in range(train_cnt+dev_cnt, cnt):
            h.write(filtered[i][0])

    with open(os.path.join(train_dir, "train.bot"), "w") as b:
        for i in range(train_cnt):
            b.write(filtered[i][1])

    with open(os.path.join(train_dir, "dev.bot"), "w") as b:
        for i in range(train_cnt, train_cnt+dev_cnt):
            b.write(filtered[i][1])

    with open(os.path.join(train_dir, "test.bot"), "w") as b:
        for i in range(train_cnt+dev_cnt, cnt):
            b.write(filtered[i][1])

def main():
    base_dir = os.path.dirname(__file__)
    vocab_dir = os.path.join(base_dir, "vocab")
    if not os.path.exists(vocab_dir):
        os.mkdir(vocab_dir)
    make_vocabs()

    samples_dir = os.path.join(base_dir, "samples")
    train_dir = os.path.join(base_dir, "train")
    make_training(train_dir, samples_dir)

    parser = argparse.ArgumentParser()
    add_arguments(parser)
    nmt.nmt.nmt.FLAGS, unparsed = parser.parse_known_args([
        "--src=human", "--tgt=bot",
        "--vocab_prefix={}".format(os.path.join(vocab_dir, "vocab")),
        "--train_prefix={}".format(os.path.join(train_dir, "train")),
        "--dev_prefix={}".format(os.path.join(train_dir, "dev")),
        "--test_prefix={}".format(os.path.join(train_dir, "test")),
        "--out_dir={}".format(os.path.join(base_dir, "model")),
        "--num_train_steps=12000",
        "--steps_per_stats=100",
        "--num_layers=2",
        "--num_units=128",
        "--dropout=0.2",
        "--metrics=bleu"])
    tf.app.run(main=nmt_main, argv=[sys.argv[0]]+unparsed)
    

if __name__ == '__main__':
    main()
