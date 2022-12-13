#!/usr/bin/env python3

def parse_rucksack(line):
    middle = len(line) // 2
    return set(line[0:middle]), set(line[middle:])


def inspect(rucksack):
    common = rucksack[0] & rucksack[1]
    if len(common) != 1:
        raise Exception(f'{len(common)} duplicates in {rucksack}')
    return common.pop()


def priority(item):
    if item.islower():
        return ord(item) - ord('a') + 1
    return ord(item) - ord('A') + 27


def part1(input_path):
    with open(input_path) as f:
        lines = filter(len, map(str.strip, f))
        rucksacks = map(parse_rucksack, lines)
        items = map(inspect, rucksacks)
        prios = map(priority, items)
        print(sum(prios))


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print('ERROR: input file path not provided', file=sys.stderr)
        sys.exit(1)

    part1(sys.argv[1])

