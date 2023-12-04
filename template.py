from task import Task


def part1(text, timer):
    timer.parsed()
    return None

def part2(text, timer):
    timer.parsed()
    return None

task = Task(
    TASK_NUM,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    # task.benchmark()

