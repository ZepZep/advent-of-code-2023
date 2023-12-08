import time
import timeit
from inspect import signature
import os
import sys

class Task:
    def __init__(self, num, *part_fcns, test=False):
        self.part_fcns = part_fcns
        self.tasknum = num

        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        cur_dir = os.getcwd()
        if script_dir == cur_dir:
            prefix = "../"
        else:
            prefix = ""

        if not test:
            self.filename = f"{prefix}inputs/input{num:02d}.txt"
        else:
            self.filename = f"{prefix}inputs/test{num:02d}.txt"

    def time_and_run(self, f, part, output=True):
        timer = Timer()
        sig = signature(f)
        if len(sig.parameters) == 1:
            timer.start()
            result = f(self.text)
        else:
            timer.start()
            result = f(self.text, timer)
        timer.stop()
        if output:
            timer.summary(part, result)
        return timer

    def run(self):
        with open(self.filename) as f:
            self.text = f.read()

        for i, f in enumerate(self.part_fcns):
            self.time_and_run(f, i+1)

    def benchmark(self, repeats=10, header=True):
        with open(self.filename) as f:
            self.text = f.read()

        if header:
            print("\nBENCHMARK:")
        values = []
        for i, f in enumerate(self.part_fcns):
            timers = []
            for r in range(repeats):
                t = self.time_and_run(f, i+1, output=False)
                timers.append(t)
            values.extend(get_timers_summary(timers))
        print_bench_values(values, self.tasknum, header)


def mean(it):
    return sum(it) / len(it)


def get_timers_summary(timers):
    total = mean([(t.t_stop - t.t_start) * t.mul for t in timers])
    if timers[0].t_parsed:
        par = mean([(t.t_parsed - t.t_start) * t.mul for t in timers])
        exe = mean([(t.t_stop - t.t_parsed) * t.mul for t in timers])
        return total, par, exe
    return total, None, None


def print_bench_values(values, task, header=True, unit="ms", prec=" 7.3f", cell_len=15):
    if header:
        print("| task ", end="")
        for i in range(0, len(values), 3):
            print(f"| p{i//3+1} total [{unit}] | p{i//3+1} parse [{unit}] | p{i//3+1} exec [{unit}]  ", end="")
        print("|")

    res = [f"|  {task:02d}  |"]
    for v in values:
        if v:
            s = f"{v:{prec}}"
            res.append(f"{s:^{cell_len}}|")
        else:
            res.append(f"{'-':^{cell_len}}|")
    print("".join(res))


class Timer:
    def __init__(self):
        self.t_start = None
        self.t_parsed = None
        self.t_stop = None

        self.unit = "ms"
        self.mul = 1000
        self.prec = " 7.3f"

    def start(self):
        self.t_start = time.time()

    def parsed(self):
        self.t_parsed = time.time()

    def stop(self):
        self.t_stop = time.time()

    def summary(self, part, result):
        total = (self.t_stop - self.t_start) * self.mul
        print(f"part {part} [{total:{self.prec}} {self.unit}]: {str(result):<30}", end="")
        if self.t_parsed:
            par = (self.t_parsed - self.t_start) * self.mul
            exe = (self.t_stop - self.t_parsed) * self.mul
            frac = exe / total
            # print(f"    parsing:   {par:{self.prec}} {self.unit}  ({(1-frac)*100: 3.0f}%)")
            # print(f"    execution: {exe:{self.prec}} {self.unit}  ({frac*100: 3.0f}%)")
            print(f"  (execution: {frac*100: 3.0f}% [{exe:{self.prec}} {self.unit}])")
        else:
            print()

