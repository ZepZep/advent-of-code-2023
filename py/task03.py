from task import Task
import re
from dataclasses import dataclass, astuple

@dataclass
class PartNum:
    num: int
    r: int
    s: int
    e: int
    adjacent: list

@dataclass
class Symbol:
    char: str
    r: int
    c: int
    adjacent: list


def parse_blueprint(lines):
    numbers = {(n.r, n.s): n for n in get_nums(lines)}
    symbols = {(s.r, s.c): s for s in get_symbols(lines)}

    connect_ns(lines, numbers, symbols)

    return numbers, symbols


def get_nums(lines):
    for r, line in enumerate(lines):
        for m in re.finditer("[0-9]+", line):
            s, e = m.span()
            yield PartNum(int(m.group(0)), r, s, e, [])


def get_symbols(lines):
    for r, line in enumerate(lines):
        for m in re.finditer("[^0-9\.]", line):
            s, e = m.span()
            yield Symbol(m.group(0), r, s, [])


def connect_ns(lines, numbers, symbols):
    mr = len(lines) - 1
    mc = len(lines[0]) - 1
    for num in numbers.values():
        for spos in get_neighborhood(num):
            if not is_good_coord(spos, mr, mc):
                continue
            r, c = spos
            if is_symbol(lines[r][c]):
                symbol = symbols[r,c]
                num.adjacent.append(symbol)
                symbol.adjacent.append(num)


def is_good_coord(pos, mr, mc):
    r, c = pos
    if not (0 <= r <= mr):
        return False
    if not (0 <= c <= mc):
        return False
    return True


def is_symbol(char):
    if char == ".":
        return False
    if char.isnumeric():
        return False
    return True


def get_neighborhood(num):
    yield num.r, num.s-1
    yield num.r, num.e
    for pr in (num.r-1, num.r+1):
        for pc in range(num.s-1, num.e+1):
            yield pr, pc


def part1(text, timer):
    lines = text.split("\n")[:-1]
    numbers, symbols = parse_blueprint(lines)
    timer.parsed()

    output = 0
    for num in numbers.values():
        if num.adjacent:
             output += num.num
    return output


def part2(text, timer):
    lines = text.split("\n")[:-1]
    numbers, symbols = parse_blueprint(lines)
    timer.parsed()

    output = 0
    for sym in symbols.values():
        if sym.char != "*":
            continue
        if len(sym.adjacent) != 2:
            continue
        n1, n2 = sym.adjacent
        output += n1.num * n2.num
    return output


task = Task(
    3,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark(100)

