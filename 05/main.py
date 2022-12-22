#!/usr/bin/env python3
from collections import namedtuple
from itertools import takewhile

def parse_stacks(lines):
    columns = [col for col, char in enumerate(lines[-1]) if char != ' ']
    stacks = [[] for _ in range(len(columns))]

    for line in reversed(lines[:-1]):
        for stack, col in zip(stacks, columns):
            if col < len(line) and line[col] != ' ':
                stack.append(line[col])

    return stacks


Instruction = namedtuple('Instruction', 'count,src,dst')
def parse_instruction(line):
    parts = line.split(' ')
    return Instruction(
        count=int(parts[1]),
        src=int(parts[3]) - 1,  # we index the stacks from 0
        dst=int(parts[5]) - 1   # we index the stacks from 0
    )


def crate_mover_9000(stacks, instructions):
    for inst in instructions:
        for _ in range(inst.count):
            src, dst = stacks[inst.src], stacks[inst.dst]
            dst.append(src.pop())


def crate_mover_9001(stacks, instructions):
    for inst in instructions:
        src, dst = stacks[inst.src], stacks[inst.dst]
        bottom = len(src) - inst.count
        dst.extend(src[bottom:])
        del src[bottom:]


def solve(filepath, crate_mover):
    with open(filepath) as f:
        lines = map(str.rstrip, f)
        stacks = parse_stacks(list(takewhile(len, lines)))
        instructions = map(parse_instruction, lines)
        crate_mover(stacks, instructions)
        tops = [s[-1] for s in stacks]
        return ''.join(tops)


def part1(filepath):
    return solve(filepath, crate_mover_9000)


def part2(filepath):
    return solve(filepath, crate_mover_9001)


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

