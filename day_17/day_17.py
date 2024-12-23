import re
from enum import Enum
from functools import reduce
from itertools import product, zip_longest
    
class Register(Enum):
    A  = 0
    B  = 1
    C  = 2
    IP = 3

class Opcode(Enum):
    adv = 0
    bxl = 1
    bst = 2
    jnz = 3
    bxc = 4
    out = 5
    bdv = 6
    cdv = 7

class Instruction():
    def __init__(self, opcode: Opcode):
        self.opcode: Opcode = Opcode(opcode)

    def get_combo(literal: int, memory: dict[Register, int]):
            if literal <= 3:
                return literal
            elif literal == 4:
                return memory[Register.A]
            elif literal == 5:
                return memory[Register.B]
            elif literal == 6:
                return memory[Register.C]
            else:
                raise KeyError

    def execute(self, memory: dict[Register, int], argument: int):

        match self.opcode:
            case Opcode.adv:
                memory[Register.A] >>= Instruction.get_combo(argument, memory)
                memory[Register.IP] += 2
                return None
            case Opcode.bxl:
                memory[Register.B] ^= argument
                memory[Register.IP] += 2
                return None
            case Opcode.bst:
                memory[Register.B] = Instruction.get_combo(argument, memory) % 8
                memory[Register.IP] += 2
                return None
            case Opcode.jnz:
                if memory[Register.A]:
                    memory[Register.IP] = argument
                else:
                    memory[Register.IP] += 2
                return None
            case Opcode.bxc:
                memory[Register.B] ^= memory[Register.C]
                memory[Register.IP] += 2
                return None
            case Opcode.out:
                memory[Register.IP] += 2
                return Instruction.get_combo(argument, memory) % 8
            case Opcode.bdv:
                memory[Register.B] = memory[Register.A] >> Instruction.get_combo(argument, memory)
                memory[Register.IP] += 2
                return None
            case Opcode.cdv:
                memory[Register.C] = memory[Register.A] >> Instruction.get_combo(argument, memory)
                memory[Register.IP] += 2
                return None

with open('input') as input:
    registers, program = input.read().split('\n\n')
    registers = registers.splitlines()
    registers: dict[Register, int] = {number: int( re.search(r'(\d+)', register).group(0) ) for register, number in zip(registers, Register)} | {Register.IP: 0}

    program: list[int] = [*map(int, re.findall(r'(\d)', program))]

def step_program(program: list[int], registers: dict[Register, int]) -> str:
    ins_ptr = registers[Register.IP]
    arg_ptr = registers[Register.IP] + 1
    instruction = Instruction(program[ins_ptr])
    argument = program[arg_ptr]
    return instruction.execute(registers, argument)

def solve_program(program: list[int], registers: dict[Register, int]) -> str:
    output = []
    while 0 <= (registers[Register.IP]) and (registers[Register.IP] + 1) < len(program):
        out: None | int = step_program(program, registers)
        if out != None:
            output.append(out)
    return output


def solve_program_conformed(program: list[int], program_index: int, A_register: list[None | bool]) -> str:
    A_index = (len(program) - 1 - program_index) * 3
    result = set()

    def tribits_to_value(a: bool, b: bool, c: bool) -> int:
        return a * 4 + b * 2 + c * 1
    
    def value_to_tribits(value: int) -> tuple[None | bool, None | bool, None | bool]:
        return (value & 4) >> 2, (value & 2) >> 1, (value & 1) >> 0

    if not None in A_register:
        return {reduce(lambda r, x: r * 2 + x, A_register, 0)}
    else:
        expected_result: int = program[program_index]
        for a, b, c in product([False, True], repeat=3):
            if A_register[A_index+0] in [None, a] and A_register[A_index+1] in [None, b] and A_register[A_index+2] in [None, c]:
                    
                new_A_register = A_register.copy()
                new_A_register[A_index:A_index+3] = [a,b,c]
                
                B_register  = tribits_to_value(a, b, c)
                B_register ^= 3
                C_index     = A_index - B_register
                B_register ^= 5
                C_expect    = expected_result ^ B_register

                if all(x in [None, y] for x, y in zip_longest(reversed(new_A_register[max(0, C_index):max(0, C_index+3)]), reversed(value_to_tribits(C_expect)), fillvalue=0)):
                    new_A_register[max(0, C_index):max(0, C_index+3)] = list(map(bool, value_to_tribits(C_expect)))[:max(0, C_index+3)-max(0, C_index)]
                    result.update(solve_program_conformed(program, program_index+1, new_A_register))
    return result

with open('output', 'w') as output:
    output.write( ','.join(map(str, solve_program(program, registers))) + '\n')
    output.write( str(min(solve_program_conformed(program, 0, [None] * (len(program) * 3)))) + '\n')