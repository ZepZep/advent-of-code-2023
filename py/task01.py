from task import Task
import re

words = "one, two, three, four, five, six, seven, eight, nine".split(", ")

tr = {
    f"{i}": i for i in range(1, 10)
} | {
    word: i+1 for i, word in enumerate(words)
}

def get_with_re(text, re_num):
    re_single = re.compile(re_num)
    re_multi = re.compile(rf".*?({re_num}).*({re_num})")
    s = 0

    for line in text.split("\n"):
        if not line:
            continue

        m = re_multi.match(line)
        if m is not None:
            l = tr[m.group(1)]
            r = tr[m.group(2)]
        else:
            m = re_single.search(line)
            l = tr[m.group(0)]
            r = l

        s += l * 10 + r
    return s


re_num_p1 = r"[1-9]"
re_num_p2 = rf"{re_num_p1}|" + "|".join(words)

task = Task(
    1,
    lambda text: get_with_re(text, re_num_p1),
    lambda text: get_with_re(text, re_num_p2),
)

if __name__ == "__main__":
    task.run()
    task.benchmark(100)
