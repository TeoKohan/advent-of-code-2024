from vector2 import Vector2
from functools import reduce
from itertools import product, groupby, count

with open('input') as input:
    crops: list[str] = input.read().splitlines()
    crops: list[list[str]] = list(map(list, crops))
height = len(crops)
width  = len(crops[0])

def consume_adjacent(crops: list[list[str]], id: str, point: Vector2, region: set[Vector2]):
    if 0 <= point.x < height and 0 <= point.y < width and crops[point.x][point.y] == id:
        crops[point.x][point.y] = '_'
        region.add(point)
        return {point}.union(*[consume_adjacent(crops, id, point + direction, region) for direction in Vector2.orthogonal() if not point + direction in region])
    else:
        return set()

regions = set()
while (point := next((Vector2(i, j) for i, j in product(range(height), range(width)) if crops[i][j] != '_'), False)):
    region = set()
    consume_adjacent(crops, crops[point.x][point.y], Vector2(point.x, point.y), region)
    regions.add(frozenset(region))

def perimeter(region: set[Vector2]) -> int:
    return reduce(lambda r, x: r + sum([not (x + direction) in region for direction in Vector2.orthogonal()]), region, 0) 

def sides(region: set[Vector2]) -> int:

    borders: set[tuple[Vector2, Vector2]] = {(point, direction) for point in region for direction in Vector2.orthogonal() if not (point + direction) in region}

    side_count = 0
    for direction, direction_group in groupby(sorted(borders, key=lambda x: x[1]), lambda x: x[1]):
        if direction in [Vector2(1, 0), Vector2(-1, 0)]:
            for _, column_group in groupby(sorted(direction_group, key=lambda x: x[0].x), lambda x: x[0].x):
                side_count += sum([1 for _, _ in groupby(sorted(column_group, key=lambda x: x[0].y), lambda x, c=count(): x[0].y-next(c))])
        elif direction in [Vector2(0, 1), Vector2(0, -1)]:
            for _, row_group in groupby(sorted(direction_group, key=lambda x: x[0].y), lambda x: x[0].y):
                side_count += sum([1 for _, _ in groupby(sorted(row_group, key=lambda x: x[0].x), lambda x, c=count(): x[0].x-next(c))])
    return side_count

def area(region: set[Vector2]) -> int:
    return len(region)    

with open('output', 'w') as output:
    output.write( str(sum([perimeter(region) * area(region) for region in regions])) + '\n')
    output.write( str(sum([sides(region) * area(region) for region in regions])) + '\n')