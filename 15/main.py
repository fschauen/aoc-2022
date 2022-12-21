#!/usr/bin/env python3
from dataclasses import dataclass
from itertools import tee
import re

@dataclass
class Vec2:
    x: int
    y: int


@dataclass
class Range:
    left: int
    right: int

    def __len__(self):
        return abs(self.right - self.left) + 1


def parse(f):
    def parse_line(line):
        sx, sy, bx, by = map(int, re.findall(r'-?\d+', line))
        sensor, beacon = Vec2(sx, sy), Vec2(bx, by)
        distance = abs(sensor.x - beacon.x) + abs(sensor.y - beacon.y)
        return sensor, beacon, distance

    return [parse_line(line) for line in filter(len, map(str.rstrip, f))]


def covered_ranges(data, y):
    for sensor, _, radius in data:
        dy = abs(sensor.y - y)
        if dy < radius:
            dx = radius - dy
            yield Range(sensor.x - dx, sensor.x + dx)


def merge_ranges(ranges):
    iterator = iter(sorted(ranges, key=lambda s: s.left))
    current = next(iterator, None)
    for it in iterator:
        if it.left <= current.right + 1:
            current.right = max(it.right, current.right)
        else:
            yield current
            current = it
    yield current


def part1(filepath, /, y=10):
    with open(filepath) as f:
        data = parse(f)
        ranges = covered_ranges(data, y)
        merged = merge_ranges(ranges)
        covered = sum(len(part) for part in merged)
        beacons = len(set(b.x for _, b, _ in data if b.y == y))
        return covered - beacons


def cap_ranges(ranges, lower, upper):
    return (Range(max(r.left, lower), min(r.right, upper)) for r in ranges)


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def find_uncovered(coverage, lower, upper):
    yield from range(lower, coverage[0].left)
    if len(coverage) > 1:
        for a, b in pairwise(coverage):
            yield from range(a.right + 1, b.left)
        yield from range(coverage[-1].right + 1, upper)


def part2(filepath, /, lower, upper):
    with open(filepath) as f:
        data = parse(f)
        for y in range(lower, upper+1):
            ranges = covered_ranges(data, y)
            merged = merge_ranges(ranges)
            covered = list(cap_ranges(merged, lower, upper))

            assert covered, f'No coverage at y={y}'
            for x in find_uncovered(covered, lower, upper):
                tuning = x * 4_000_000 + y
                print(f'    {tuning}  ->  ({x}, {y})')


if __name__ == '__main__':
    sample_path = 'sample.txt'
    print(f'Input file: {sample_path}')
    print(f'  Part 1: {part1(sample_path, y=10)}')
    print(f'  Part 2:')
    part2(sample_path, lower=0, upper=20)

    print()

    input_path = 'input.txt'
    print(f'Input file: {input_path}')
    print(f'  Part 1: {part1(input_path, y=2_000_000)}')
    print(f'  Part 2:')
    part2(input_path, lower=0, upper=4_000_000)

