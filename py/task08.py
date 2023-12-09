from task import Task
import re
import math
import itertools


inster2index = {"L": 0, "R": 1}
STARTING = "AAA"
ENDING = "ZZZ"

def parse(text):
    lines = text.split("\n")

    instrs = lines[0]
    instrs = [inster2index[i] for i in instrs]
    nodes = {}

    re_line = re.compile(r"(...) = \((...), (...)\)")
    for line in lines[2:]:
        if not line:
            continue
        m = re_line.match(line)
        n, l, r = m.groups()
        nodes[n] = (l, r)

    return instrs, nodes


# PART 1
def follow(instrs, nodes):
    steps = 0
    cur = STARTING

    while True:
        for instr in instrs:
            cur = nodes[cur][instr]
            steps += 1
            if cur == ENDING:
                return steps


# PART 2
# ...e...|.e...e.
# 3, 9, 13, 17==9
# 3, 6 | 4, 4
def make_loopdef(ends, loop_start, loop_end_step):
    for i, (step, node) in enumerate(ends):
        if node == loop_start:
            start_end = i+1
            break
    last = 0
    deltas = []
    for step, node in ends:
        deltas.append(step - last)
        last = step
    deltas.append(loop_end_step - last)

    return deltas[:start_end], deltas[start_end:]

def get_loopdef(instrs, nodes, start):
    cache = {(start, 0): 0}
    steps = 0
    cur = start
    ends = []

    while True:
        for ic, instr in enumerate(instrs):
            cur = nodes[cur][instr]
            steps += 1

            if cur[-1] == "Z":
                if (cur, ic) in cache:
                    # print(f"  {cur} {ends}")
                    return make_loopdef(ends, cur, steps)
                ends.append((steps, cur))

                cache[cur, ic] = steps

def is_special(lds):
    for ld in lds:
        s, l = ld
        if len(s) != 1:
            return False
        if s != l:
            return False
    return True

# solves for a special case, where each gohost encounters only one end
# and ends in a loop that is the same length as the step of the first end.
# The input seems to be like this
def solve_part2_special(loopdefs):
    ms = [ld[0][0] for ld in loopdefs]
    return math.lcm(*ms)

# PART 2 general
def looper(loopdef):
    start, loop = loopdef
    return itertools.chain(start, itertools.cycle(loop))

def catchup(it, lv, target):
    while lv < target:
        # print(lv)
        lv += next(it)
    return lv, lv == target


def solve_part2_general(loopdefs):
    fst, *iters = [iter(looper(ld)) for ld in loopdefs]
    last_values = [0 for _ in iters]
    cur = 0
    while True:
        is_same = True
        cur += next(fst)
        for i, it in enumerate(iters):
            last_values[i], exact = catchup(it, last_values[i], cur)
            is_same &= exact
        if is_same:
            return cur


def part1(text, timer):
    instrs, nodes = parse(text)
    timer.parsed()
    return follow(instrs, nodes)

def part2(text, timer):
    instrs, nodes = parse(text)
    timer.parsed()
    starts = [n for n in nodes if n[-1] == "A"]
    lds = []
    for start in starts:
        ld = get_loopdef(instrs, nodes, start)
        lds.append(ld)
        # print(f"    {start} {ld}")

    if is_special(lds):
        return solve_part2_special(lds)
    print("iterations reduced by factor ~10000, but still takes ~12 minutes")
    return solve_part2_general(lds)

task = Task(
    8,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark(30)
