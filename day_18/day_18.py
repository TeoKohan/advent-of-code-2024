import re
from collections import deque
from typing import Self
from vector2 import Vector2

with open('input') as input:
    obstacles = input.read().splitlines()
    obstacles = [Vector2(*map(int, re.findall(r'\d+', obstacle))) for obstacle in obstacles]

class Node():

    def __init__(self, position: Vector2, parent: None | Self):
        self.position: Vector2 = position
        self.parent: None | Self = parent
    
    def length(self):
        if self.parent:
            return 1 + self.parent.length()
        else:
            return 0

def solve_path(board: list[list[str]], start: Vector2, end: Vector2) -> None | Node:
    visited: set[tuple[int, int]] = set()
    to_do: deque[tuple[Vector2, int]] = deque([Node(start, None)])

    while to_do:
        current: Node = to_do.popleft()
        if tuple(current.position) in visited:
            pass
        elif current.position == end:
            return current
        else:
            visited.add(tuple(current.position))
            for v in [current.position + direction for direction in Vector2.orthogonal()]:
                if 0 <= v.x < len(board[0]) and 0 <= v.y < len(board) and not tuple(v) in visited and tuple(v) and board[v.x][v.y] != '#':
                    to_do.append( Node(v, current) )
    return None

def solve(width: int, height: int, obstacles: list[Vector2], start: Vector2, end: Vector2) -> None | Node:

    board: list[list[str]] = [['.'] * width for _ in range(height)]
    for p in obstacles:
        board[p.y][p.x] = '#'

    return solve_path(board, start, end)

def find_block(width: int, height: int, obstacles: list[Vector2], start: Vector2, end: Vector2) -> int:

    left  = 0
    right = len(obstacles)

    while right - left > 1:
        midpoint = (left + right) // 2
        if solve(width, height, obstacles[:midpoint], start, end):
            left = midpoint
        else:
            right = midpoint
    
    return obstacles[right-1]

with open('output', 'w') as output:
    output.write( str(solve(71, 71, obstacles[:1024], Vector2.zero(), Vector2.one() * 70).length()) + '\n')
    output.write( ','.join(map(str, find_block(71, 71, obstacles, Vector2.zero(), Vector2.one() * 70))) + '\n')