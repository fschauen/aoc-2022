#!/usr/bin/env python3
import math
import operator
from collections import deque
from dataclasses import dataclass
from itertools import groupby
from typing import Optional

def tail(line, sep):
    return line.split(sep)[-1].strip()


def is_empty(line):
    return len(line.strip()) == 0


@dataclass
class Operation:
    function: str
    arg: Optional[int]

    @classmethod
    def parse(cls, string):
        _, op, arg = string.split(' ')
        if   op == '+': function = operator.add
        elif op == '*': function = operator.mul
        else:           raise ValueError(f'Invalid operation: {op}')
        return cls(function, None if arg == 'old' else int(arg))

    def apply(self, old):
        return self.function(old, old if self.arg is None else self.arg)


@dataclass
class Monkey:
    items: deque
    operation: Operation
    divisor: int
    if_true: int
    if_false: int
    activity: int = 0

    @classmethod
    def parse(cls, lines):
        return cls(
            # Skip line[0] -> 'Monkey #:'
            items     = deque(int(item) for item in tail(lines[1], ':').split(',')),
            operation = Operation.parse(tail(lines[2], '=')),
            divisor   = int(tail(lines[3], 'by')),
            if_true   = int(tail(lines[4], ' ')),
            if_false  = int(tail(lines[5], ' ')))

    def inspect(self, item):
        self.activity += 1
        return self.operation.apply(item)

    def decide(self, item):
        return self.if_true if item % self.divisor == 0 else self.if_false


def parse_monkeys(f):
    for empty, lines in groupby(f.read().split('\n'), is_empty):
        if not empty:
            yield Monkey.parse(list(lines))


def round_part1(monkeys):
    for monkey in monkeys:
        while monkey.items:
            item = monkey.items.popleft()       # Pick an item (left to right).
            item = monkey.inspect(item)         # Inspect item (worry increases).
            item = item // 3                    # Relief.
            rx = monkeys[monkey.decide(item)]   # Monkey decides where to throw.
            rx.items.append(item)               # Receiver gets the item.


def round_part2(monkeys):
    worry_cap = math.lcm(*[m.divisor for m in monkeys])
    for monkey in monkeys:
        while monkey.items:
            item = monkey.items.popleft()       # Pick an item (left to right).
            item = monkey.inspect(item)         # Inspect item (worry increases).

            # Since the monkeys make decisions based on divisibility by
            # a certain number, we cap the worry to the Least Common Multiplier
            # of all divisors. This keeps the maximum worry under control but
            # leaves the monkeys' decisions unchanged.
            item = item % worry_cap

            rx = monkeys[monkey.decide(item)]   # Monkey decides where to throw.
            rx.items.append(item)               # Receiver gets the item.


def solve(filepath, /, rounds, play_round):
    with open(filepath) as f:
        monkeys = list(parse_monkeys(f))
        for i in range(rounds):
            play_round(monkeys)
        monkeys = sorted(monkeys, key=lambda m: m.activity)
        return monkeys[-1].activity * monkeys[-2].activity


def part1(filepath):
    return solve(filepath, rounds=20, play_round=round_part1)


def part2(filepath):
    return solve(filepath, rounds=10_000, play_round=round_part2)


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

