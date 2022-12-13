#!/usr/bin/env python3
from functools import reduce

def make_groups(iterable, n):
    args = [iter(iterable)] * n
    return zip(*args)


def find_badge(group):
    badges = reduce(set.intersection, group)
    if len(badges) != 1:
        raise Exception(f'{len(badges)} badges in group {group}')
    return badges.pop()


def priority(item):
    if item.islower():
        return ord(item) - ord('a') + 1
    return ord(item) - ord('A') + 27


def part2(input_path):
    with open(input_path) as f:
        lines = filter(len, map(str.strip, f))
        rucksacks = map(set, lines)
        groups = make_groups(rucksacks, n=3)
        badges = map(find_badge, groups)
        prios = map(priority, badges)
        print(sum(prios))


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print('ERROR: input file path not provided', file=sys.stderr)
        sys.exit(1)

    part2(sys.argv[1])

