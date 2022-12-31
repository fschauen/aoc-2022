#!/usr/bin/env python3
from dataclasses import dataclass

@dataclass(frozen=True)
class Valve:
    name: str
    rate: int
    others: tuple  # of names of other valves


def parse(f):
    def parse_line(line):
        # Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
        # 0     1  2   3    4       5       6    7  8      9...
        pieces = line.split()
        name = pieces[1]
        rate = int(pieces[4].split('=')[1].strip(';'))
        others = tuple(p.strip(', ') for p in pieces[9:])
        return name, Valve(name, rate, others)

    non_empty_lines = filter(len, map(str.rstrip, f))
    return dict(parse_line(line) for line in non_empty_lines)


# def solve(valves, time=30):
#     def inner(remaining, opened, released, curent):
#         print(remaining, opened)
#         if remaining:
#             actions = [opened]
#             if current.rate > 0 and current not in opened:
#                 actions.append(opened + {current})

#             r = sum(v.rate for v in opened)

#             branches = [
#                 inner(remaining - 1, o, released + r, valve)
#                 for o in actions
#                 for valve in current.others]

#         else:
#             return opened

#     inner(time, {}, 0, valves['AA'])


def solve(valves, /, time=30):
    def inner(t, current, /, acc, releasing, paths, level=0):
        prefix = '    ' * level
        new = sum(v.rate for v in releasing)
        acc = acc + new

        branches = [acc]

        if t > 0:
            names = sorted(v.name for v in releasing)
            print(f'{prefix}\x1b[37mSTART {time - t + 1}  ->  {new} from {names}\x1b[0m')

            if current.rate > 0 and current not in releasing:
                print(f'{prefix}\x1b[91m+ open {current.name}')
                branches.append(inner(t-1, current,
                                      acc=acc,
                                      releasing=releasing | set([current]),
                                      paths=paths,
                                      level=level+1))

            for v in [valves[name] for name in current.others]:
                new_path = (current.name, v.name)
                if new_path not in paths:
                    print(f'{prefix}\x1b[36m> move to {v.name}\x1b[0m')
                    branches.append(inner(t-1, v,
                                          acc=acc,
                                          releasing=releasing,
                                          paths=paths | set([new_path]),
                                          level=level+1))
                else:
                    print(f'{prefix}\x1b[30m  skipping {new_path}\x1b[0m')

            result = max(branches)
            print(f'{prefix}\x1b[37mEND {time - t + 1}: {result} from {branches}\x1b[0m')

        return max(branches)

    return inner(time, valves['AA'], acc=0, releasing=set(), paths=set())


def part1(filepath):
    with open(filepath) as f:
        valves = parse(f)
        result = solve(valves, time=4)
        print(result)

        # for i, valve in enumerate(parse(f), start=1):
        #     print(f'{i:>2}: {valve}')


if __name__ == '__main__':
    import sys
    for filepath in sys.argv[1:]:
        print(f'Input file: {filepath}')
        print(f'  Part 1: {part1(filepath)}')
        # print(f'  Part 2: {part2(filepath)}')
        print()

