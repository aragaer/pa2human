#!/usr/bin/env python
import os

from nltk.stem.snowball import RussianStemmer


def tokenize(line):
    return line.strip().split()


def words_from_file(path):
    result = []
    with open(path) as d:
        for s in d:
            result.extend(tokenize(s))
    return result


def replace_numbers(words):
    return ['number' if w.isdigit() else w for w in words]


def words_to_stems(words):
    stemmer = RussianStemmer(ignore_stopwords=True)
    return [stemmer.stem(w) for w in words]


def normalize(words):
    words = [w.lower() for w in words]
    words = replace_numbers(words)
    return words_to_stems(words)
    

def prepare_text(line):
    return normalize(tokenize(line))


class Class:
    def __init__(self, stems):
        self.stems = stems
        self.ws = len(stems)


def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    classes = {}
    total_size = 0
    for f in os.listdir(data_dir):
        if not f.endswith(".txt"):
            continue
        cls_name = f[:-4]
        all_words = words_from_file(os.path.join(data_dir, f))
        words = replace_numbers(all_words)
        stems = words_to_stems(words)
        classes[cls_name] = Class(stems)
        total_size += classes[cls_name].ws
    return classes, total_size


def classify(line, classes, total_size):
    text = prepare_text(line)
    probs = {}
    for n, c in classes.items():
        prob = c.ws/total_size
        multiply = 1.0
        for w in text:
            count = c.stems.count(w)
            multiply *= (count + 0.1)/prob
        probs[n] = multiply * prob
    return max(probs, key=probs.get)


def main():
    total_size, classes = load_data()
    while True:
        try:
            line = input("enter a line: ")
        except EOFError:
            print()
            break
        result = classify(line, classes, total_size)
        print(result, probs[result], text, probs)


if __name__ == '__main__':
    main()
