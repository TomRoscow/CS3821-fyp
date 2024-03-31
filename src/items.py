from typing import List, Tuple

def add_items(size: int) -> List[Tuple[int, int]]:
    # Adds an item to every tile, except the crown and entrance tiles
    items = []
    for i in range(size):
        for j in range(size):
            items.append((i, j))
    items.remove((0, size-1))
    items.remove((size-1, 0))
    return items