#!/usr/bin/env python

import json
import sys

from PIL import Image


def get_color_values(filename):
    with Image.open(filename) as image:
        # print(image.format, image.size, image.mode)
        pixels = image.load()
        width, height = image.size
        counts = []
        for x in range(0, width):
            for y in range(0, height):
                r, g, b, a = pixels[x, y]
                if a == 0:
                    # Filter out transparent pixels
                    continue
                # "brightness" via https://stackoverflow.com/a/6449381
                value = (r + g + b) / 3
                counts.append(value)
        return counts


if __name__ == '__main__':
    filename = sys.argv[1]
    counts = get_color_values(filename)
    print(json.dumps({'counts': counts}))
