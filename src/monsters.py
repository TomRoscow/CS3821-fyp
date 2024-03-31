import random
from typing import Dict, List, Tuple

def static_monsters(graph: Dict[Tuple[int, int], Dict[Tuple[int, int], int]], size: int) -> Tuple[Dict[Tuple[int, int], Dict[Tuple[int, int], int]], List[Tuple[int, int]]]:
    # New method of setting monster locations randomly, still according to size of maze

    # Decide the number of monsters based on the maze size
    if size == 4:
        num_monsters = 1
    elif size == 8:
        num_monsters = 2
    elif size == 16:
        num_monsters = 4
    elif size == 32:
        num_monsters = 10
    else:
        num_monsters = 0  # Default case with no monsters

    # Generate random monster locations
    monsters = [(random.randint(0, size-1), random.randint(0, size-1)) for _ in range(num_monsters)]

    # Cost greater than base 1 to assign to edges from neighbouring tiles to monster tiles
    cost = 5
        
    # For every monster tile
    for monster in monsters:
        if monster in graph:
            # For every neighbouring tile
            for neighbour in graph[monster].keys():
                # Update the cost from neighbour to monster
                graph[neighbour][monster] = cost
    
    return graph, monsters