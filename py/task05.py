from task import Task


def parse(text):
    seeds_s, *maps_s = text.split("\n\n")
    seeds = [int(s) for s in seeds_s[7:].split(" ")]

    maps = []
    for m in maps_s:
        curmap = []
        for line in m.split("\n")[1:]:
            if not line:
                continue
            curmap.append([int(s) for s in line.split(" ")])
        maps.append(curmap)

    return seeds, maps

# PART 1 functions
def get_mapping(value, cmap):
    for dst, src, l in cmap:
        if src <= value < src+l:
            return dst, src, l
    return None

def map_value(value, cmap):
    mapping = get_mapping(value, cmap)
    if mapping is None:
        return value
    dst, src, l = mapping
    offset = dst - src
    return value + offset

def map_multi(value, maps):
    for cmap in maps:
        value = map_value(value, cmap)
    return value


# PART 2 functions
def overlap(v, r, src, l):
    s1 = v
    e1 = v+r
    s2 = src
    e2 = src + l

    if l == 0 or e1 <= s2 or e2 <= s1:
        return None, None

    os = max(s1, s2)
    oe = min(e1, e2)

    return os, oe

def map_value_r(v, r, cmap):
    last_end = 0 # points after done part
    for dst, src, l in cmap:
        # catch up to src
        os, oe = overlap(v, r, last_end, src-last_end)
        if os is not None:
            # print("  catch ", os, oe - os)
            # print(f"      {v=} {r=} {os=} {oe=} {last_end=} {src=}")
            yield os, oe - os

        # actual interval
        os, oe = overlap(v, r, src, l)
        if os is not None:
            offset = dst - src
            # print("  actual", os + offset, oe - os)
            yield os + offset, oe - os

        # shift last_end
        last_end = src+l

    if v+r > last_end:
        # final catch up
        os, oe = overlap(v, r, last_end, v+r-last_end)
        if os is not None:
            # print("  catch ", os, oe - os)
            yield os, oe - os


def map_multi_r(vrs, maps):
    # print(vrs)
    for cmap in maps:
        new_vrs = []
        for v, r in vrs:
            new_vrs.extend(map_value_r(v, r, cmap))
        vrs = new_vrs
        # print(vrs)
    return vrs

def sort_maps(maps):
    return [ sorted(cmap, key=lambda x: x[1]) for cmap in maps ]


def part1(text, timer):
    seeds, maps = parse(text)
    timer.parsed()
    locations = [map_multi(s, maps) for s in seeds]
    return min(locations)

def part2(text, timer):
    seeds, maps = parse(text)
    timer.parsed()

    maps = sort_maps(maps)
    locations = []
    for i in range(len(seeds)//2):
        vr = (seeds[2*i], seeds[2*i+1])
        locations.extend(map_multi_r([vr], maps))
    return min(a for a, _ in locations)


task = Task(
    5,
    lambda text, timer: part1(text, timer),
    lambda text, timer: part2(text, timer),
    # test=True,
)


if __name__ == "__main__":
    task.run()
    task.benchmark(100)
