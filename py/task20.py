from task import Task
from dataclasses import dataclass
from collections import deque, defaultdict
import math

@dataclass
class Message:
    dst: str
    src: str
    pulse: bool


class Module:
    def __init__(self, name, bus, destinations):
        self.name = name
        self.bus = bus
        self.destinations = destinations
        self.initialize()
        self.inputs = {}

    def initialize(self):
        pass

    def add_input(self, name):
        self.inputs[name] = False

    def send(self, pulse):
        for dst in self.destinations:
            self.bus.send(Message(dst, self.name, pulse))

    def dot_name(self):
        return f"{self.name}"
    def dot_node(self):
        return f"{self.dot_name()}"

class FlipFlop(Module):
    def initialize(self):
        self.state = False

    def handle(self, msg):
        if msg.pulse:
            return
        self.state = not self.state
        self.send(self.state)

    def dot_name(self):
        return f"F_{self.name}"

    def dot_node(self):
        return f"{self.dot_name()}[style=filled,color=red]"


last_high = {}

class Conjunctor(Module):
    def handle(self, msg):
        self.inputs[msg.src] = msg.pulse

        all_high = all(self.inputs.values())
        if all_high:
            if self.name in ["qx", "db", "gf", "vc"]:
                if self.name in last_high:
                    print(self.name, n - last_high[self.name])
                last_high[self.name] = n
        self.send( not all_high )

    def dot_name(self):
        return f"C_{self.name}"

    def dot_node(self):
        return f"{self.dot_name()}[style=filled,color=blue]"


class Broadcaster(Module):
    def handle(self, msg):
        self.send(msg.pulse)


class Bus:
    def __init__(self):
        self.modules = None
        self.queue = deque()
        self.counter = defaultdict(int)
        self.rx_on = False

    def press(self):
        self.send(Message("broadcaster", "button", False))

        while self.queue:
            self.process_one()

    def send(self, msg):
        self.counter[msg.pulse] += 1
        self.queue.append(msg)

        if msg.dst == "rx" and msg.pulse == False:
            self.rx_on = True

    def process_one(self):
        msg = self.queue.popleft()
        module = self.modules.get(msg.dst)
        if module is not None:
            module.handle(msg)

    def print_dot(self):
        for module in self.modules.values():
            print(module.dot_node())
            for dst in module.destinations:
                dst_module = self.modules.get(dst)
                if dst_module is None:
                    print(f"{module.dot_name()} -> {dst}")
                else:
                    print(f"{module.dot_name()} -> {dst_module.dot_name()}")


def parse(text):
    modules = {}
    bus = Bus()

    for line in text.splitlines():
        l, r = line.split(" -> ")
        destinations = r.split(", ")

        if l == "broadcaster":
            modules["broadcaster"] = Broadcaster("broadcaster", bus, destinations)
        elif l.startswith("%"):
            name = l[1:]
            modules[name] = FlipFlop(name, bus, destinations)
        elif l.startswith("&"):
            name = l[1:]
            modules[name] = Conjunctor(name, bus, destinations)

    for name, module in modules.items():
        for dst in module.destinations:
            dst_module = modules.get(dst)
            if dst_module is not None:
                dst_module.add_input(name)

    bus.modules = modules
    return bus


def part1(text, timer):
    bus = parse(text)
    timer.parsed()
    # bus.print_dot()
    for _ in range(1000):
        bus.press()
    return bus.counter[False] * bus.counter[True]

# meh...
def part2(text, timer):
    bus = parse(text)
    timer.parsed()
    global n
    n = 0
    last_high.clear()
    while not bus.rx_on:
        n += 1
        bus.press()
        if len(last_high) == 4:
            # 3923, 4027, 3739, 3793
            return math.lcm(*last_high.values())
    return n

task = Task(
    20,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark()

