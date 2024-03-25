import random
from typing import Dict, List, Tuple

def add_items(graph: Dict[Tuple[int, int], Dict[Tuple[int, int], int]], size: int) -> List[Tuple[int, int]]:
    # Set item locations according to size of maze
    # if size == 8:
    #     items = [(4, 5), (1, 2), (2, 0), (1, 1), (3, 6)]
    # elif size == 16:
    #     items = [(8, 1), (11, 1), (15, 3), (15, 9), (14, 10)]
    # elif size == 32:
    #     items = [(8, 22), (19, 30), (19, 24), (11, 28), (31, 6)]
    # else:
    #     items = []  # Default
    

    # New method of setting item locations randomly, still according to size of maze
        
    # Decide the number of items based on the maze size
    if size == 8:
        num_items = 3
    if size == 12:
        num_items = 5
    elif size == 16:
        num_items = 5
    elif size == 32:
        num_items = 11
    else:
        num_items = 0  # Default case with no items

    # Generate random item locations
    items = [(random.randint(0, size-1), random.randint(0, size-1)) for _ in range(num_items)]

    return items