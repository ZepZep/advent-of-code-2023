from task import Task
import re

def parse_numbers(numbers):
    return [int(n) for n in re.split(r"\s+", numbers.strip())]

def get_cards(text):
    cards = []
    for line in text.split("\n"):
        if not line:
            continue

        m = re.match(r".*: (.*) \| (.*)", line)
        cards.append((
            parse_numbers(m.group(1)),
            parse_numbers(m.group(2))
        ))
    return cards

def count_points(n1, n2):
    intersection = set(n1).intersection(n2)
    if len(intersection) == 0:
        return 0
    return 2 ** (len(intersection) - 1)

def add_scratchcards(cards, cardnums, i):
    n1, n2 = cards[i]
    intersection = set(n1).intersection(n2)
    curnum = cardnums[i]
    for j in range(i+1, min(i+1+len(intersection), len(cards))):
        cardnums[j] += curnum


def part1(text, timer):
    cards = get_cards(text)
    timer.parsed()
    points = 0
    for n1, n2 in cards:
        points += count_points(n1, n2)
    return points

def part2(text, timer):
    cards = get_cards(text)
    timer.parsed()
    points = 0
    cardnums = [1 for _ in cards]
    for i in range(len(cards)):
        add_scratchcards(cards, cardnums, i)
    return sum(cardnums)

task = Task(
    4,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True
)

if __name__ == "__main__":
    task.run()
    task.benchmark(100)

