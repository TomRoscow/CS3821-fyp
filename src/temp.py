import math
from visualisation import draw_maze, update_knight
from graph import create_maze_graph
from graph_search.breadth_first import bfs
from graph_search.depth_first import dfs
from graph_search.uniform_cost import uniform_cost_search
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
    size = size_mapping.get(args.size, 10)  # Default to 'small' (10x10) if not specified

    #parser = argparse.ArgumentParser()
    #parser.add_argument("--tile_exits")
    #args = parser.parse_args()

    # draw_maze([["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"]])

    #size = 10  <-this was the old way of setting size before user choice to also med or large
    flattened_exits, graph = create_maze_graph(size)

    tile_exits, axs = draw_maze(flattened_exits, block=True)

    # My attempt to create a list of entities instead of handling drawing the crown and knight separately repeatedly
    #entities = [[]]
    #for each in entities:
    #    print_image(name)

    
    bfs_path = bfs(graph, (size-1, 0), (0, size-1))
    if bfs_path:
        for each in bfs_path:
            update_knight(tile_exits, each, axs, block=True)   

        print(f"BFS shortest path from character to reward: {bfs_path}")
    else:
        print(f"No path found from character to reward with BFS.")


    dfs_path = dfs(graph, (size-1, 0), (0, size-1))
    if dfs_path:
        for each in dfs_path:
            update_knight(tile_exits, each, axs, block=True)   

        print(f"DFS first path from character to reward: {dfs_path}")
    else:
        print(f"No path found from character to reward with DFS.")
        
    ucs_path, cost = uniform_cost_search(graph, (size-1, 0), (0, size-1))
    if ucs_path:
        print(f"UCS least costly path from character to reward: {ucs_path}, Cost: {cost}")
    else:
        print(f"No path found from character to reward with UCS.")