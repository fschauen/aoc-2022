#!/usr/bin/env python3
from itertools import groupby

def part1(input_path):
    with open(input_path) as f:
        lines = map(str.strip, f)
        groups = [list(g) for k, g in groupby(lines, key=len) if k > 0]
        elves = [list(map(int, g)) for g in groups]
        print(max(map(sum, elves)))


def part2(input_path):
    with open(input_path) as f:
        lines = map(str.strip, f)
        groups = [list(g) for k, g in groupby(lines, key=len) if k > 0]
        elves = [list(map(int, g)) for g in groups]
        totals = sorted(map(sum, elves))
        print(sum(totals[-3:]))


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print('ERROR: input file path not provided', file=sys.stderr)
        sys.exit(1)

    part2(sys.argv[1])

