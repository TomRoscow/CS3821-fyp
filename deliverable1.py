import argparse

from src.graph import create_maze_graph
from src.visualisation import draw_maze


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
