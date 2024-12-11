import re
from itertools import chain, product

with open('input') as input:
    wordsearch: list[str] = input.read().splitlines()

def transpose(wordsearch):
    return list(map(''.join, (map(list, zip(*wordsearch)))))

def main_diagonal(wordsearch, i, j):
    while 0 <= i < len(wordsearch) and 0 <= j < len(wordsearch[0]):
        yield wordsearch[i][j]
        i, j = i+1, j+1

def secondary_diagonal(wordsearch, i, j):
    while 0 <= i < len(wordsearch) and 0 <= j < len(wordsearch[0]):
        yield wordsearch[i][j]
        i, j = i-1, j+1

def xmas(wordsearch: list[str]) -> int:
    return sum(
        [
            len(re.findall(r'(?=(XMAS))|(?=(SAMX))', line))
            for line in chain(
                wordsearch,
                transpose(wordsearch),
                (''.join(main_diagonal(wordsearch, i, 0)) for i in range(len(wordsearch))),
                (''.join(main_diagonal(wordsearch, 0, j)) for j in range(1, len(wordsearch[0]))),
                (''.join(secondary_diagonal(wordsearch, i, 0)) for i in range(len(wordsearch))),
                (''.join(secondary_diagonal(wordsearch, len(wordsearch)-1, j)) for j in range(1, len(wordsearch[0])))
            )
        ]
    )

def x_mas(wordsearch: list[str]) -> int:
    x_mases: int = 0
    for li, lj in product(range(0, len(wordsearch) - 2), range(0, len(wordsearch[0]) - 2)):
        chunk = [[wordsearch[i][j] for j in range(lj, lj+3)] for i in range(li, li+3)]
        chunk_main_diagonal = ''.join(main_diagonal(chunk, 0, 0))
        chunk_secondary_diagonal = ''.join(secondary_diagonal(chunk, len(chunk)-1, 0))
        is_main_sam = bool(re.match(r'(?=(MAS))|(?=(SAM))', chunk_main_diagonal))
        is_secondary_sam = bool(re.match(r'(?=(MAS))|(?=(SAM))', chunk_secondary_diagonal))
        x_mases += is_main_sam and is_secondary_sam
    return x_mases

with open('output', 'w') as output:
    output.write( str(xmas(wordsearch)) + '\n')
    output.write( str(x_mas(wordsearch)) + '\n')