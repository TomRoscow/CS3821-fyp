from typing import Dict, List, Tuple

def static_monsters(graph: Dict[Tuple[int, int], Dict[Tuple[int, int], int]], size: int) -> Tuple[Dict[Tuple[int, int], Dict[Tuple[int, int], int]], List[Tuple[int, int]]]:
    # Set monster locations according to size of maze
    if size == 8:
        monsters = [(3, 2), (3, 5)]
    elif size == 16:
        monsters = [(3, 3), (12, 12), (3, 12), (12, 3)]
    elif size == 32:
        monsters = [(2, 4), (2, 16), (2, 27), (10, 10), (10, 22), (21, 11), (21, 21), (29, 4), (29, 17), (29, 27)]
    else:
        monsters = []  # Default

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

# in visualisation.py, modify draw_maze() to take an additional parameter which is monster locations
# for every monster location, do: print_image("monster.png", tile_exits, monster_position, axs)
# When calling draw_maze(), add in the monster locations that are returned by static_monsters()