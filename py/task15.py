from task import Task

def parse(text):
    text = text.replace("\n", "")
    return text.split(",")

def rhash(text):
    cur = 0
    for c in text:
        cur += ord(c)
        cur *= 17
        cur %= 256
    return cur

def initialize_boxes(steps):
    boxes = [{} for _ in range(256)]
    for step in steps:
        if step.endswith("-"):
            name = step[:-1]
            box = boxes[rhash(name)]
            box.pop(name, None)
        else:
            name, fl = step.split("=")
            fl = int(fl)
            box = boxes[rhash(name)]
            box[name] = fl
    return boxes

def get_fcusing_power(boxes):
    s = 0
    for bn, box in enumerate(boxes):
        for sn, fl in enumerate(box.values()):
            s += (bn+1) * (sn+1) * fl
    return s

def part1(text, timer):
    steps = parse(text)
    timer.parsed()
    return sum(rhash(s) for s in steps)

def part2(text, timer):
    steps = parse(text)
    timer.parsed()
    boxes = initialize_boxes(steps)
    return get_fcusing_power(boxes)

task = Task(
    15,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark()

