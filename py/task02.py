from task import Task
import re

indexes = {
    "red": 0,
    "green": 1,
    "blue": 2,
}

def parse_games(text):
    games = {}
    for line in text.split("\n"):
        if not line:
            continue
        m = re.match(r"Game ([0-9]+): (.*)", line)
        gid = int(m.group(1))
        game = []
        for subgame in m.group(2).split("; "):
            sg = [0 for _ in indexes]
            for colortext in subgame.split(", "):
                num, color = colortext.split(" ")
                sg[indexes[color]] += int(num)
            game.append(sg)
        games[gid] = game

    return games

def is_valid(game, limits):
    for sg in game:
        for num, lim in zip(sg, limits):
            if num > lim:
                return False
    return True

def sum_if_not_valid(games, limits):
    return sum(i for i, game in games.items() if is_valid(game, limits))

def mul(it):
    m = 1
    for n in it:
        m *= n
    return m

def min_power(game):
    mins = [0 for _ in indexes]
    for sg in game:
        for i, num in enumerate(sg):
            mins[i] = max(mins[i], num)
    return mul(mins)

def sum_min_powers(games):
    return sum(min_power(g) for g in games.values())


def part1(text, timer, limits):
    games = parse_games(text)
    timer.parsed()
    return sum_if_not_valid(games, limits)

def part2(text, timer):
    games = parse_games(text)
    timer.parsed()
    return sum_min_powers(games)


task = Task(
    2,
    lambda text, timer: part1(text, timer, [12, 13, 14]),
    lambda text, timer: part2(text, timer),
)

if __name__ == "__main__":
    task.run()
    task.benchmark(100)

