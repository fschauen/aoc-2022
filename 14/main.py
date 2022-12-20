#!/usr/bin/env python3
from dataclasses import dataclass
from math import copysign

@dataclass(frozen=True)
class Vec2:
    x: int
    y: int

    @classmethod
    def from_str(cls, s):
        return cls(*map(int, s.split(',')))

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(slef, other):
        return Vec2(slef.x - other.x, slef.y - other.y)

    def __mul__(self, scalar):
        return Vec2(self.x * scalar, self.y * scalar)


def parse_file(f):
    tiles = set()
    for line in filter(len, map(str.rstrip, f)):
        points = [Vec2.from_str(piece) for piece in line.split('->')]
        for begin, end in zip(points[:-1], points[1:]):
            match end - begin:
                case Vec2(x=0,    y=dist): unit = Vec2(0, 1)
                case Vec2(x=dist, y=0   ): unit = Vec2(1, 0)
                case _: raise ValueError(f'Invalid delta: {end - begin}')
            steps = (int(copysign(i, dist)) for i in range(0, abs(dist)+1))
            tiles |= {begin + unit * i for i in steps}
    return tiles


def part1(filepath, start=Vec2(500, 0)):
    with open(filepath) as f:
        tiles = parse_file(f)
        rocks = len(tiles)
        void = max(tiles, key=lambda t: t.y).y
        sand = start
        while sand.y < void:
            moved = None
            for delta in (Vec2(0,1), Vec2(-1,1), Vec2(1,1)):
                if moved is None and sand + delta not in tiles:
                    moved = sand + delta

            if moved is None:
                tiles.add(sand) # Stopped moving -> mark location...
                sand = start    # .. and create a new sand unit.
            else:
                sand = moved    # Keep moving!

        return len(tiles) - rocks


def part2(filepath, start=Vec2(500, 0)):
    with open(filepath) as f:
        tiles = parse_file(f)
        rocks = len(tiles)
        floor = 2 + max(tiles, key=lambda t: t.y).y
        sand = start
        while True:
            moved = None
            if sand.y + 1 < floor:
                for d in (Vec2(0,1), Vec2(-1,1), Vec2(1,1)):
                    if moved is None and sand + d not in tiles:
                        moved = sand + d

            if moved is None:
                tiles.add(sand)     # Stopped moving -> mark location...
                if sand != start:
                    sand = start    # ... and create a new sand unit...
                else:
                    break           # ... unless the start is clogged.
            else:
                sand = moved        # Keep moving!

        return len(tiles) - rocks


if __name__ == '__main__':
    import sys
    for filepath in sys.argv[1:]:
        print(f'Input file: {filepath}')
        print(f'  Part 1: {part1(filepath)}')
        print(f'  Part 2: {part2(filepath)}')
        print()

