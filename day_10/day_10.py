from itertools import product

with open('input') as input:
    data: list[list[str]] = input.read().splitlines()
    data: list[list[int]] = [[*map(int, line)] for line in data]

D = [(1, 0), (-1, 0), (0, 1), (0, -1)]
n, m = len(data), len(data[0])

def trailhead_destinations(data: list[list[int]], value: int, i: int, j: int):
    if not (0 <= i < len(data) and 0 <= j < len(data[0])) or data[i][j] != value:
        return set()
    elif value == 9:
        return {(i, j)}
    else:
        return set(destinations for x, y in D for destinations in trailhead_destinations(data, value+1, i+x, j+y))

def trailhead_rating(data: list[list[int]], value: int, i: int, j: int):
    if not (0 <= i < len(data) and 0 <= j < len(data[0])) or data[i][j] != value:
        return 0
    elif value == 9:
        return 1
    else:
        return sum(trailhead_rating(data, value+1, i+x, j+y) for x, y in D)

trailheads = sum(
    len(trailhead_destinations(data, 0, i, j))
    for i, j in product(range(n), range(m))
)

trailheads_ratings = sum(
    trailhead_rating(data, 0, i, j)
    for i, j in product(range(n), range(m))
)

with open('output', 'w') as output:
    output.write( str(trailheads) + '\n')
    output.write( str(trailheads_ratings) + '\n')