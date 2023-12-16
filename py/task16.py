from task import Task
import numpy as np

from numba import jit, njit, prange, threading_layer, config
config.THREADING_LAYER = 'threadsafe'

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3

EMPTY = ord(".")
MTL = ord("\\")
MTR = ord("/")
SPLITH = ord("-")
SPLITV = ord("|")

deltas = np.array([
    [-1, 0, 1, 0],
    [0, -1, 0, 1],
    [1,  2, 4, 8],
], dtype=int).T

MTL_DELTAS = np.array([
    [*deltas[LEFT][:2], LEFT],
    [*deltas[UP][:2], UP],
    [*deltas[RIGHT][:2], RIGHT],
    [*deltas[DOWN][:2], DOWN],
], dtype=int)

MTR_DELTAS = np.array([
    [*deltas[RIGHT, :2], RIGHT],
    [*deltas[DOWN, :2], DOWN],
    [*deltas[LEFT, :2], LEFT],
    [*deltas[UP, :2], UP],
], dtype=int)


def parse(text):
    arr = np.frombuffer(bytes(text, "ascii"), dtype=np.uint8)
    width = arr.argmin()
    arr =  arr.reshape((width, arr.shape[0]//width))[:, :-1]
    return arr

@njit
def add_if_inside(arr, stack, spos, r, c, dir):
    mr, mc = arr.shape
    if 0 <= r < mr and 0 <= c < mc:
        stack[spos, :] = [r, c, dir]
        spos += 1
    return spos


# def move(cell, r, c, dr, dc, stack, spos)
@njit
def energize(arr, r, c, dir):
    energy = np.zeros(arr.shape, dtype=np.int32)
    stack = np.zeros((10000, 3), dtype=np.int32)
    spos = 1 # first is already 0, 0
    stack[0, ] = [r, c, dir]

    while spos > 0:
        r, c, dir = stack[spos-1, :]
        spos -= 1
        # print(r,c, dir)
        dr, dc, dir_e  = deltas[dir, :]
        if energy[r,c] & dir_e:
            continue
        energy[r,c] |= dir_e

        cell = arr[r, c]

        if cell == EMPTY:
            spos = add_if_inside(arr, stack, spos, r+dr, c+dc, dir)
        elif cell == MTL:
            dr, dc, ndir = MTL_DELTAS[dir]
            # print("TL", dir, dr, dc)
            spos = add_if_inside(arr, stack, spos, r+dr, c+dc, ndir)
        elif cell == MTR:
            dr, dc, ndir = MTR_DELTAS[dir]
            spos = add_if_inside(arr, stack, spos, r+dr, c+dc, ndir)
        elif cell == SPLITH:
            if dir == UP or dir == DOWN:
                dr, dc, _ = deltas[LEFT]
                spos = add_if_inside(arr, stack, spos, r+dr, c+dc, LEFT)
                dr, dc, _ = deltas[RIGHT]
                spos = add_if_inside(arr, stack, spos, r+dr, c+dc, RIGHT)
            else:
                spos = add_if_inside(arr, stack, spos, r+dr, c+dc, dir)
        elif cell == SPLITV:
            if dir == LEFT or dir == RIGHT:
                dr, dc, _ = deltas[UP]
                spos = add_if_inside(arr, stack, spos, r+dr, c+dc, UP)
                dr, dc, _ = deltas[DOWN]
                spos = add_if_inside(arr, stack, spos, r+dr, c+dc, DOWN)
            else:
                spos = add_if_inside(arr, stack, spos, r+dr, c+dc, dir)
        else:
            print("Bad cell", repr(cell))

    return energy

@njit
def get_n_energized(arr, r, c, dir):
    energy = energize(arr, r, c, dir)
    return (energy > 0).sum()

@njit(parallel=True)
def energize_max(arr):
    out = 0
    mr, mc = arr.shape

    for r in prange(mr):
        cur = get_n_energized(arr, r, 0, RIGHT)
        out = max(out, cur)

        cur = get_n_energized(arr, r, mc-1, LEFT)
        out = max(out, cur)


    for c in prange(mc):
        cur = get_n_energized(arr, 0, c, DOWN)
        out = max(out, cur)

        cur = get_n_energized(arr, mr-1, c, UP)
        out = max(out, cur)

    return out


def part1(text, timer):
    arr = parse(text)
    timer.parsed()
    return get_n_energized(arr, 0, 0, RIGHT)


def part2(text, timer):
    arr = parse(text)
    timer.parsed()
    return energize_max(arr)

task = Task(
    16,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark(100)

