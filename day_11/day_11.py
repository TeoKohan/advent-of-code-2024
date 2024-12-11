from collections import defaultdict
import re

with open('input') as input:
    data: list[str] = re.findall(r'\d+', input.read().rstrip())
    stones: dict[int, int] = defaultdict(int)
    for stone in map(int, data):
        stones[stone] += 1

def blink(stones: dict[int, int], times: int) -> dict[int, int]:
    if times > 0:
        new_stones = defaultdict(int)
        for stone, amount in stones.items():
            if stone == 0:
                new_stones[1] += amount
            elif len(str(stone)) % 2 == 0:
                half_digits = len(str(stone)) // 2
                left, right = stone//(10**half_digits), stone % (10**half_digits)
                new_stones[left] += amount
                new_stones[right] += amount
            else:
                new_stones[stone*2024] += amount
        return blink(new_stones, times-1)
    else:
        return stones

with open('output', 'w') as output:
    output.write( str(sum(blink(stones, 25).values())) + '\n')
    output.write( str(sum(blink(stones, 75).values())) + '\n')