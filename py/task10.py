from task import Task
from dataclasses import dataclass
import numpy as np
import sys
sys.setrecursionlimit(100000)

@dataclass(frozen=True)
class Pos:
    r: int
    c: int

    def __add__(self, other):
        return Pos(self.r + other.r, self.c+other.c)

    def __mul__(self, other):
        return Pos(self.r * other, self.c * other)


n_ = Pos(-1,  0)
s_ = Pos( 1,  0)
e_ = Pos( 0,  1)
w_ = Pos( 0, -1)

dirs = [n_, s_, e_, w_]

opposite = {
    n_: s_,
    s_: n_,
    e_: w_,
    w_: e_,
}

connections ={
    "|": (n_, s_),
    "-": (e_, w_),
    "L": (n_, e_),
    "J": (n_, w_),
    "7": (s_, w_),
    "F": (s_, e_),
}

def parse(text):
    lines = text.split("\n")[:-1]
    for r, line in enumerate(lines):
        c = line.find("S")
        if c != -1:
            return lines, Pos(r, c)

def get_start_direction(field, start):
    ds = []
    for d in dirs:
        pos = start + d
        char = field[pos.r][pos.c]
        if char == ".":
            continue
        if opposite[d] in connections[char]:
            ds.append(d)
    for char, (a, b) in connections.items():
        if [a,b] == ds or [b, a] == ds:
            return ds[0], char

def count_loop(field, start):
    last_dir, char = get_start_direction(field, start)
    cur = start + last_dir
    steps = 1
    while field[cur.r][cur.c] != "S":
        last_dir = dir_along(field, cur, last_dir)
        cur = cur + last_dir
        steps += 1
    return steps


def dir_along(field, pos, enter_dir):
    a, b = connections[field[pos.r][pos.c]]
    if a == opposite[enter_dir]:
        return b
    return a


def put_walls(nfield, r, c, char):
    cons = connections[char]
    nfield[3*r+1, 3*c+1] = WALL
    for delta in cons:
        nfield[3*r + delta.r + 1, 3*c + delta.c + 1] = WALL


EMPTY = 0
WALL = 1
def redraw(field, start):
    # 0 - empty
    # 1 - wall
    # pos %3 == 1 -> part of original field

    w = len(field[0])
    h = len(field)
    nfield = np.zeros((3*h, 3*w))

    last_dir, char = get_start_direction(field, start)
    put_walls(nfield, start.r, start.c, char)
    cur = start + last_dir
    char = field[cur.r][cur.c]
    while  char != "S":
        put_walls(nfield, cur.r, cur.c, char)
        last_dir = dir_along(field, cur, last_dir)
        cur = cur + last_dir
        char = field[cur.r][cur.c]
    return nfield

val_map = {
    0: " ",
    1: "#",
    2: ".",
}
def write_nfield(nfield, num=0):
    with open(f"nfield{num:03d}.txt", "w") as f:
        for line in nfield:
            f.write("".join(val_map[val] for val in line))
            f.write("\n")

def is_original(pos):
    return pos.r % 3 == 1 and pos.c % 3 == 1

def is_inside_nfield(nfield, pos):
    r, c = nfield.shape
    return 0 <= pos.r < r and 0 <= pos.c < c


def dfs(nfield, pos):
    orig_count = 0
    if is_original(pos):
        orig_count += 1
    nfield[pos.r, pos.c] = WALL
    for d in dirs:
        npos = pos+d
        if not is_inside_nfield(nfield, npos):
            # reached the edge
            orig_count = -1
            continue
        if nfield[npos.r, npos.c] == EMPTY:
            to_add = dfs(nfield, npos)
            if to_add == -1:
                orig_count = -1
            if orig_count != -1:
                orig_count += to_add
    return orig_count


def cont_inside_component(nfield):
    out = 0
    mr, mc = nfield.shape
    num_components = 0
    for r in range(mr):
        for c in range(mc):
            if nfield[r, c] == EMPTY:
                to_add = dfs(nfield, Pos(r, c))
                num_components += 1
                # print("comp", (nfield != WALL).sum())
                # write_nfield(nfield, num_components)
                if to_add != -1:
                    out += to_add
                    # print("inside")
    return out


def part1(text, timer):
    field, start = parse(text)
    timer.parsed()
    # print(start)
    count = count_loop(field, start)
    return count // 2

def part2(text, timer):
    field, start = parse(text)
    timer.parsed()
    nfield = redraw(field, start)
    # write_nfield(nfield)
    count = cont_inside_component(nfield)
    return count

task = Task(
    10,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark()

