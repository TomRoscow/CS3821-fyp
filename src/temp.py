from visualisation import draw_maze
from graph import create_maze_graph
import argparse

if __name__ == "__main__":
    #parser = argparse.ArgumentParser()
    #parser.add_argument("--tile_exits")
    #args = parser.parse_args()

    # draw_maze([["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"], ["north"]])

    flattened_exits, graph = create_maze_graph(5)

    draw_maze(flattened_exits, block=True)
