#!/usr/bin/env python3
from itertools import tee, islice

def rolling_window(iterable, width=2):
    return zip(*[
        islice(it, skip, None)
        for skip, it
        in enumerate(tee(iterable, width))
    ])


def find_start(line, /, length):
    for i, s in enumerate(map(set, rolling_window(line, width=length))):
        if len(s) == length:
            return i + length


def part1(filepath):
    with open(filepath) as f:
        return find_start(f.read(), length=4)  # start of packet → 4


def part2(filepath):
    with open(filepath) as f:
        return find_start(f.read(), length=14)  # start of message → 14


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print('ERROR: input file(s) not provided', file=sys.stderr)
        sys.exit(1)

    for filepath in sys.argv[1:]:
        print(f'Input file: {filepath}')
        print(f'  Part 1: {part1(filepath)}')
        print(f'  Part 2: {part2(filepath)}')
        print()

