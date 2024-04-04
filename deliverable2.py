import argparse

from src.graph_search.breadth_first import bfs
from src.graph_search.depth_first import dfs
from src.graph import create_maze_graph
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
    monsters_starts = []
    tile_exits, axs = draw_maze(flattened_exits, monsters_starts, items_locations, block=True)

    # BREADTH-FIRST SEARCH ENTRANCE TO CROWN
    bfs_path = bfs(graph, (size-1, 0), (0, size-1))
    if bfs_path:
        trail_to_remove = bfs_path[0]
        for each in bfs_path:
            update_character(tile_exits, each, axs, "knight.png", trail_to_remove)   
            trail_to_remove = each
        print(f"BFS shortest path from character to reward: {bfs_path}")
    else:
        print(f"No path found from character to reward with BFS.")

    erase_path(tile_exits, bfs_path, axs, monsters_starts, items_locations)

    # DEPTH-FIRST SEARCH ENTRANCE TO CROWN
    dfs_path = dfs(graph, (size-1, 0), (0, size-1))
    if dfs_path:
        trail_to_remove = dfs_path[0]
        for each in dfs_path:
            update_character(tile_exits, each, axs, "knight.png", trail_to_remove)   
            trail_to_remove = each
        print(f"DFS first path from character to reward: {dfs_path}")
    else:
        print(f"No path found from character to reward with DFS.")