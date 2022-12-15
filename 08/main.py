#!/usr/bin/env python3
import functools
import operator

def parse_trees(f):
    lines = filter(len, map(str.rstrip, f))
    return tuple(tuple(int(tree) for tree in line) for line in lines)


def T(trees):
    '''Transpose the trees'''
    return tuple(zip(*trees))


def R(trees):
    '''Reverse each row of trees'''
    return tuple(tuple(reversed(row)) for row in trees)


def visible_from_west(trees):
    def look_from_west(row):
        tallest = -1
        for tree in row:
            if tree > tallest:
                tallest = tree
                yield True
            else:
                yield False

    return tuple(tuple(look_from_west(row)) for row in trees)


def part1(filepath):
    with open(filepath) as f:
        trees = parse_trees(f)

        west = visible_from_west(trees)
        east = R(visible_from_west(R(trees)))
        north = T(visible_from_west(T(trees)))
        south = T(R(visible_from_west(R(T(trees)))))

        # Visibility is how many directions each tree is visible from:
        #   == 0 -> hidden
        #    > 0 -> visible
        visibility = tuple(
            sum(directions)
            for row in zip(west, east, north, south)
            for directions in zip(*row))

        # How many trees are visible.
        return sum(map(lambda v: v > 0, visibility))


def view_distance_to_east(trees):
    def look_east(row):
        for i, tree in enumerate(row):
            distance = 0
            for other in row[i + 1:]:
                distance += 1
                if other >= tree:
                    break
            yield distance

    return tuple(tuple(look_east(row)) for row in trees)


def part2(filepath):
    with open(filepath) as f:
        trees = parse_trees(f)

        east = view_distance_to_east(trees)
        west = R(view_distance_to_east(R(trees)))
        south = T(view_distance_to_east(T(trees)))
        north = T(R(view_distance_to_east(R(T(trees)))))

        # Scenic score is the product of view distances in all directions.
        scenic_score = tuple(
            functools.reduce(operator.mul, directions)
            for row in zip(west, east, north, south)
            for directions in zip(*row))

        return max(scenic_score)


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

