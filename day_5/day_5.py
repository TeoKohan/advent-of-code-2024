import re

with open('input') as input:
    rules, orders = input.read().split('\n\n')
    rules  = rules .splitlines()
    orders = orders.splitlines()
    rules  = [tuple(map(int, re.findall(r'\d+', rule))) for rule in rules]
    orders = [list(map(int, re.findall(r'\d+', order))) for order in orders]

def fix(order: list[int], rules):
    new_order = order.copy()
    while rule := next(
                ((x, y) 
                    for x, y in rules 
                    if x in new_order and y in new_order 
                    and new_order.index(x) > new_order.index(y)),
                None
            ):
        x, y = rule
        ix, iy = new_order.index(x), new_order.index(y)
        new_order[ix], new_order[iy] = new_order[iy], new_order[ix]
    return new_order

compliant = sum(
    order[len(order)//2] 
    for order in orders
    if all(order.index(x) < order.index(y) for x, y in rules if x in order and y in order)
)

fixed_orders = sum(
    fix(order, rules)[len(order)//2]
    for order in orders 
    if any(order.index(x) > order.index(y) for x, y in rules if x in order and y in order)
)

with open('output', 'w') as output:
    output.write( str(compliant) + '\n')
    output.write( str(fixed_orders) + '\n')