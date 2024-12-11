from typing import Self
from copy import deepcopy
from itertools import repeat, chain

class DataBlock():
    def __init__(self: Self, id: int | None, size: int):
        self.id: int = id
        self.size: int = size
    
    def is_free(self: Self) -> bool:
        return self.id == None

    def free(self: Self):
        self.id = None
    
    def __iter__ (self: Self):
        return repeat(self.id, self.size)

with open('input') as input:
    data = input.read().rstrip()
    all_blocks: list[DataBlock] = [
        DataBlock(i//2 if i % 2 == 0 else None, int(size))
        for i, size in enumerate(data)
    ]

def checksum(all_blocks: list[DataBlock]) -> int:
    return sum(
        i * id if id != None else 0
        for i, id in enumerate(chain(*all_blocks))
    )

def compact(all_blocks: list[DataBlock]):
    while \
        (full  := next(i for i, item in reversed(list(enumerate(all_blocks))) if not item.is_free())) \
        > \
        (empty := next(i for i, item in enumerate(all_blocks) if item.is_free())):
        
        full_block:  DataBlock = all_blocks[full]
        empty_block: DataBlock = all_blocks[empty]
        transfer_amount = min(empty_block.size, full_block.size)
        full_block_id: int = full_block.id

        full_block.size -= transfer_amount
        if not full_block.size:
            del all_blocks[full]

        if transfer_amount == empty_block.size:
            empty_block.id = full_block_id
        else:
            empty_block.size -= transfer_amount
            all_blocks.insert(empty, DataBlock(full_block_id, transfer_amount))

    return all_blocks


def compact_full_block(all_blocks: list[DataBlock]) -> int:
    for full_block in filter(lambda block: not block.is_free(), reversed(all_blocks)):
        full  = all_blocks.index(full_block)
        empty = next((i for i, block in enumerate(all_blocks) if block.is_free() and block.size >= full_block.size and i < full), None)
        if empty:
            all_blocks[empty].size -= full_block.size
            all_blocks.insert(empty, DataBlock(full_block.id, full_block.size))
            full_block.free() 

    return all_blocks

with open('output', 'w') as output:
    output.write( str(checksum(compact(deepcopy(all_blocks)))) + '\n')
    output.write( str(checksum(compact_full_block(deepcopy(all_blocks)))) + '\n')