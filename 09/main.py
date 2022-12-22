#!/usr/bin/env python3
from dataclasses import dataclass, astuple
from itertools import tee

@dataclass
class Point:
    x: int = 0
    y: int = 0


def parse_motion(line):
    direction, count_str = line.split()
    return direction, int(count_str)


def sign(n):
    return 1 if n > 0 else (-1 if n < 0 else 0)


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def execute(motions, rope):
    yield rope
    for direction, count in motions:
        for _ in range(count):
            # Move head one step in `direction`...
            if   direction == 'R':  rope[0].x += 1
            elif direction == 'L':  rope[0].x -= 1
            elif direction == 'U':  rope[0].y += 1
            elif direction == 'D':  rope[0].y -= 1
            else: raise ValueError(f'Invalid direction {direction}')

            # ... and then move tail knots as needed.
            for a, b in pairwise(rope):
                dx, dy = a.x - b.x, a.y - b.y
                if abs(dx) > 1 or abs(dy) > 1:
                    b.x += sign(dx)
                    b.y += sign(dy)

            yield rope


def solve(filepath, knot_count):
    rope = [Point() for _ in range(knot_count)]
    with open(filepath) as f:
        lines = filter(len, map(str.rstrip, f))
        motions = map(parse_motion, lines)
        steps = execute(motions, rope)
        visited = set(astuple(step[-1]) for step in steps)
        return len(visited)


def part1(filepath):
    return solve(filepath, knot_count=2)


def part2(filepath):
    return solve(filepath, knot_count=10)


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

