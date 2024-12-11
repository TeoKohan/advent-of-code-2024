from vector2 import Vector2
from itertools import product
from collections import defaultdict

with open('input') as input:
    data: list[list[str]] = input.read().splitlines()
    data: list[list[int]] = list(map(list, data))
    width: int = len(data)
    height: int = len(data[0])

    antennas: dict[Vector2, set] = defaultdict(set)
    for i, j in product(range(width), range(height)):
        if data[i][j] != '.':
            antennas[data[i][j]].add(Vector2(i, j))

def simple_antinodes(antennas: dict[Vector2, set], width: int, height: int) -> set[Vector2]:
    antinodes = set()
    for ant_A, ant_B in ((ant_A, ant_B) for antenna in antennas for ant_A, ant_B in product(antennas[antenna], antennas[antenna]) if ant_A != ant_B):
        antinode_a = 2 * ant_A - ant_B
        antinode_b = 2 * ant_B - ant_A
        antinodes.update([antinode_a, antinode_b])
    return set([node for node in antinodes if 0 <= node.x < height and 0 <= node.y < width])

def complex_antinodes(antennas: dict[Vector2, set], width: int, height: int) -> set[Vector2]:

    def propagate(origin: Vector2, direction: Vector2, width: int, height: int) -> set[Vector2]:
        result = set()
        while 0 <= origin.x < height and 0 <= origin.y < width:
            result.add(origin)
            origin += direction
        return result

    antinodes = set()
    for ant_A, ant_B in ((ant_A, ant_B) for antenna in antennas for ant_A, ant_B in product(antennas[antenna], antennas[antenna]) if ant_A != ant_B):
            antinode_direction = ant_A - ant_B
            antinodes.update(propagate(ant_A,  antinode_direction, width, height))
            antinodes.update(propagate(ant_B, -antinode_direction, width, height))
    return antinodes

with open('output', 'w') as output:
    output.write( str(len(simple_antinodes (antennas, width, height))) + '\n')
    output.write( str(len(complex_antinodes(antennas, width, height))) + '\n')