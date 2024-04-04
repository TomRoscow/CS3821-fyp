import argparse

from src.graph_search.a_star_search import a_star_search, heuristic_nearest_location
from src.graph import create_maze_graph
from src.graph_search.greedy import greedy_search
from src.items import add_items
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
    items_locations = add_items(size)
    graph, monsters_starts = static_monsters(graph, size)
    tile_exits, axs = draw_maze(flattened_exits, monsters_starts, items_locations, block=True)

    # A* SEARCH COLLECT ALL ITEMS
    items_path_a_star, items_cost_a_star = a_star_search(graph, (size-1, 0), size, heuristic_nearest_location, set(items_locations))
    if items_path_a_star:
        trail_to_remove = items_path_a_star[0]
        for each in items_path_a_star:
            update_character(tile_exits, each, axs, "knight.png", trail_to_remove)
            trail_to_remove = each
        print(f"A* shortest path collecting all items, length: {len(items_path_a_star)}, cost: {items_cost_a_star}. Heuristic: Nearest Item")
    else:
        print(f"No path found collecting all items with A* algorithm and nearest item heuristic.")

    erase_path(tile_exits, items_path_a_star, axs, monsters_starts, items_locations)

    # GREEDY SEARCH COLLECT ALL ITEMS
    items_path_greedy = greedy_search(graph, (size-1, 0), items_locations, heuristic_nearest_location)
    if items_path_greedy:
        trail_to_remove = items_path_greedy[0]
        for each in items_path_greedy:
            update_character(tile_exits, each, axs, "knight.png", trail_to_remove)
            trail_to_remove = each
        print(f"Greedy shortest path collecting all items, length: {len(items_path_greedy)}. Heuristic: Nearest Item")
    else:
        print(f"No path found collecting all items with greedy algorithm and nearest item heuristic.")
