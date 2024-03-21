from typing import Dict, List, Tuple


def add_items(graph: Dict[Tuple[int, int], Dict[Tuple[int, int], int]], size: int) -> Tuple[Dict[Tuple[int, int], Dict[Tuple[int, int], int]], List[Tuple[int, int]]]:
    # Set item locations according to size of maze
    if size == 8:
        items = [(4, 5), (1, 2), (2, 0), (1, 1), (3, 6)]   # monsters at [(3, 2), (3, 5)]
    elif size == 16:
        items = [(8, 1), (11, 1), (15, 3), (15, 9), (14, 10)]   # monsters at [(3, 3), (12, 12), (3, 12), (12, 3)]
    elif size == 32:
        items = [(8, 22), (19, 30), (19, 24), (11, 28), (31, 6)]   # monsters at [(2, 4), (2, 16), (2, 27), (10, 10), (10, 22), (21, 11), (21, 21), (29, 4), (29, 17), (29, 27)]
    else:
        items = []  # Default

    return graph, items