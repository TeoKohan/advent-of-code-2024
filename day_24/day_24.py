import re
from operator import xor, and_, or_
from functools import reduce
from typing import Self, Callable
from itertools import product

class Signal():

    def __init__(self, database: dict[str, Self], id: str):
        self.database: dict[str, Self] = database
        self.id: str = id

    def calculate(self) -> bool:
        pass

    def get_tree(self) -> set[str]:
        pass

class Wire(Signal):

    def __init__(self, database: dict[str, Self], id: str, value: bool):
        super().__init__(database, id)
        self.value: bool = value
    
    def calculate(self) -> bool:
        return self.value

    def get_tree(self) -> set[str]:
        return set([self.id])

class Gate(Signal):

    def __init__(self, database: dict[str, Self], id: str, left: str, operation: Callable[[bool, bool], bool], right: str):
        super().__init__(database, id)
        self.operation: Callable[[bool, bool], bool] = operation
        self.left: str  = left
        self.right: str = right

    def set_operation(self, operation: Callable[[bool, bool], bool]):
        self.operation = operation

    def set_dependencies(self, a: str, b: str):
        self.left  = a
        self.right = b
    
    def get_left(self) -> Signal:
        return self.database[self.left]

    def get_right(self) -> Signal:
        return self.database[self.right]
    
    def calculate(self) -> bool:
        return self.operation(self.get_left().calculate(), self.get_right().calculate())

    def get_tree(self) -> set[str]:
        return self.get_left().get_tree().union(self.get_right().get_tree()).union(set([self.id]))

with open('input') as input:
    in_wires, in_gates = input.read().split('\n\n')
    in_wires: list[str] = in_wires.splitlines()
    in_wires: list[tuple[str, str]] = [re.match(r'(\w+): (0|1)', wire).groups() for wire in in_wires]
    in_wires: list[tuple[str, str]] = [(cable, bool(int(value))) for cable, value in in_wires]

    in_gates: list[str] = in_gates.splitlines()
    in_gates: list[tuple[str, str, str, str]] = [re.match(r'(\w+) (AND|OR|XOR) (\w+) -> (\w+)', gate).groups() for gate in in_gates]

    gates: dict[str, Wire | Gate] = dict()
    gates |= {id: Wire(gates, id, value) for id, value in in_wires} |\
             {id: Gate(gates, id, left, {'AND': and_, 'OR': or_, 'XOR': xor}[op], right) for left, op, right, id in in_gates}

def get_output(gates: dict[str, Wire | Gate], output_gates: list[str]) -> int:
    return reduce(lambda r, x: r * 2 + x, [gates[gate].calculate() for gate in output_gates], 0)

def get_full_output(gates: dict[str, Wire | Gate]) -> int:
    z_gates: list[str] = sorted([*filter(lambda x: 'z' in x, gates)], reverse=True)
    return get_output(gates, z_gates)

def correct_output(gates: dict[str, Wire | Gate], i: int):
    prev: str = f"{i-1:02d}" if i > 0 else None
    curr: str = f"{i  :02d}"

    correct = True
    for a,b,c,d in product([True, False], repeat=4):
        if prev:
            gates['x'+prev].value = a
            gates['y'+prev].value = c
        gates['x'+curr].value = b
        gates['y'+curr].value = d
        if prev:
            correct = correct and gates['z'+curr].calculate() == xor(a and c, xor(b, d))
        else:
            correct = correct and gates['z'+curr].calculate() == xor(b, d)
    return correct

def dependencies(gates: dict[str, Wire | Gate], i: int) -> list[Signal]:
    prev: str = f"{i-1:02d}" if i > 0 else None
    curr: str = f"{i  :02d}"
    prev_gates: set[str] = gates['z'+ prev].get_tree() if prev else []
    curr_gates: set[str] = gates['z'+ curr].get_tree()
    return [*filter(lambda x: x not in prev_gates and isinstance(gates[x], Gate), curr_gates)]

def fix_output(gates: dict[str, Wire | Gate], i: int, j: int) -> tuple[Gate, Callable[[bool, bool], bool]]:
    A: set[str] = dependencies(gates, i)
    B: set[str] = dependencies(gates, j)

    for u, v in product(A, B):
        if u not in gates[v].get_tree() and v not in gates[u].get_tree():
            gates[u], gates[v] = gates[v], gates[u]
            if correct_output(gates, i) and correct_output(gates, j):
                gates[u], gates[v] = gates[v], gates[u]
                return u, v
            gates[u], gates[v] = gates[v], gates[u]

def find_defective(gates: dict[str, Wire | Gate]) -> str:

    for i in range(45):
        gates['x'+f'{i:02d}'].value = False
        gates['y'+f'{i:02d}'].value = False

    wrong_outputs = [*filter(lambda x: not correct_output(gates, x), range(45))]

    wrong_gates: set[str] = set()
    for i, j in product(wrong_outputs, repeat=2):
        if i != j:
            t = fix_output(gates, i, j)
            if t:
                wrong_gates.update(t)

    return ','.join(sorted(wrong_gates))

with open('output', 'w') as output:
    output.write( str(get_full_output(gates)) + '\n')
    output.write( str(find_defective(gates)) + '\n')