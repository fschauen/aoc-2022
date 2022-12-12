#!/usr/bin/env python3
from enum import Enum
from itertools import starmap

class Shape(Enum):
    ROCK     = 1
    PAPER    = 2
    SCISSORS = 3

    @classmethod
    def from_character(cls, character):
        if character in 'ABC':
            return cls(ord(character) - ord('A') + 1)
        raise ValueError(f'{character} is not a valid shape')

    def as_index(self):
        return self.value - 1


class Outcome(Enum):
    LOSE = 0
    DRAW = 3
    WIN  = 6

    @classmethod
    def from_character(cls, character):
        if character in 'XYZ':
            return cls(3 * (ord(character) - ord('X')))
        raise ValueError(f'{character} is not a valid outcome')

    def as_index(self):
        return self.value // 3


def parse(f):
    lines = filter(len, map(str.strip,f))
    for line in lines:
        parts = line.split(' ')
        yield Shape.from_character(parts[0]), Outcome.from_character(parts[1])


def score(theirs, outcome):
    MAP = [
        # Lose              Draw            Win         ← outcome, theirs ↓
        [ Shape.SCISSORS,   Shape.ROCK,     Shape.PAPER],               # Rock
        [ Shape.ROCK,       Shape.PAPER,    Shape.SCISSORS],            # Paper
        [ Shape.PAPER,      Shape.SCISSORS, Shape.ROCK]                 # Scissors
    ]
    ours = MAP[theirs.as_index()][outcome.as_index()]
    return outcome.value + ours.value


def part2(input_path):
    with open(input_path) as f:
        rounds = parse(f)
        scores = starmap(score, rounds)
        print(sum(scores))


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print('ERROR: input file path not provided', file=sys.stderr)
        sys.exit(1)

    part2(sys.argv[1])

