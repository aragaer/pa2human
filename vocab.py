#!/usr/bin/env python3
import os

def tokenize(line):
    return line.strip().split()


def words_from_file(path):
    result = []
    with open(path) as d:
        for s in d:
            result.extend(tokenize(s))
    return result


def make_vocabs():
    base_dir = os.path.dirname(__file__)
    samples_dir = os.path.join(base_dir, "samples")
    vocab_dir = os.path.join(base_dir, "vocab")
    for f in os.listdir(samples_dir):
        if not f.endswith(".txt"):
            continue
        lang = f[:-4]
        all_words = words_from_file(os.path.join(samples_dir, f))
        with open(os.path.join(vocab_dir, "vocab.{}".format(lang)), "w") as vocab:
            for word in set(all_words):
                print(word, file=vocab)


if __name__ == '__main__':
    make_vocabs()
