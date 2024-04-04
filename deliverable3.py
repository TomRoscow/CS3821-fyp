import argparse

from src.graph import create_maze_graph
from src.monsters import static_monsters
from src.graph_search.uniform_cost import uniform_cost_search
from src.visualisation import draw_maze, update_character


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

    # UNIFORM-COST SEARCH ENTRANCE TO CROWN
    ucs_path, ucs_cost = uniform_cost_search(graph, (size-1, 0), (0, size-1))
    if ucs_path:
        trail_to_remove = ucs_path[0]
        for each in ucs_path:
            update_character(tile_exits, each, axs, "knight.png", trail_to_remove)   
            trail_to_remove = each
        print(f"UCS least costly path from character to reward: {ucs_path}, Cost: {ucs_cost}")
    else:
        print(f"No path found from character to reward with UCS.")