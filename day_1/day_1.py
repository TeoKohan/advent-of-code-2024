import re

with open('input') as input:
    location_ids = input.read().splitlines()
    location_ids = [re.findall(r'\d+', id) for id in location_ids]
    location_ids = [[int(x), int(y)] for x, y in location_ids]

left_ids, right_ids = list(zip(*location_ids))
left_ids, right_ids = sorted(left_ids), sorted(right_ids)

def distance(left_ids: list[int], right_ids: list[int]) -> int:
    pairs = zip(left_ids, right_ids)
    return sum([abs(x-y) for x, y in pairs])

def similarity_score(left_ids: list[int], right_ids: list[int]) -> int:
    return sum([x * right_ids.count(x) for x in left_ids])

with open('output', 'w') as output:
    output.write( str(distance(left_ids, right_ids)) + '\n')
    output.write( str(similarity_score(left_ids, right_ids)) + '\n')