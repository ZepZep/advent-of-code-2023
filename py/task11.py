from task import Task
import numpy as np

from numba import njit, jit

def parse(text):
    a = np.frombuffer(bytes(text, "ascii"), dtype=np.uint8)
    width = a.argmin()
    return a.reshape((width, a.shape[0]//width))[:, :-1]

def add_expansion(coords, missing, expand_by):
    prefix = np.zeros(coords.max()+1, dtype=int)
    prefix[list(missing)] = expand_by
    return coords + prefix.cumsum()[coords]

def get_expanded_positions(arr, expand_by):
    rs, cs = np.where(arr==ord("#"))
    mr, mc = arr.shape
    missing_rows = set(range(mr)) - set(rs)
    missing_cols = set(range(mc)) - set(cs)

    rs = add_expansion(rs, missing_rows, expand_by)
    cs = add_expansion(cs, missing_cols, expand_by)

    return rs, cs

@njit
def get_sum(mat):
    return np.abs(mat-mat.T).sum()//2

def sum_distances_one_axis(pos):
    mat = np.tile(pos, [pos.shape[0], 1])
    # print(np.abs(mat-mat.T))
    return get_sum(mat)


def part1(text, timer):
    arr = parse(text)
    timer.parsed()
    rs, cs = get_expanded_positions(arr, 1)
    s = sum_distances_one_axis(rs) + sum_distances_one_axis(cs)
    return s


def part2(text, timer):
    arr = parse(text)
    timer.parsed()
    rs, cs = get_expanded_positions(arr, 999999)
    s = sum_distances_one_axis(rs) + sum_distances_one_axis(cs)
    return s

task = Task(
    11,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark()

