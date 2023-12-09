from task import Task
import numpy as np


def parse(text):
    seqs = []
    for line in text.split("\n"):
        if not line:
            continue
        seqs.append([int(v) for v in line.split(" ")])
    return seqs

def is_zeros(seq):
    for i in seq:
        if i != 0:
            return False
    return True

def get_diffs(seq):
    diffs = [seq]
    curseq = seq

    while True:
        nextseq = []
        for i in range(len(curseq)-1):
            nextseq.append(curseq[i+1] - curseq[i])
        diffs.append(nextseq)
        curseq = nextseq
        if is_zeros(nextseq):
            break

    return diffs

def apply_diffs(diffs):
    cur = 0
    for diff in reversed(diffs):
        cur = diff[-1] + cur
    return cur

def apply_diffs_back(diffs):
    cur = 0
    for diff in reversed(diffs):
        cur = diff[0] - cur
    return cur


def part1(text, timer):
    seqs = parse(text)
    timer.parsed()
    s = 0
    for seq in seqs:
        diffs = get_diffs(seq)
        pred = apply_diffs(diffs)
        s += pred
    return s

def part2(text, timer):
    seqs = parse(text)
    print(seqs)

    timer.parsed()
    s = 0
    for seq in seqs:
        diffs = get_diffs(seq)
        pred = apply_diffs_back(diffs)
        s += pred
    return s


# NUMPY solution
def diffs_np(seqs):
    cur = seqs
    diffs =[seqs]
    for _ in range(seqs.shape[1] - 1):
        cur = np.diff(cur, axis=1)
        diffs.append(cur)
    return diffs

def solve_np_1(diffs):
    return np.sum([diff[:, -1] for diff in diffs])

def solve_np_2(diffs):
    return np.sum([diff[:, 0] * (-1)**(i)  for i, diff in enumerate(diffs)])

def part1_np(text, timer):
    seqs = np.array(parse(text))
    timer.parsed()
    diffs = diffs_np(seqs)
    return solve_np_1(diffs)

def part2_np(text, timer):
    seqs = np.array(parse(text))
    timer.parsed()
    diffs = diffs_np(seqs)
    return solve_np_2(diffs)

task = Task(
    9,
    # lambda text, timer: part1(text, timer),
    # lambda text, timer: part2(text, timer),
    lambda text, timer: part1_np(text, timer),
    lambda text, timer: part2_np(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark(100)

