import math
from graph_search.greedy import greedy_search
from monsters import static_monsters
from items import add_items
from visualisation import draw_maze, erase_path, update_knight
from graph import create_maze_graph
from graph_search.breadth_first import bfs
from graph_search.depth_first import dfs
from graph_search.uniform_cost import uniform_cost_search
from graph_search.a_star_search import a_star_search, heuristic_nearest_location, heuristic_sum_locations, custom_heuristic
from comparison_a_star_greedy import compare_a_star_greedy
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Maze Size Selector")
    parser.add_argument("--size", type=str, choices=['small', 'medium', 'large'], help="Size of the maze: small, medium, or large")
    args = parser.parse_args()

    # Map the size choices to numerical sizes
    size_mapping = {
        'small': 8,  # Let a small maze be 8x8
        'medium': 16,  # Let a medium maze be 15x15
        'large': 32   # Let a large maze be 20x20
    }
    
    # Get the numerical size from the user's input
    size = size_mapping.get(args.size, 8)  # Default to 'small' (8x8) if not specified

    #parser = argparse.ArgumentParser()
    #parser.add_argument("--tile_exits")
    #args = parser.parse_args()

    # draw_maze([["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"]])

    #size = 10  <-this was the old way of setting size before user choice to also med or large
    flattened_exits, graph = create_maze_graph(size)

    # Creates monsters and places them in graph
    graph, monsters = static_monsters(graph, size)

    # Creates items and places them in graph
    items_locations = add_items(graph, size)
    
    tile_exits, axs = draw_maze(flattened_exits, monsters, items_locations, block=True)

    # My attempt to create a list of entities instead of handling drawing the crown and knight separately repeatedly
    #entities = [[]]
    #for each in entities:
    #    print_image(name)

    # BREADTH-FIRST SEARCH ENTRANCE TO CROWN
    bfs_path = bfs(graph, (size-1, 0), (0, size-1))
    if bfs_path:
        print(f"BFS shortest path from character to reward: {bfs_path}")
    else:
        print(f"No path found from character to reward with BFS.")

    # DEPTH-FIRST SEARCH ENTRANCE TO CROWN
    dfs_path = dfs(graph, (size-1, 0), (0, size-1))
    if dfs_path:
        print(f"DFS first path from character to reward: {dfs_path}")
    else:
        print(f"No path found from character to reward with DFS.")
        
    # UNIFORM-COST SEARCH ENTRANCE TO CROWN
    ucs_path, ucs_cost = uniform_cost_search(graph, (size-1, 0), (0, size-1))
    if ucs_path:
        for each in ucs_path:
            update_knight(tile_exits, each, axs, block=True)   
        print(f"UCS least costly path from character to reward: {ucs_path}, Cost: {ucs_cost}")
    else:
        print(f"No path found from character to reward with UCS.")

    erase_path(tile_exits, ucs_path, axs, monsters, items_locations)

    # A* SEARCH ALL CORNERS, THREE HEURISTICS
    
    def get_corners(N):
        """Get all corners for an NxN maze."""
        return [(0, 0), (0, N-1), (N-1, 0), (N-1, N-1)]

    a_star_path, a_star_cost = a_star_search(graph, (size-1, 0), size, heuristic_nearest_location, set(get_corners(size)))
    if a_star_path:
        for each in a_star_path:
            update_knight(tile_exits, each, axs, block=True)
        print(f"A* shortest path touching all corners, length: {len(a_star_path)}, cost: {a_star_cost}. Heuristic: Nearest Corner")
    else:
        print(f"No path found touching all corners with A* algorithm and nearest corner heuristic.")

    erase_path(tile_exits, a_star_path, axs, monsters, items_locations)
        
    a_star_path, a_star_cost = a_star_search(graph, (size-1, 0), size, heuristic_sum_locations, set(get_corners(size)))
    if a_star_path:
        for each in a_star_path:
            update_knight(tile_exits, each, axs, block=True)
        print(f"A* shortest path touching all corners, length: {len(a_star_path)}, cost: {a_star_cost}. Heuristic: Sum of Corners")
    else:
        print(f"No path found touching all corners with A* algorithm and sum of corners heuristic.")

    erase_path(tile_exits, a_star_path, axs, monsters, items_locations)

    a_star_path, a_star_cost = a_star_search(graph, (size-1, 0), size, custom_heuristic, set(get_corners(size)))
    if a_star_path:
        for each in a_star_path:
            update_knight(tile_exits, each, axs, block=True)
        print(f"A* shortest path touching all corners, length: {len(a_star_path)}, cost: {a_star_cost}. Heuristic: Custom")
    else:
        print(f"No path found touching all corners with A* algorithm and my custom heuristic.")

    erase_path(tile_exits, a_star_path, axs, monsters, items_locations)    

    
    # A* SEARCH COLLECT ALL ITEMS
    items_path_a_star, items_cost_a_star = a_star_search(graph, (size-1, 0), size, heuristic_nearest_location, set(items_locations))
    if items_path_a_star:
        for each in items_path_a_star:
            update_knight(tile_exits, each, axs, block=True)
        print(f"A* shortest path collecting all items, length: {len(items_path_a_star)}, cost: {items_cost_a_star}. Heuristic: Nearest Item")
    else:
        print(f"No path found collecting all items with A* algorithm and nearest item heuristic.")

    erase_path(tile_exits, items_path_a_star, axs, monsters, items_locations)

    # GREEDY SEARCH COLLECT ALL ITEMS
    items_path_greedy = greedy_search(graph, (size-1, 0), items_locations, heuristic_nearest_location)
    if items_path_greedy:
        for each in items_path_greedy:
            update_knight(tile_exits, each, axs, block=True)
        print(f"Greedy shortest path collecting all items, length: {len(items_path_greedy)}. Heuristic: Nearest Item")
    else:
        print(f"No path found collecting all items with greedy algorithm and nearest item heuristic.")

    # COMPARISON OF A* AND GREEDY SEARCHES COLLECTING ALL ITEMS OVER SEVERAL ITERATIONS
    #compare_a_star_greedy()