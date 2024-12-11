import re
from typing import Callable
from operator import add, mul

with open('input') as input:
    equations: list[list[int]] = input.read().splitlines()
    equations: list[list[int]] = [re.findall(r'\d+', equation) for equation in equations]
    equations: list[list[int]] = [list(map(int, equation)) for equation in equations]

def concat(left: int, right: int) -> int:
    return int(str(left) + str(right))

def solve_equation(result: int, current_value: int, numbers: list[int], operators: list[Callable[[int, int], int]]) -> bool:
    if not numbers:
        return result == current_value
    else:
        next_value, *leftover_numbers = numbers
        return any(solve_equation(result, operator(current_value, next_value), leftover_numbers, operators) for operator in operators)

def test_values(equations: list[list[int]], operators: list[Callable[[int, int], int]]) -> int:
    sum = 0
    for equation in equations:
        result, initial_value, *numbers = equation
        sum += result if solve_equation(result, initial_value, numbers, operators) else 0
    return sum

with open('output', 'w') as output:
    output.write( str(test_values(equations, [add, mul])) + '\n')
    output.write( str(test_values(equations, [add, mul, concat])) + '\n')