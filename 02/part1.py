#!/usr/bin/env python3
from enum import Enum
from itertools import starmap

class Shape(Enum):
    ROCK     = 0
    PAPER    = 1
    SCISSORS = 2

    @classmethod
    def from_character(cls, character):
        if character in 'ABC':
            return cls(ord(character) - ord('A'))

        if character in 'XYZ':
            return cls(ord(character) - ord('X'))

        raise ValueError(f'{character} is not a valid shape')


def score(theirs, ours):
    LOSE, DRAW, WIN = 0, 3, 6
    outcome = [
        # Rock  Paper Scissors ← theirs, ours ↓
        [ DRAW, LOSE, WIN],             # Rock
        [ WIN,  DRAW, LOSE],            # Paper
        [ LOSE, WIN,  DRAW ]            # Scissors
    ]

    return outcome[ours.value][theirs.value] + ours.value + 1


def part1(input_path):
    with open(input_path) as f:
        lines = filter(len, map(str.strip,f))
        rounds = (map(Shape.from_character, line.split(' ')) for line in lines)
        scores = starmap(score, rounds)
        print(sum(scores))


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print('ERROR: input file path not provided', file=sys.stderr)
        sys.exit(1)

    part1(sys.argv[1])

