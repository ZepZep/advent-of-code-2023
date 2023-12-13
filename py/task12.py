from task import Task

from tqdm import tqdm
from multiprocessing import Pool
from itertools import islice
import numpy as np


OK = 0
NOK = 1
UNK = 2

num_map = {
    ".": OK,
    "#": NOK,
    "?": UNK,
}

def parse(text):
    springs = []
    broken_lens = []
    for line in text.split("\n"):
        if not line:
            break
        s, nums = line.split(" ")
        s = [num_map[c] for c in s]
        nums = [int(n) for n in nums.split(",")]
        springs.append(s)
        broken_lens.append(nums)
    return springs, broken_lens

# ------ part 1
def can_place(spring, l, spos):
    if spos - l + 1 < 0:
        return False
    for i in range(l):
        if spring[spos-i] == OK:
            return False

    # left boundery
    if spos-l+1 != 0 and spring[spos-l] == NOK:
        return False

   # right boundery
    if spos+1 < len(spring) and spring[spos+1] == NOK:
        return False

    return True


def comb_dynamic_enter(args):
    spring, lens = args
    cache = {}
    res = comb_dynamic(spring, lens, len(spring)-1, len(lens)-1, cache)
    return res

def comb_dynamic(spring, lens, spos, lpos, cache):
    s = cache.get((spos, lpos))
    if s is not None:
        return s

    # Finished all lens
    if lpos == -1:
        if spos >= 0 and NOK in islice(spring, None, spos+1):
            cache[spos, lpos] = 0
            return 0
        cache[spos, lpos] = 1
        return 1
    l = lens[lpos]

    # accessing springs before start
    if spos < 0:
        if lpos == -1:
            cache[spos, lpos] = 1
            return 1
        cache[spos, lpos] = 0
        return 0

    # placing first len, check for NOK before
    if lpos == 0:
        if spos-l >= 0 and spring[spos] == NOK and NOK in islice(spring, None, spos-l+1):
            cache[spos, lpos] = 0
            return 0

    # placing last len, check for NOK after
    if lpos == len(lens)-1 and NOK in islice(spring, spos+1, None):
        cache[spos, lpos] = 0
        return 0

    s = 0
    if can_place(spring, l, spos):
        # decided to place
        s += comb_dynamic(spring, lens, spos-l-1, lpos-1, cache)

    # decided not to place, only if possible (not NOK)
    if spring[spos] != NOK:
        s += comb_dynamic(spring, lens, spos-1, lpos, cache)

    cache[spos, lpos] = s
    return s


# ------ part 2
def unfold(spring, lens, n):
    new_spring = []
    new_lens = []
    for i in range(n):
        new_spring.extend(spring)
        if i != n-1:
            new_spring.append(UNK)
        new_lens.extend(lens)
    return new_spring, new_lens


# ------ debug functions
s_map = {v:k for k, v in num_map.items()}

def spring2str(spring):
    return "".join(s_map[n] for n in spring)

def print_cache(cache, spring, lens):
    print(f"\n  {spring}  | {lens}")
    ncache = np.zeros((len(lens),len(spring)), dtype=np.int64) - 1
    for (c, r), val in cache.items():
        ncache[r, c] = val
    print(ncache)


# ------ parts
def part1(text, timer):
    springs, broken_lens = parse(text)
    timer.parsed()
    it = zip(springs, broken_lens)
    # it = tqdm(it, total=len(springs), desc="Bruteforcing")
    total = 0
    for s, l in it:
        cur = comb_dynamic_enter((s, l))
        total += cur
    return total

def part2(text, timer):
    springs, broken_lens = parse(text)
    timer.parsed()

    for i in range(len(springs)):
        springs[i], broken_lens[i] = unfold(springs[i], broken_lens[i], 5)

    it = zip(springs, broken_lens)
    with Pool(8) as pool:
        it = pool.imap_unordered(comb_dynamic_enter, it, 10)
        total = 0
        for cur, spring, lens in zip(it, springs, broken_lens):
            total += cur
    return total

task = Task(
    12,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark(10)

