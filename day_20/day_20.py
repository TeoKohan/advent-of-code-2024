from typing import Self
from collections import deque, defaultdict
from itertools import product
from vector2 import Vector2

with open('input') as input:
    maze: list[str] = input.read().splitlines()
    maze: list[list[str]] = [*map(list, maze)]
    height, width = len(maze), len(maze[0])
    start = next(Vector2(i, line.index('S')) for i, line in enumerate(maze) if 'S' in line)
    end   = next(Vector2(i, line.index('E')) for i, line in enumerate(maze) if 'E' in line)

class Node():

    def __init__(self, position: Vector2, parent: None | Self):
        self.position: Vector2   = position
        self.parent: None | Self = parent
        self.start_distance: None | int  = None
        self.end_distance: None | int  = None
    
    def set_start_distance(self, length: int):
        current: Node = self
        while current:
            current.start_distance = length
            current = current.parent
            length -= 1
    
    def set_end_distance(self, length: int):
        current: Node = self
        while current:
            current.end_distance = length
            current = current.parent
            length += 1

def print_board(board: list[list[str]]):
    print(
        '\n'.join(
            ''.join(letter for letter in line) for line in board
        )
    )

def fill_path(M: dict[tuple[int, int], Node], maze: list[list[str]], start: Vector2) -> None | Node:
    visited: set[tuple[int, int]] = set()
    to_do: deque[tuple[Vector2, int]] = deque([Node(start, None)])

    while to_do:
        current: Node = to_do.popleft()
        M[tuple(current.position)] = current

        if not tuple(current.position) in visited:
            visited.add(tuple(current.position))
            for v in [current.position + direction for direction in Vector2.orthogonal()]:
                if 0 <= v.y < len(maze[0]) and 0 <= v.x < len(maze) and not tuple(v) in visited and tuple(v) and maze[v.x][v.y] != '#':
                    to_do.append( Node(v, current) )
    return M

M: dict[tuple[int, int], Node] = fill_path(dict(), maze, start)

M[tuple(end)].set_end_distance(0)
M[tuple(end)].set_start_distance(M[tuple(start)].end_distance)
full_distance = M[tuple(end)].start_distance

def cheat_paths_filter(M: dict[tuple[int, int], Node], cheat_distance: int) -> None | Node:

    result: defaultdict[int, int] = defaultdict(lambda: 0)

    for u, v in ((u, v) for u, v in product(M, repeat=2) if M[u].start_distance < M[v].start_distance):
        distance_between_nodes: Vector2 = Vector2.taxicab_distance(Vector2(*u), Vector2(*v))
        if distance_between_nodes <= cheat_distance:
            distance = M[u].start_distance + distance_between_nodes + M[v].end_distance
            distance_delta = full_distance - distance
            result[distance_delta] += distance_delta >= 0
    
    return sum(v for k, v in result.items() if k >= 100)

with open('output', 'w') as output:
    output.write( str(cheat_paths_filter(M,  2)) + '\n')
    output.write( str(cheat_paths_filter(M, 20)) + '\n')