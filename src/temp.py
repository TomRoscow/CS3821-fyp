import math
from visualisation import draw_maze, update_knight
from graph import create_maze_graph
from graph_search.breadth_first import bfs
from graph_search.depth_first import dfs
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Maze Size Selector")
    parser.add_argument("--size", type=str, choices=['small', 'medium', 'large'], help="Size of the maze: small, medium, or large")
    args = parser.parse_args()

    # Map the size choices to numerical sizes
    size_mapping = {
        'small': 8,  # Assuming a small maze is 10x10
        'medium': 16,  # Assuming a medium maze is 15x15
        'large': 32   # Assuming a large maze is 20x20
    }
    
    # Get the numerical size from the user's input
    size = size_mapping.get(args.size, 10)  # Default to 'small' (10x10) if not specified

    #parser = argparse.ArgumentParser()
    #parser.add_argument("--tile_exits")
    #args = parser.parse_args()

    # draw_maze([["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"]])

    #size = 10  this was the old way os setting size before user choice to also med or large
    flattened_exits, graph = create_maze_graph(size)

    tile_exits, axs = draw_maze(flattened_exits, block=True)

    #entities = [[]]
    #for each in entities:
    #    print_image(name)

    
    
    bfs_path = bfs(graph, (size-1, 0), (0, size-1))

    for each in bfs_path:
        update_knight(tile_exits, each, axs, block=True)   

    if bfs_path:
        print(f"BFS shortest path from character to reward: {bfs_path}")
    else:
        print(f"No path found from character to reward with BFS.")

    dfs_path = dfs(graph, (size-1, 0), (0, size-1))

    for each in dfs_path:
        update_knight(tile_exits, each, axs, block=True)   

    if dfs_path:
        print(f"DFS first path from character to reward: {dfs_path}")
    else:
        print(f"No path found from character to reward with DFS.")
        
    