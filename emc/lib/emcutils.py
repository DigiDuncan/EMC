def items_to_stacks(count: int):
    stacks = count // 64
    items = count % 64
    return stacks, items
