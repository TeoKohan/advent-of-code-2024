from math import prod
import re

with open('input') as input:
    datastream = input.read()

def add_all_muls(datastream: str) -> int:
    muls = re.findall(r'mul\((\d+),(\d+)\)', datastream)
    muls = (map(int, m) for m in muls)
    muls = map(prod, muls)
    return sum(muls)

def add_all_muls_with_control(datastream: str) -> int:
    instructions = re.findall(r'(?:mul\(\d+,\d+\))|(?:do\(\))|(?:don\'t\(\))', datastream)
    instructions = ''.join(instructions)
    instructions = re.sub(r"don't\(\).+?do\(\)", '', instructions)
    return add_all_muls(instructions)

with open('output', 'w') as output:
    output.write( str(add_all_muls(datastream)) + '\n')
    output.write( str(add_all_muls_with_control(datastream)) + '\n')