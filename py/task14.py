from task import Task
import numpy as np
from numba import jit, njit


ROLL  = 79
EMPTY = 46
STOP  = 35

# parse
def parse(text):
    arr = np.frombuffer(bytes(text, "ascii"), dtype=np.uint8)
    width = arr.argmin()
    arr =  arr.reshape((width, arr.shape[0]//width))[:, :-1]
    # return arr
    return np.pad(arr, pad_width=1, mode='constant',constant_values=STOP)

# part1
def get_iter(arr, dr, dc):
    mr, mc = arr.shape
    if dr == 1:
        return ((r, c) for c in range(mc) for r in range(mr))
    if dr == -1:
        return ((r, c) for c in range(mc) for r in range(mr-1, -1, -1))
    if dc == 1:
        return ((r, c) for r in range(mr) for c in range(mc))
    if dc == -1:
        return ((r, c) for r in range(mr) for c in range(mc-1, -1, -1))

@njit
def get_nb_iter(iters, dr, dc) -> np.array:
    if dr == 1:
        return iters[0]
    if dr == -1:
        return iters[1]
    if dc == 1:
        return iters[2]
    if dc == -1:
        return iters[3]

@njit
def get_roll_slice(r, c, dr, dc, gathered_rocks):
    if dr == 1:
        return r-gathered_rocks, r, c, c+1
    if dr == -1:
        return r+1, r+gathered_rocks+1, c, c+1
    if dc == 1:
        return r, r+1, c-gathered_rocks, c
    if dc == -1:
        return r, r+1, c+1, c+gathered_rocks+1

@njit
def roll_rocks(arr, dr, dc, iters):
    it = get_nb_iter(iters, dr, dc)

    gathered_rocks = 0
    for r, c in it:
        cur = arr[r, c]
        if cur == STOP:
            if gathered_rocks == 0:
                continue
            sr1, sr2, sc1, sc2 = get_roll_slice(r, c, dr, dc, gathered_rocks)
            arr[sr1:sr2, sc1:sc2] = ROLL
            gathered_rocks = 0
        elif cur == ROLL:
            gathered_rocks += 1
            arr[r, c] = EMPTY
    return arr

def load(arr, dr, dc):
    mr, mc = arr.shape
    if dr == 1:
        return ((arr == ROLL) * np.arange(mr)[:, None]).sum()
    if dr == -1:
        return ((arr == ROLL) * np.arange(mr)[::-1, None]).sum()
    if dc == 1:
        return ((arr == ROLL) * np.arange(mc)[None, :]).sum()
    if dc == -1:
        return ((arr == ROLL) * np.arange(mc)[None, ::-1]).sum()

# part 2
def cycle(arr, iters):
    for dr, dc in ((-1,0), (0,-1), (1,0), (0,1)):
        roll_rocks(arr, dr, dc, iters)

def skip_periodic(arr, N, prev, i, iters):
    remaining = N-i
    period = i - prev
    to_make = remaining % period
    for _ in range(to_make):
        cycle(arr, iters)

# debug
def print_arr(arr):
    print("\n".join(row.tobytes().decode() for row in arr))

# parts
def part1(text, timer):
    arr = parse(text)
    timer.parsed()
    iters = tuple(
        np.array(list(get_iter(arr, dr, dc)))
        for dr, dc in ((1,0), (-1,0), (0,1), (0,-1))
    )
    dr, dc = -1, 0
    arr = roll_rocks(arr, dr, dc, iters)
    return load(arr, dr, dc)


def part2(text, timer):
    arr = parse(text)
    timer.parsed()
    iters = tuple(
        np.array(list(get_iter(arr, dr, dc)))
        for dr, dc in ((1,0), (-1,0), (0,1), (0,-1))
    )
    N = 1000000000
    cache = {}
    cache[arr.tobytes()] = 0
    for i in range(N):
        cycle(arr, iters)
        i += 1
        rep = arr.tobytes()
        prev = cache.get(rep)
        if prev is not None:
            # print("hit", prev, i)
            skip_periodic(arr, N, prev, i, iters)
            break
        cache[rep] = i
    return load(arr, -1, 0)

task = Task(
    14,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark(10)

