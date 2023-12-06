from task import Task
import math


def parse(text):
    l1, l2, _ = text.split("\n")
    _, *times = l1.split()
    _, *dists = l2.split()

    times = [int(x) for x in times]
    dists = [int(x) for x in dists]

    return times, dists

def parse2(text):
    l1, l2, _ = text.split("\n")
    time = int(l1.split(":")[1].replace(" ", ""))
    dist = int(l2.split(":")[1].replace(" ", ""))
    return time, dist

# DUMB
def get_margin(time, dist):
    ok = 0
    for speed in range(1, time):
        if speed * (time - speed) > dist:
            ok += 1
    return ok


# SMART
def solve_quad(a, b, c):
    d = b**2 - 4*a*c
    x1 = ( -b + d**0.5 ) / (2*a)
    x2 = ( -b - d**0.5 ) / (2*a)
    return x1, x2

def get_margin_smart(time, dist):
    # -1*speed**2 + time*speed -dist == 0
    x1, x2 = solve_quad(-1, time, -dist)
    start = math.ceil(x1)
    end = math.floor(x2)
    return end - start + 1


def part1(text, timer):
    times, dists = parse(text)
    timer.parsed()
    s = 1
    for time, dist in zip(times, dists):
        m1 = get_margin_smart(time, dist)
        s *= m1
    return s

def part2(text, timer):
    time, dist = parse2(text)
    timer.parsed()
    return get_margin_smart(time, dist)


task = Task(
    6,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark(1000)
