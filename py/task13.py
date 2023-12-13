from task import Task


def parse(text):
    patterns = []
    for p in text.split("\n\n"):
        rows = p.splitlines()
        cols = ["".join(cs) for cs in zip(*rows)]
        patterns.append((rows, cols))
    return patterns


def n_differences(a, b, smudges):
    diff = 0
    for ac, bc in zip(a, b):
        if ac != bc:
            diff += 1
            if diff > smudges:
                return diff
    return diff

def is_reflected_at(pat, pos, smudges=0):
    limit = min(pos+1, len(pat)-pos-1)
    # print(pos, len(pat), limit)
    for i in range(limit):
        a = pat[pos-i]
        b = pat[pos+1+i]
        if a != b:
            if smudges == 0:
                return False
            smudges -= n_differences(a, b, smudges)
        if smudges < 0:
            return False
    return smudges == 0

def get_reflection_pos(pat, smudges=0):
    for pos in range(0, len(pat)-1):
        if is_reflected_at(pat, pos, smudges):
            return pos + 1
    return 0


def part1(text, timer):
    patterns = parse(text)
    timer.parsed()
    s = 0
    for rows, cols in patterns:
        s += get_reflection_pos(cols)
        s += 100 * get_reflection_pos(rows)
    return s

def part2(text, timer):
    patterns = parse(text)
    timer.parsed()
    smudges = 1
    s = 0
    for rows, cols in patterns:
        s += get_reflection_pos(cols, smudges)
        s += 100 * get_reflection_pos(rows, smudges)
    return s

task = Task(
    13,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark(100)

