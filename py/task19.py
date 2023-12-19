from task import Task
from dataclasses import dataclass
from copy import deepcopy

@dataclass
class Condition:
    key: str
    cmp: str
    val: int

    def evaluate(self, part):
        if self.key == "_":
            return True
        if self.cmp == "<":
            return part[self.key] < self.val
        return part[self.key] > self.val


def parse(text):
    rs, ps = text.split("\n\n")
    return parse_rules(rs), parse_parts(ps)

def get_rule_validator(constraint):
    key = constraint[0]
    cmp = constraint[1]
    val = int(constraint[2:])
    return Condition(key, cmp, val)

always = Condition("_", "=", 0)

# gv{a>1626:A,x<2292:R,a<1391:R,R}
def parse_rules(rs):
    rules = {}
    for line in rs.splitlines():
        name, rest = line.split("{")
        rule = []
        for part in rest[:-1].split(","):
            if ":" in part:
                constraint, send = part.split(":")
                rule.append((get_rule_validator(constraint), send))
            else:
                rule.append((always, part))
        rules[name] = rule
    return rules

# {x=2154,m=1989,a=788,s=417}
def parse_parts(ps):
    parts = []
    for line in ps.splitlines():
        line = line[1:-1]
        part = {}
        for pp in line.split(","):
            name, val = pp.split("=")
            part[name] = int(val)
        parts.append(part)
    return parts


# PART 1
def follow_rules(rules, part, curname):
    while True:
        if curname == "A":
            return True
        if curname == "R":
            return False

        for cond, nrule in rules[curname]:
            if cond.evaluate(part):
                curname = nrule
                break


# PART 2
def margins_from_cond(margins, cond):
    if cond.key == "_":
        return margins, None

    m_ok = deepcopy(margins)
    m_nok = deepcopy(margins)
    if cond.cmp == "<":
        m_ok[cond.key][1]  = min(cond.val, m_ok[cond.key][1] )
        m_nok[cond.key][0] = max(cond.val, m_nok[cond.key][0])
    else:
        m_ok[cond.key][0]  = max(cond.val+1, m_ok[cond.key][0] )
        m_nok[cond.key][1] = min(cond.val+1, m_nok[cond.key][1])

    if m_ok[cond.key][0] >= m_ok[cond.key][1]:
        m_ok = None
    if m_nok[cond.key][0] >= m_nok[cond.key][1]:
        m_nok = None

    return m_ok, m_nok

def mul(it):
    out = 1
    for v in it:
        out *= v
    return out



def search_all(rules, margins, cur):
    if cur == "R":
        return 0
    if cur == "A":
        val = mul(v2-v1 for v1, v2 in margins.values())
        return val

    accepting = 0
    for cond, nrule in rules[cur]:
        m_ok, m_nok = margins_from_cond(margins, cond)
        if m_ok:
            accepting += search_all(rules, m_ok, nrule)
        if not m_nok:
            break
        margins = m_nok
    return accepting


def part1(text, timer):
    rules, parts = parse(text)
    timer.parsed()

    total = 0
    for part in parts:
        if follow_rules(rules, part, "in"):
            total += sum(part.values())
    return total

def part2(text, timer):
    rules, parts = parse(text)
    timer.parsed()
    return search_all(rules, {k: [1, 4001] for k in "xmas"}, "in")

task = Task(
    19,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark(50)

