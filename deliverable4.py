import argparse

from src.graph_search.a_star_search import a_star_search, custom_heuristic, heuristic_nearest_location, heuristic_sum_locations
from src.graph import create_maze_graph
from src.monsters import static_monsters
from src.visualisation import draw_maze, erase_path, update_character


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Maze Size Selector")
    parser.add_argument("--size", type=str, choices=['small', 'medium', 'large'], help="Size of the maze: small, medium, or large")
    args = parser.parse_args()
    # Map the size choices to numerical sizes
    size_mapping = {
        'small': 4,
        'medium': 8,
        'large': 16
    }
    # Get the numerical size from the user's input
    size = size_mapping.get(args.size, 4)  # Default to 'small' (4x4) if not specified

    # Set up the maze with items on all tiles and some monsters
    flattened_exits, graph = create_maze_graph(size, seed=0)
    items_locations = []
    graph, monsters_starts = static_monsters(graph, size)
    tile_exits, axs = draw_maze(flattened_exits, monsters_starts, items_locations, block=True)

    # A* SEARCH ALL CORNERS, THREE HEURISTICS
    
    def get_corners(N):
        """Get all corners for an NxN maze."""
        return [(0, 0), (0, N-1), (N-1, 0), (N-1, N-1)]

    a_star_path, a_star_cost = a_star_search(graph, (size-1, 0), size, heuristic_nearest_location, set(get_corners(size)))
    if a_star_path:
        trail_to_remove = a_star_path[0]
        for each in a_star_path:
            update_character(tile_exits, each, axs, "knight.png", trail_to_remove)
            trail_to_remove = each
        print(f"A* shortest path touching all corners, length: {len(a_star_path)}, cost: {a_star_cost}. Heuristic: Nearest Corner")
    else:
        print(f"No path found touching all corners with A* algorithm and nearest corner heuristic.")

    erase_path(tile_exits, a_star_path, axs, monsters_starts, items_locations)
        
    a_star_path, a_star_cost = a_star_search(graph, (size-1, 0), size, heuristic_sum_locations, set(get_corners(size)))
    if a_star_path:
        trail_to_remove = a_star_path[0]
        for each in a_star_path:
            update_character(tile_exits, each, axs, "knight.png", trail_to_remove)
            trail_to_remove = each
        print(f"A* shortest path touching all corners, length: {len(a_star_path)}, cost: {a_star_cost}. Heuristic: Sum of Corners")
    else:
        print(f"No path found touching all corners with A* algorithm and sum of corners heuristic.")

    erase_path(tile_exits, a_star_path, axs, monsters_starts, items_locations)

    a_star_path, a_star_cost = a_star_search(graph, (size-1, 0), size, custom_heuristic, set(get_corners(size)))
    if a_star_path:
        trail_to_remove = a_star_path[0]
        for each in a_star_path:
            update_character(tile_exits, each, axs, "knight.png", trail_to_remove)
            trail_to_remove = each
        print(f"A* shortest path touching all corners, length: {len(a_star_path)}, cost: {a_star_cost}. Heuristic: Custom")
    else:
        print(f"No path found touching all corners with A* algorithm and my custom heuristic.")