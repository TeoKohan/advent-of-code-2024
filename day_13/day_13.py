import re
from fractions import Fraction
from vector2 import Vector2

with open('input') as input:
    claw_machines: list[str] = input.read().split('\n\n')
    claw_machines: list[list[str]] = [machine.splitlines() for machine in claw_machines]
    claw_machines: list[list[Vector2]] = [[Vector2(*map(int, re.findall(r'\d+', line))) for line in machine] for machine in claw_machines]

def solve_machine(a_button: Vector2, b_button: Vector2, prize: Vector2) -> None | int:
    a1, a2 = a_button
    b1, b2 = b_button
    x , y  = prize

    A: list[list[Fraction]] = [
        [a1, b1, x],
        [a2, b2, y]
    ]

    A[1] = [0, b2 - b1 * Fraction(a2, a1), y - x * Fraction(a2, a1)]
    A[1] = [*map(lambda x: x / A[1][1], A[1])]
    A[0] = [A[0][0], 0, A[0][2] - A[1][2] * A[0][1]]
    A[0] = [*map(lambda x: x / A[0][0], A[0])]

    if A[0][2].is_integer() and A[1][2].is_integer():
        return Vector2(int(A[0][2]), int(A[1][2]))
    else:
        return Vector2.zero()

def solve_machine_bigger(a_button: Vector2, b_button: Vector2, prize: Vector2) -> None | int:
    return solve_machine(a_button, b_button, prize + Vector2.one() * 10000000000000)

tokens_normal = sum(
    solve_machine(*machine) @ Vector2(3, 1)
    for machine in claw_machines
)

tokens_bigger = sum(
    solve_machine_bigger(*machine) @ Vector2(3, 1)
    for machine in claw_machines
)

with open('output', 'w') as output:
    output.write( str(tokens_normal) + '\n')
    output.write( str(tokens_bigger) + '\n')