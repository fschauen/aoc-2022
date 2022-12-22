#!/usr/bin/env python3
def execute(program):
    x = 1
    for instruction in program:
        if instruction == 'noop':
            yield x
        elif instruction.startswith('addx'):
            _, v = instruction.split()
            yield x
            yield x
            x += int(v)
        else:
            raise ValueError(f'Invalid instruction: {instruction}')
    yield x


def part1(filepath):
    with open(filepath) as f:
        program = filter(len, map(str.rstrip, f))
        xs = execute(program)
        cycles = enumerate(xs, start=1)
        interesting = filter(
            lambda c: c[0] in (20, 60, 100, 140, 180, 220),
            cycles)
        return sum(n * x for n, x in interesting)


def draw_crt(xs, rows=6, columns=40):
    for _ in range(rows):
        yield ''.join(
            '█' if abs(x - i) < 2 else ' '
            for i, x in zip(range(columns), xs))


def part2(filepath):
    with open(filepath) as f:
        program = filter(len, map(str.rstrip, f))
        xs = execute(program)
        crt = draw_crt(xs)
        for row in crt:
            print(f'    {row}')


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print('ERROR: input file(s) not provided', file=sys.stderr)
        sys.exit(1)

    for filepath in sys.argv[1:]:
        print(f'Input file: {filepath}')
        print(f'  Part 1: {part1(filepath)}')
        print(f'  Part 2:')
        part2(filepath)
        print()

