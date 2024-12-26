from typing import Generator
from collections import defaultdict
from operator import sub
from itertools import islice, tee, starmap

with open('input') as input:
    secret_codes: list[str] = input.read().splitlines()
    secret_codes: list[int] = [int(code) for code in secret_codes]

def monkey(number: int):
    while True:
        yield number
        number = ((number <<  6) ^ number) & 16777215
        number = ((number >>  5) ^ number) & 16777215
        number = ((number << 11) ^ number) & 16777215

def two_thousandth_monkey(secret_codes: list[int]) -> int:
    monkeys: list[Generator] = [*map(monkey, secret_codes)]
    for _ in range(2000):
        [next(m) for m in monkeys]
    return sum([next(m) for m in monkeys])

def savvy_monkeys(secret_codes: list[int]) -> int:

    stop_sequence_values: dict[tuple[int, int, int, int], int] = defaultdict(lambda: 0)

    monkeys: list[list[int]] = [list(islice(monkey(m), 2000)) for m in secret_codes]
    monkey_values: list[list[int]] = [[d % 10 for d in m] for m in monkeys]

    for values in monkey_values:
        
        deltas: list[list[int]] = starmap(sub, zip(values[1:], values))

        a, b = tee(deltas)
        next(b)
        b, c = tee(b)
        next(c)
        c, d = tee(c)
        next(d)
        v = iter(values[4:])
        sequence_values = zip(v, a, b, c, d)

        visited = set()
        for value, *sequence in sequence_values:
            if tuple(sequence) not in visited:
                visited.add(tuple(sequence))
                stop_sequence_values[tuple(sequence)] += value

    return(max(stop_sequence_values.values()))

with open('output', 'w') as output:
    output.write( str(two_thousandth_monkey(secret_codes)) + '\n')
    output.write( str(savvy_monkeys(secret_codes)) + '\n')