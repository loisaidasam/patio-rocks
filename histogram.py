#!/usr/bin/env python

# Ripped from https://gist.github.com/loisaidasam/4c2ea6655ff0d12977ff9f3f698ba90e

import argparse
import json
import math
import os.path
import pickle

import matplotlib.pyplot as plt


def main():
    args = parse_args()
    title = args.title or (args.filename and os.path.basename(args.filename))
    data = get_data(args)
    return plot(data, title, args.bins)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', help="Input data filename")
    parser.add_argument('--data', help="Space-delimited string of data points")
    parser.add_argument('--title', help="Optional, defaults to filename")
    parser.add_argument('--bins',
                        type=int,
                        default=None,
                        help="Num bins (something like '50'), otherwise set dynamically based on max value")
    return parser.parse_args()


def get_data(args):
    if args.data:
        return map(int, args.data.split())
    if not args.filename:
        raise Exception("Missing `filename` or `--data`")
    with open(args.filename, 'r') as fp:
        if args.filename.endswith('.json'):
            return find_data_list(json.load(fp))
        if args.filename.endswith('.p'):
            return find_data_list(pickle.load(fp))
        # If no extension, assume data is delimited by spaces or newlines
        return map(int, fp.read().split())


def find_data_list(data):
    """Take an object and find the first list
    """
    if isinstance(data, list):
        # List, cool
        return data
    if not isinstance(data, dict):
        raise Exception("Loaded data type that we don't know what to do with")
    print("Loaded dict with keys: %s" % data.keys())
    for key, value in data.items():
        # Look for first list value
        if isinstance(value, list):
            print("Choosing key: `%s`" % key)
            return value
    raise Exception("Loaded dict with no list values!")


def plot(data, title, bins):
    # data = [1, 2, 3]
    print("%s data points" % len(data))
    if not bins:
        bin_range = max(data) + 1
        print("bin range: %s" % bin_range)
        bins = range(int(math.ceil(bin_range)))
    n, bins, patches = plt.hist(data, bins=bins, facecolor='green', alpha=0.75)
    if title:
        print("Title: %s" % title)
        plt.title(title)
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()
