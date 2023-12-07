from task import Task

def parse(text):
    hands = []
    for line in text.split("\n"):
        if not line:
            continue
        h, b = line.split(" ")
        hands.append((h, int(b)))
    return hands


suit_index = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, 'T': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}

suit_index_j = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, 'T': 8, 'J': -1, 'Q': 10, 'K': 11, 'A': 12}

def card_counts(hand):
    counts = [0 for _ in suit_index]
    for c in hand:
        counts[suit_index[c]] += 1
    return counts

# 7 Five of a kind
# 6 Four of a kind
# 5 Full house  23332
# 4 Three of a kind
# 3 Two pair
# 2 One pair
# 1 High card
def extract_type(hand):
    counts = card_counts(hand)
    if 5 in counts:
        return 7
    if 4 in counts:
        return 6
    if 3 in counts and 2 in counts:
        return 5
    if 3 in counts:
        return 4
    if counts.count(2) == 2:
        return 3
    if 2 in counts:
        return 2
    return 1

def extract_type_j(hand):
    counts = card_counts(hand)
    scounts = [ (c, s) for c, s in sorted(zip(counts, suit_index.keys()), reverse=True)
               if s != "J" ]
    # print(scounts)

    j = counts[suit_index["J"]]
    fm, fs = scounts[0] if len(scounts) >= 1 else (0, None)
    sm, ss = scounts[1] if len(scounts) >= 2 else (0, None)
    # print(hand, fm, sm, j, scounts)

    if fm + j == 5:
        return 7
    if fm + j == 4:
        return 6
    if fm + sm + j == 5:
        return 5
    if fm + j == 3:
        return 4
    if fm + sm + j == 4:
        return 3
    if fm + j == 2:
        return 2
    return 1

def hand_tuple(hand, si):
    return tuple(si[c] for c in hand)

def part1(text, timer):
    hands = parse(text)
    timer.parsed()
    hands = [(extract_type(hand), hand_tuple(hand, suit_index), b) for hand, b in hands]
    s = 0
    for i, (t, tup, b) in enumerate(sorted(hands)):
        # print(f"{i+1}  {t} {tup}")
        s += (i+1) * b
    return s

def part2(text, timer):
    hands = parse(text)
    timer.parsed()
    hands = [(extract_type_j(hand), hand_tuple(hand, suit_index_j), b) for hand, b in hands]
    s = 0
    for i, (t, tup, b) in enumerate(sorted(hands)):
        # print(f"{i+1} {hand} {t} {tup}")
        s += (i+1) * b
    return s

task = Task(
    7,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)

if __name__ == "__main__":
    task.run()
    task.benchmark(50)

