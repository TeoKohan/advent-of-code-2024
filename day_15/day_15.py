import re
from vector2 import Vector2
from copy import deepcopy

with open('input') as input:
    warehouse, moves = input.read().split('\n\n')
    warehouse: list[str] = warehouse.splitlines()
    warehouse: list[list[str]] = [*map(list, warehouse)]

    D: dict[str, Vector2] = dict(zip('^>v<', Vector2.orthogonal()))
    moves = [line.rstrip() for line in moves]
    moves = ''.join(moves)
    moves = [D[move] for move in moves]

def print_warehouse(warehouse: list[list[str]]):
    print(''.join(map(lambda x: ''.join(x) + '\n' , warehouse)))

def push(warehouse: list[list[str]], player: Vector2, direction: Vector2):

    changes: dict[tuple[int, int], str] = dict()
    pending: list[tuple[Vector2, str]] = [(player, '.')]

    while pending:
        position, value = pending.pop()
        looking = warehouse[position.y][position.x]
        match looking:
            case '.':
                changes[tuple(position)] = value 
            case '#':
                return False
            case 'O':
                changes[tuple(position)] = value 
                pending.append( (position + direction, 'O') )
            case '@':
                changes[tuple(position)] = value 
                pending.append( (position + direction, '@') )
            case '[':
                changes[tuple(position)] = value 
                pending.append( (position + direction, '[') )
                if not tuple(position + Vector2(1, 0)) in changes:
                    pending.append( (position + Vector2(1, 0), '.') )
            case ']':
                changes[tuple(position)] = value 
                pending.append( (position + direction, ']') )
                if not tuple(position - Vector2(1, 0)) in changes:
                    pending.append( (position - Vector2(1, 0), '.') )
                    
                
    for (x, y) in changes:
        warehouse[y][x] = changes[(x, y)]
    player += direction
    return True

def GPS(warehouse: list[list[str]]):
    rocks = 0
    for i, line in enumerate(warehouse):
        for j, object in enumerate(line):
            if object == 'O' or object == '[':
                rocks += 100 * i + j
    return rocks

def solve_warehouse(warehouse: list[list[str]], moves: list[Vector2]):

    for i, line in enumerate(warehouse):
        if '@' in line:
            robot: Vector2 = Vector2(line.index('@'), i)

    for move in moves:
        push(warehouse, robot, move)

    return GPS(warehouse)

def embiggen(warehouse: list[list[str]]) -> list[list[str]]:
    new_warehouse: list[list[str]] = [*map(''.join, warehouse)]
    new_warehouse = [re.sub(r'#' , '##', line) for line in new_warehouse]
    new_warehouse = [re.sub(r'O' , '[]', line) for line in new_warehouse]
    new_warehouse = [re.sub(r'\.', '..', line) for line in new_warehouse]
    new_warehouse = [re.sub(r'@' , '@.', line) for line in new_warehouse]
    new_warehouse = list(map(list, new_warehouse))
    return new_warehouse

with open('output', 'w') as output:
    output.write( str(solve_warehouse(deepcopy(warehouse), moves)) + '\n')
    output.write( str(solve_warehouse(embiggen(warehouse), moves)) + '\n')