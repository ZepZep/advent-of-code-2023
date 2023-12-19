from task import Task
import numpy as np
from astar import AStar
from dataclasses import dataclass
from itertools import islice


def parse(text):
    arr = np.frombuffer(bytes(text, "ascii"), dtype=np.uint8)
    width = arr.argmin()
    arr = arr.reshape((width, arr.shape[0]//width))[:, :-1]
    return arr - ord("0")

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

deltas = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]

dir_indicators = [
    ord("^"),
    ord(">"),
    ord("v"),
    ord("<"),
]

# num_dist = 0

@dataclass(frozen=True)
class Node:
    r: int
    c: int
    dir: int
    steps: int

    def __add__(self, other):
        return Pos(self.r + other.r, self.c+other.c)

    def __mul__(self, other):
        return Pos(self.r * other, self.c * other)

class CrucibleAStar(AStar):
    def __init__(self, arr, min_turn, max_turn):
        self.arr = arr
        self.mr, self.mc = arr.shape
        self.min_turn = min_turn
        self.max_turn = max_turn

    def yield_if_inside(self, node):
        if 0<=node.r<self.mr and 0<=node.c<self.mc:
            yield node


    def neighbors(self, node):
        if node.steps >= self.min_turn:
            # turn right
            ndir = (node.dir+1)%4
            dr, dc = deltas[ndir]
            yield from self.yield_if_inside(Node(node.r+dr, node.c+dc, ndir, 1))

            # turn left
            ndir = (node.dir-1)%4
            dr, dc = deltas[ndir]
            yield from self.yield_if_inside(Node(node.r+dr, node.c+dc, ndir, 1))

        if node.steps < self.max_turn:
            # go forward
            dr, dc = deltas[node.dir]
            yield from self.yield_if_inside(Node(node.r+dr, node.c+dc, node.dir, node.steps+1))


    def distance_between(self, n1, n2):

        return self.arr[n2.r, n2.c]

    def heuristic_cost_estimate(self, current, goal):
        return abs(current.r - goal.r) + abs(current.c - goal.c)
        return 0

    def is_goal_reached(self, current, goal):
        return current.r == goal.r and current.c == goal.c

def get_path_len(arr, path):
    s = 0
    for node in islice(path, 1, None):
        s += arr[node.r, node.c]
    return s

def print_path(arr, path):
    arr = arr + ord("0")
    for node in path:
        arr[node.r, node.c] = dir_indicators[node.dir]

    for line in arr:
        print("".join(chr(c) for c in line))


def part1(text, timer):
    arr = parse(text)
    timer.parsed()
    mr, mc = arr.shape
    path = CrucibleAStar(arr, 0, 3).astar(
        Node(0, 0, DOWN, 0),
        Node(mr-1, mc-1, 0, 0),
    )
    # print(list(path))
    # path = list(path)
    # print(path)
    # print(len(path))
    # print_path(arr, path)
    # print(num_dist)
    return get_path_len(arr, path)

def part2(text, timer):
    arr = parse(text)
    timer.parsed()
    mr, mc = arr.shape
    path = CrucibleAStar(arr, 4, 10).astar(
        Node(0, 0, DOWN, 0),
        Node(mr-1, mc-1, 0, 0),
    )
    # print(list(path))
    # path = list(path)
    # print(path)
    # print(len(path))
    # print_path(arr, path)
    # print(num_dist)
    return get_path_len(arr, path)

task = Task(
    17,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark(1)

