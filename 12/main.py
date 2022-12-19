#!/usr/bin/env python3
from dataclasses import dataclass
from functools import cached_property

def height(value):
    if value == 'S': value = 'a'
    if value == 'E': value = 'z'
    return ord(value) - ord('a')


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


@dataclass
class HeightMap:
    contents: list
    start: Point
    end: Point

    @classmethod
    def parse(cls, f):
        lines = filter(len, map(str.rstrip, f))
        start, end, rows = None, None, []
        for y, line in enumerate(lines):
            rows.append(line)
            for x, cell in enumerate(line):
                if cell == 'S': start = Point(x, y)
                if cell == 'E': end   = Point(x, y)
        return cls(rows, start, end)

    def __getitem__(self, point):
        return self.contents[point.y][point.x]

    def __iter__(self):
        for y, row in enumerate(self.contents):
            for x, item in enumerate(row):
                yield Point(x, y), item

    @cached_property
    def width(self):
        return len(self.contents[0])

    @cached_property
    def height(self):
        return len(self.contents)

    def neighbors(self, point):
        result = set()
        for delta in (Point(0, -1), Point(-1, 0), Point(0, +1), Point(+1, 0)):
            neighbor = point + delta
            if all((neighbor.x >= 0, neighbor.x < self.width,
                    neighbor.y >= 0, neighbor.y < self.height)):
                result.add(neighbor)
        return result

    # Expand the border from Start until we reach the End, while making sure we
    # don't double back and only climb when not too steep. The path length is
    # equal to the number of times we expanded the border.
    def shortest_path(self, start=None):
        border = { start if start is not None else self.start }
        visited = set()
        count = 0
        while border:
            count += 1
            next_border = set()
            for item in border:
                visited.add(item)
                for neighbor in self.neighbors(item):
                    # This neighbor was already visited via another (shorter)
                    # path -> ignore it.
                    if neighbor in visited:
                        continue

                    # Ignore the neighbor it the climb is too steep.
                    if height(self[neighbor]) - height(self[item]) > 1:
                        continue

                    # Reached the end -> DONE!
                    if neighbor == self.end:
                        return count

                    next_border.add(neighbor)
            border = next_border

        # Could not reach the end.
        return None


def part1(filepath):
    with open(filepath) as f:
        return HeightMap.parse(f).shortest_path()


def part2(filepath):
    with open(filepath) as f:
        hm = HeightMap.parse(f)
        starting_positions = [p for p, value in hm if value in 'aS']
        return min(filter(None, map(hm.shortest_path, starting_positions)))


if __name__ == '__main__':
    import sys
    for filepath in sys.argv[1:]:
        print(f'Input file: {filepath}')
        print(f'  Part 1: {part1(filepath)}')
        print(f'  Part 2: {part2(filepath)}')
        print()

