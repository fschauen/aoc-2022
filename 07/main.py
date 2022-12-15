#!/usr/bin/env python3
from dataclasses import dataclass, field
from operator import attrgetter

@dataclass
class File:
    name: str
    size: int


@dataclass
class Directory:
    name: str
    children: list = field(default_factory=list)

    @property
    def size(self):
        return sum(child.size for child in self.children)

    def __getitem__(self, key):
        for child in self.children:
            if child.name == key:
                return child
        raise KeyError(f'`{key}` not found in {self.name}')

    def walk_dirs(self):
        yield self
        for child in self.children:
            if isinstance(child, Directory):
                yield from child.walk_dirs()


def parse_terminal_output(lines):
    root = Directory('/')
    stack = [root]
    pwd = stack[-1]
    for line in lines:
        if line.startswith('$'):
            _, cmd, *args = line.split()
            if cmd == 'cd':
                name = args[0]
                if name == '/':     stack = [root]
                elif name == '..':  stack.pop()
                else:               stack.append(pwd[name])
                pwd = stack[-1]
            else:
                pass  # ingore other commands, including `ls`

        else:  # assume the line is output of `ls`
            size, name = line.split()
            item = Directory(name) if size == 'dir' else File(name, int(size))
            pwd.children.append(item)

    return root


def part1(filepath):
    with open(filepath) as f:
        lines = filter(len, map(str.rstrip, f))
        root = parse_terminal_output(lines)
        return sum(d.size for d in root.walk_dirs() if d.size < 100_000)


def part2(filepath, disk_size=70_000_000, space_required=30_000_000):
    with open(filepath) as f:
        lines = filter(len, map(str.rstrip, f))
        root = parse_terminal_output(lines)
        available_space = disk_size - root.size

        for d in sorted(root.walk_dirs(), key=attrgetter('size')):
            if available_space + d.size >= space_required:
                return d.size


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

