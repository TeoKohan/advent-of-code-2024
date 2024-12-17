from vector2 import Vector2

with open('input') as input:
    data = input.read().splitlines()
    data = list(map(list, data))
    n, m = len(data), len(data[0])
    guard = next(Vector2(line.index('^'), i) for i, line in enumerate(data) if '^' in line)
    data[guard.y][guard.x] = '.'

def get_path(data: list[list[str]], guard: Vector2) -> set[tuple[int, int]]:
    direction: Vector2 = Vector2(0, -1)
    visited = set()

    while 0 <= guard.x < m and 0 <= guard.y < n:
        visited.add(tuple(guard))
        
        x, y = guard + direction
        if 0 <= x < m and 0 <= y < n and data[y][x] == '#':
            direction.rotate_clockwise()
        else:
            guard = guard + direction
    
    return visited

def loops(data: list[list[str]], guard: Vector2, obstacle: Vector2):
    data[obstacle.y][obstacle.x] = '#'
    
    direction = Vector2(0, -1)
    visited = set()
    while 0 <= guard.x < m and 0 <= guard.y < n and not (tuple(guard), tuple(direction)) in visited:
        visited.add((tuple(guard), tuple(direction)))
        
        x, y = guard + direction
        if 0 <= x < m and 0 <= y < n and data[y][x] == '#':
            direction.rotate_clockwise()
        else:
            guard = guard + direction

    data[obstacle.y][obstacle.x] = '.'
    return 0 <= guard.x < m and 0 <= guard.y < n

def count_looping(data: list[list[str]], guard: Vector2, obstacle_positions: set[tuple[int, int]]) -> int:
    return sum([loops(data, guard, Vector2(i, j)) for i, j in obstacle_positions if Vector2(i, j) != guard])

obstacle_positions = get_path(data, Vector2(*guard))

with open('output', 'w') as output:
    output.write( str(len(obstacle_positions)) + '\n')
    output.write( str(count_looping(data, Vector2(*guard), obstacle_positions)) + '\n')