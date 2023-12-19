from task import Task
from dataclasses import dataclass, astuple
import numpy as np
from collections import deque

from numba import njit

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


@dataclass(frozen=True)
class Pos:
    r: int
    c: int

    def __add__(self, other):
        return Pos(self.r + other.r, self.c+other.c)

    def __mul__(self, other):
        return Pos(self.r * other, self.c * other)


@dataclass(order=True)
class Segment:
    x: int
    y: int
    end: int


deltas = [
    Pos(-1, 0),
    Pos(0, 1),
    Pos(1, 0),
    Pos(0, -1),
]

dirmap = {
    "U": UP,
    "L": LEFT,
    "R": RIGHT,
    "D": DOWN,
}

dirmap2 = {
    "3": UP,
    "2": LEFT,
    "0": RIGHT,
    "1": DOWN,
}

MARK = ord("#")
EMPTY = ord(" ")
INSIDE = ord(".")


def parse1(text):
    directions = []
    for line in text.splitlines():
        d, n, color = line.split(" ")
        directions.append((dirmap[d], int(n)))
    return directions

def parse2(text):
    directions = []
    for line in text.splitlines():
        d, n, color = line.split(" ")
        directions.append((dirmap2[color[-2]], int(color[2:-2], 16)))
    return directions


def get_lines(directions, doi, prim, sec):
    pos = Pos(0, 0)
    segments = []
    for d, steps, in directions:
        npos = pos + deltas[d]*steps
        if d in doi:
            l = min(astuple(pos)[prim], astuple(npos)[prim])
            segments.append(Segment(l, astuple(pos)[sec], l+steps))
        pos = npos
    return segments


class AreaCalc:
    def __init__(self, lines):
        self.lines = lines
        self.area = 0

    def calculate_at(self, at):
        relevant = [seg for seg in self.lines if seg.x <= at <= seg.end]
        relevant.sort(key=lambda k: k.y)

        total = 0
        inside = False
        last_inside = False
        last_y = 0
        border = False

        last = None
        for seg in relevant:
            cur = None
            if seg.x == at:
                cur = "start"
            if seg.end == at:
                cur = "end"

            if cur is not None and last is not None:
                border = not border
            else:
                border = False

            if inside or border: # am inside
                total += seg.y - last_y
            else:
                total += 1
            last_y = seg.y

            inside_bak = inside
            if cur is None:
                inside = not inside
            elif last is None:
                inside = True
            elif last == cur:
                inside = last_inside
            else:
                if border:
                    inside = not last_inside

            last_inside = inside_bak
            last = cur
        return total


def calc_events(lines):
    ac = AreaCalc(lines)

    events = set()
    for seg in lines:
        events.add(seg.x)
        events.add(seg.x+1)
        events.add(seg.end)
        events.add(seg.end+1)

    events = sorted(events)

    last_i = 0
    last_count = 0
    total = 0
    for i in events:
        total += last_count * (i - last_i)
        last_count = ac.calculate_at(i)
        last_i = i
    return total


def part1(text, timer):
    directions = parse1(text)
    timer.parsed()

    lines = get_lines(directions, [1, 3], 1, 0)
    lines.sort()

    return calc_events(lines)

def part2(text, timer):
    directions = parse2(text)
    timer.parsed()

    lines = get_lines(directions, [1, 3], 1, 0)
    lines.sort()
    return calc_events(lines)



task = Task(
    18,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark(50)

