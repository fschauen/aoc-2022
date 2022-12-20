#!/usr/bin/env python3
from functools import cmp_to_key, reduce
from itertools import zip_longest, chain
from operator import add, mul
import json

def parse(f):
    return map(json.loads, filter(len, map(str.rstrip, f)))


def grouper(iterable, n):
    iters = [iter(iterable)] * n
    return zip(*iters)


def compare_ints(left, right):
    if   left < right:   return -1
    elif left == right:  return  0
    else:                return  1


def compare(left, right):
    match left, right:
        case    int(),    int(): return compare_ints(left, right)
        case     [*_],    int(): return compare(left, [right])
        case    int(),     [*_]: return compare([left], right)
        case       [],       []: return  0
        case       [],        _: return -1
        case        _,       []: return  1
        case [x, *xs], [y, *ys]: return compare(x, y) or compare(xs, ys)

        case _:
            print(f"ERROR: can't compare {left} and {right}")
            return 0


def valid_pair_indices(pairs):
    for index, (left, right) in enumerate(pairs, start=1):
        if compare(left, right) < 1:
            yield index


def part1(filepath):
    with open(filepath) as f:
        packets = parse(f)
        pairs = grouper(packets, n=2)
        return reduce(add, valid_pair_indices(pairs))


def find_indices(needles, /, haystack):
    for index, packet in enumerate(haystack, start=1):
        if packet in needles:
            yield index


def part2(filepath):
    with open(filepath) as f:
        dividers = ([[2]], [[6]])
        packets = chain(parse(f), dividers)
        ordered = sorted(packets, key=cmp_to_key(compare))
        return reduce(mul, find_indices(dividers, haystack=ordered))


if __name__ == '__main__':
    import sys
    for filepath in sys.argv[1:]:
        print(f'Input file: {filepath}')
        print(f'  Part 1: {part1(filepath)}')
        print(f'  Part 2: {part2(filepath)}')
        print()

