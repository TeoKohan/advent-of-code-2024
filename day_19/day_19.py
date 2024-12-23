import re

with open('input') as input:
    available, patterns = input.read().split('\n\n')
    available: list[str] = re.findall(r'[^, ]+', available)
    patterns: list[str] = patterns.splitlines()

def can_make(available: list[str], pattern: str) -> bool:
    return pattern == '' or any(re.match(towel, pattern) and can_make(available, pattern[len(towel):]) for towel in available)

def ways_to_make(M: dict[str, int], available: list[str], pattern: str) -> bool:
    if not pattern in M:
        if pattern == '':
            M[pattern] = 1
        else:
            M[pattern] = sum(
                ways_to_make(M, available, pattern[len(towel):])
                for towel in available
                if re.match(towel, pattern)
            )
    return M[pattern]

with open('output', 'w') as output:
    output.write( str(sum(can_make(available, pattern) for pattern in patterns)) + '\n')
    output.write( str(sum(ways_to_make(dict(), available, pattern) for pattern in patterns)) + '\n')