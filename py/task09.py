from task import Task
from io import StringIO
import numpy as np

def parse(text):
    c = StringIO(text)
    return np.loadtxt(c, dtype=int)

def diffs_np(seqs):
    cur = seqs
    diffs =[seqs]
    for _ in range(seqs.shape[1] - 1):
        cur = np.diff(cur, axis=1)
        diffs.append(cur)
    return diffs

def predict_next(diffs):
    return np.sum([diff[:, -1] for diff in diffs])

# slightly slower (30 µs) than reversing the sequences and using predict_next
def predict_prev(diffs):
    return np.sum([diff[:, 0] * (-1)**(i)  for i, diff in enumerate(diffs)])

def part1(text, timer):
    seqs = np.array(parse(text))
    timer.parsed()
    diffs = diffs_np(seqs)
    return predict_next(diffs)

def part2(text, timer):
    seqs = np.array(parse(text))
    timer.parsed()
    diffs = diffs_np(seqs[:, ::-1])
    return predict_next(diffs)

task = Task(
    9,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark(100)

