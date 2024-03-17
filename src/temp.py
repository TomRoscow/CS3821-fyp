import math
from visualisation import draw_maze
from graph import create_maze_graph
from graph_search.breadth_first import bfs
import argparse

if __name__ == "__main__":
    #parser = argparse.ArgumentParser()
    #parser.add_argument("--tile_exits")
    #args = parser.parse_args()

    # draw_maze([["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"]])

    size = 10
    flattened_exits, graph = create_maze_graph(size)

    draw_maze(flattened_exits, block=True)

    
    path = bfs(graph, (size-1, 0), (0, size-1))
    if path:
        print(f"Shortest path from character to reward: {path}")
    else:
        print(f"No path found from character to reward.")


