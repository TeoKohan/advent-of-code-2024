with open('input') as input:
    objects: list[str] = input.read().split('\n\n')
    objects: list[list[str]] = [object.splitlines() for object in objects]
    keys, locks = [*filter(lambda x: x[0] == '#####', objects)], [*filter(lambda x: x[0] == '.....', objects)]

def fits(key: list[str], lock: list[str]) -> bool:

    def can_combine_row(key_row: str, lock_row: str) -> bool:
        return all(i != '#' or j != '#' for i, j in zip(key_row, lock_row))

    return all(can_combine_row(key_row, lock_row) for key_row, lock_row in zip(key, lock))

def try_locks(keys: list[list[str]], locks: list[list[str]]) -> int:
    return sum(fits(key, lock) for key in keys for lock in locks)

with open('output', 'w') as output:
    output.write( str(try_locks(keys, locks)) + '\n')