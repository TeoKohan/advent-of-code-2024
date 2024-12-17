import sys
from math import inf
from collections import defaultdict
from vector2 import Vector2

type FVector2 = tuple[int, int]
sys.setrecursionlimit(15000)

mov_cost = 1
rot_cost = 1000

with open('input') as input:
    maze: list[str] = input.read().splitlines()
    maze: list[list[str]] = [*map(list, maze)]
    height, width = len(maze), len(maze[0])
    start = next(Vector2(line.index('S'), i) for i, line in enumerate(maze) if 'S' in line)
    end   = next(Vector2(line.index('E'), i) for i, line in enumerate(maze) if 'E' in line)


def to_tuple(reindeer: Vector2, direction: Vector2) -> tuple[FVector2, FVector2]:
    return tuple(reindeer), tuple(direction)

reindeer = Vector2(*start)
solutions: defaultdict[tuple[FVector2, FVector2], int] = defaultdict(lambda: inf)

def flood(M: dict[tuple[FVector2, FVector2], int], maze: list[list[str]], end: Vector2):
    M |= {(tuple(end), tuple(direction)): 0 for direction in Vector2.orthogonal()}
    to_consider: set[tuple[FVector2, FVector2]] = {to_tuple(end, direction) for direction in Vector2.orthogonal()}

    while to_consider:
        position, direction = to_consider.pop()
        position, direction = Vector2(*position), Vector2(*direction)
        state = to_tuple(position, direction)
        cost = M[state]
        while   (position := position - direction) and\
                0 <= position.x < width and 0 <= position.y < height and\
                maze[position.y][position.x] != '#':
            cost += 1
            if cost < M[to_tuple(position, direction)]:
                to_consider.add(to_tuple(position, direction))
                M[to_tuple(position, direction)] = cost
            if cost + rot_cost < M[to_tuple(position, direction.rotated_clockwise())]:
                to_consider.add(to_tuple(position, direction.rotated_clockwise()))
                M[to_tuple(position, direction.rotated_clockwise()        )] = cost + rot_cost
            if cost + rot_cost < M[to_tuple(position, direction.rotated_counter_clockwise())]:
                to_consider.add(to_tuple(position, direction.rotated_counter_clockwise()))
                M[to_tuple(position, direction.rotated_counter_clockwise())] = cost + rot_cost

def best_tiles(M: dict[tuple[FVector2, FVector2], int], maze: list[list[str]], start: Vector2):
    solution: set[tuple[int, int]] = set()
    to_consider: set[tuple[FVector2, FVector2]] = {to_tuple(start, Vector2(1, 0))}

    while to_consider:
        position, direction = to_consider.pop()
        position, direction = Vector2(*position), Vector2(*direction)
        solution.add(tuple(position))
        cost = M[to_tuple(position, direction)]
        if M[to_tuple(position+direction, direction)] == cost - mov_cost:
            to_consider.add(to_tuple(position+direction, direction))
        if M[to_tuple(position, direction.rotated_clockwise())] == cost - rot_cost:
            to_consider.add(to_tuple(position, direction.rotated_clockwise()))
        if M[to_tuple(position, direction.rotated_counter_clockwise())] == cost - rot_cost:
            to_consider.add(to_tuple(position, direction.rotated_counter_clockwise()))
    
    return solution

flood(solutions, maze, end)

with open('output', 'w') as output:
    output.write( str(solutions[to_tuple(start, Vector2(1, 0))]) + '\n')
    output.write( str(len(best_tiles(solutions, maze, start))) + '\n')