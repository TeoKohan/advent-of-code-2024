from typing import Self
from itertools import product, chain

with open('input') as input:
    pairs: list[str] = input.read().splitlines()
    pairs: list[tuple[str, str]] = [tuple(pair.split('-')) for pair in pairs]

class Node():

    def __init__(self, id: str):
        self.id: str = id
        self.connections: dict[str, Node] = dict()
    
    def add_connection(self, node: Self):
        self.connections[node.id] = node
    
D: dict[str, Node] = dict()
for a, b in pairs:
    if a not in D:
        D[a] = Node(a)
    if b not in D:
        D[b] = Node(b)
    
    D[a].add_connection(D[b])
    D[b].add_connection(D[a])

def three_cliques(database: dict[str, Node]) -> set[frozenset[str]]:

    triplets: set[frozenset[str]] = set()

    for comA, comB in product(D.values(), repeat=2):
        if comA.id in comB.connections and comB.id in comA.connections:
            for child in comA.connections:
                if child in comB.connections:
                    triplets.add(frozenset((comA.id, child, comB.id)))

    return triplets

def expand_cliques(database: dict[str, Node], k_cliques: set[frozenset[str]]):

    new_cliques: set[frozenset[str]] = set()
    for clique in k_cliques:
        expanded_clique = expand_clique(database, clique)
        if expanded_clique:
            new_cliques.add(expanded_clique)
    return new_cliques

def expand_clique(database: dict[str, Node], k_clique: frozenset[str]):
    
    witness: Node = database[next(iter(k_clique))]
    for possible in witness.connections:
        if possible not in k_clique and all(possible in database[node].connections for node in k_clique):
            return frozenset(chain(k_clique, [possible]))

def t_three_cliques(database: dict[str, Node]) -> int:

    triplets: set[frozenset[str]] = three_cliques(D)
    t_starts = [*filter(lambda x: any(y.startswith('t') for y in x), triplets)]
    return len(t_starts)

def biggest_clique(database: dict[str, Node]) -> frozenset[str]:

    cliques: set[frozenset[str]] = three_cliques(database)
    while len((cliques := expand_cliques(D, cliques))) > 1:
        pass
    return next(iter(cliques))

with open('output', 'w') as output:
    output.write( str(t_three_cliques(D)) + '\n')
    output.write( str(','.join(sorted(item for item in biggest_clique(D)))) + '\n')