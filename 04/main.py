#!/usr/bin/env python3
from functools import partial
from itertools import starmap

def parse_range(range_str):
    start, end = map(int, range_str.split('-'))
    return set(range(start, end + 1))


def solve(filepath, select_pairs):
    with open(filepath) as f:
        lines = filter(len, map(str.strip, f))
        ranges = map(partial(str.split, sep=','), lines)
        pairs = map(lambda s: map(parse_range, s), ranges)
        overlaps = starmap(select_pairs, pairs)
        return sum(overlaps)


def full_overlap(a, b):
    return a.issubset(b) or b.issubset(a)


def part1(filepath):
    return solve(filepath, full_overlap)


def any_overlap(a, b):
    return not a.isdisjoint(b)


def part2(filepath):
    return solve(filepath, any_overlap)


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

