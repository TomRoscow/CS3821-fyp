# Find root directory
from pathlib import Path

source_path = Path(__file__).resolve()
root_dir = source_path.parent.parent

import time
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import math
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import os
from typing import List, Tuple
plt.ion()  # Turn on interactive mode

def draw_tile(ax: plt.Axes, exits: List[str]):
    """
    Draws a single tile of the maze on the provided matplotlib Axes object based on the specified exits.

    This function visualizes a single tile (cell) of a maze by shading areas that do not lead to exits. It marks exits by
    leaving the corresponding edges of the tile unshaded. The tile is divided into a 4x4 grid, with the central area always
    unshaded to indicate it is traversable. Exits on the tile edges (north, south, east, west) are indicated by unshaded
    paths leading out of the central area.

    Parameters:
    - ax (plt.Axes): The matplotlib Axes object on which the tile will be drawn.
    - exits (List[str]): A list containing strings that indicate the exits from the tile. Valid strings are 'north', 
      'south', 'east', and 'west'. The presence of an exit string means that side of the tile will not be fully shaded,
      indicating a pathway.

    Notes:
    - The function defines a helper function `should_shade` to determine if a specific segment of the tile should be 
      shaded based on the tile's exits.
    - The visualization uses a pale grey color for non-exit areas and leaves exit paths unshaded.
    - This function is intended to be used as part of a larger maze drawing routine, where it would be called 
      for each tile in the maze grid.

    Requires:
    - matplotlib's pyplot as plt for the Axes object.
    - matplotlib.patches for drawing the rectangular segments of each tile.
    """

    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.axis('off')
    ax.set_aspect('equal', adjustable='box')

    # Define pale grey color
    pale_grey = '#f9f9f9'

    # Function to determine if a side should be shaded
    def should_shade(x, y):
        if 1 <= x <= 2 and 1 <= y <= 2:
            return False
        if (x in [1, 2] and y == 0 and 'south' in exits) or (x in [1, 2] and y == 3 and 'north' in exits):
            return False
        if (y in [1, 2] and x == 0 and 'west' in exits) or (y in [1, 2] and x == 3 and 'east' in exits):
            return False
        return True

    # Draw the tiles using a nested loop
    for x in range(4):
        for y in range(4):
            color = 'black' if should_shade(x, y) else pale_grey
            tile = patches.Rectangle((x, y), 1, 1, edgecolor=color, facecolor=color)  # Edges same as face colour
            ax.add_patch(tile)


def draw_maze(tile_exits: List[dict[str]], monster_locations: List[Tuple[int, int]], items_locations: List[Tuple[int, int]], block: bool =False):
    """
    Draws a maze based on the specified exits for each tile.

    The function creates a square grid visualisation of a maze where each cell (tile) 
    has specified exits. It checks if the number of tiles forms a perfect square 
    and raises a ValueError if not. It then visualises the maze with matplotlib, 
    marking the entrance and placing images on specified tiles.

    Parameters:
    - tile_exits (List[List[str]]): A list of lists, where each inner list contains 
      strings indicating the exits from that tile (e.g., "north", "south", etc.).
    - block: bool =False: A Boolean value to block further running of code when maze
      is plotted.

    Raises:
    - ValueError: If the length of `tile_exits` does not form a perfect square, 
      indicating that the maze cannot be laid out in a square grid.

    Notes:
    - The function modifies the exits of the bottom left tile to visualize the 
      maze entrance even if it's not traversable.
    - It also places specific images on the last tile of the first row and the 
      first tile of the last row for visual enhancement.

    Requires:
    - matplotlib for plotting the maze layout.
    - custom functions `draw_tile` and `print_image` for drawing each tile and 
      printing images on specified tiles, respectively.
    """

    # Check if the length of tile_exits is a perfect square
    num_tiles = len(tile_exits)
    side_length = int(math.sqrt(num_tiles))
    if side_length ** 2 != num_tiles:
        raise ValueError("Length of tile_exits must be a perfect square.")

    fig, axs = plt.subplots(side_length, side_length, figsize=(6, 6), gridspec_kw={'wspace':0.1, 'hspace':0.1})
    axs = axs.flatten() if num_tiles > 1 else [axs]  # Ensure axs is always a list

    for i, exits in enumerate(tile_exits):
    # For 0, first list of dictionary element in the list of list of dictionaries that is tile_exits. This hasn't changed from when it was a list of exits instead of a list of dictionaries of exits and their cost
        draw_tile(axs[i], list(exits.keys()))
        # Draw at 0, with what is made a list type from the 'list' of dictionary names for the tile. E.g. listifies 'north' and 'west' if the first tile's dictionary is {'north': 3, 'west': 5}
        # Because previously it took exits which was the first element in a list (the tile's exit directions) of lists (all tiles). Now it takes the list version of the first element's (tile) dictionary (exit) keys (direction)

    # Visualise maze entrance (even if not traversable)
    bottom_left_exits = tile_exits[num_tiles - side_length]
    bottom_left_exits['south'] = 0
    draw_tile(axs[num_tiles - side_length], bottom_left_exits)

    print_image("crown.png", tile_exits, int(math.sqrt(len(tile_exits)))-1, axs)
    print_image("knight.png", tile_exits, num_tiles - side_length, axs)
    for location in monster_locations:
        row, col = location
        flat_location = row * side_length + col
        print_image("goblin.png", tile_exits, flat_location, axs)

    for location in items_locations:
        row, col = location
        flat_location = row * side_length + col
        print_image("key.png", tile_exits, flat_location, axs)

    plt.pause(0.1)
    #block tells it to open the window but continue running the script
    #time.sleep(1)


    return tile_exits, axs # Does this so temp.py has axs for when it calls update_knight(). Remember to change tile_exits to size when print_image can be resolved for needing tile_exits instead of just the size

# The plan for this function is to be called for each coordinate in the BFS shortest path list, so you have a trail of knights, to prove how to reprint the knight image after the initialisation.
# Then you can move on to removing the previous image print [from the tile it's leaving]. And then you can move on to stuff like doing that whenever any entity's coordinates change, and having a list of entities with their image filename and coordinate.
def update_character(size, position, axs, filename, current_position):
    
    # My trouble here is temp.py is going to be calling this method because it has bfs_path from breadth_first.py and it commands the drawing (ie calls draw_maze), but print_image() here requires arguments from other functions here in visualisation.py
    # The error coming here is that print_image() takes an int for the position like 91 for bottom right but temp.py is giving an array like (9,0) for bottom right. Don't know how to resolve simply.
    row, col = position
    num_columns = int(math.sqrt(len(size)))
    flat_position = row * num_columns + col
    print_image(filename, size, flat_position, axs)

    # Clear previous position
    row, col = current_position
    flat_position = row * num_columns + col
    ax = axs[flat_position]

    # Clear the Axes corresponding to this position
    ax.clear()

    # Redraw the tile at this position without the character's image
    draw_tile(ax, list(size[flat_position].keys()))

    plt.pause(0.1)
    #time.sleep(1)


def print_image(image_name: str, tile_exits: List[dict[str]], position: int, axs: List[plt.Axes]):
    """
    Places an image on a specified position within a maze visualization.

    This function loads an image by name from a directory one level up in the folder hierarchy and under 'images',
    then converts it to an RGBA image (if not already in that format). It calculates the size of the maze grid based on the 
    length of `tile_exits` and places the image onto the specified position within the maze grid plotted on matplotlib Axes.

    Parameters:
    - image_name (str): The name of the image file (including its extension) to be placed on the maze. The image is expected 
      to be located in a folder named 'images' one level up from the current working directory.
    - tile_exits (List[List[str]]): A list of lists, where each inner list contains strings indicating the exits from that 
      tile. It's used to calculate the size of the maze grid.
    - position (int): The index position within the grid (following row-major order) where the image should be placed. 
      It is zero-based, so position 0 refers to the top-left tile of the maze.
    - axs (List[plt.Axes]): A list of matplotlib Axes objects corresponding to each tile of the maze. The image will be 
      placed on the Axes object at the index specified by `position`.

    Raises:
    - FileNotFoundError: If the image file specified by `image_name` does not exist at the expected location.

    Notes:
    - The function assumes that the maze grid is square, and the length of `tile_exits` must be a perfect square.
    - It also assumes the matplotlib figure and Axes objects have already been initialized outside this function, and 
      `axs` is a flat list of Axes, even for a 1x1 maze.
    - This function does not display the image or save the figure; it merely adds the image to the specified position 
      for later display or saving.

    Requires:
    - os for fetching the current working directory.
    - PIL's Image for opening and converting the image file.
    - numpy for handling image data.
    - matplotlib for plotting.
    """

    current_path = os.getcwd()

    image_location = os.path.join(root_dir, "images", image_name)
    image = Image.open(image_location)
    image = image.convert("RGBA")
    image_data = np.array(image)
    N = int(math.sqrt(len(tile_exits)))
    axs[position].imshow(image_data, aspect="auto", extent=(0, 4, 0, 4), zorder=2)
    
def erase_path(size: List[dict[str]], path: List[Tuple[int, int]], axs: List[plt.Axes], monster_locations: List[Tuple[int, int]], items_locations: List[Tuple[int, int]]):
    """
    Removes the knight's images along a given path in the maze.

    This function clears the tiles that the knight has visited and redraws them without the knight's image,
    effectively "erasing" the path taken by the knight. It assumes that the maze itself does not change
    and only the knight's image needs to be removed.

    Parameters:
    - size (List[dict[str]]): The list of dictionaries representing the exits for each tile in the maze.
    - path (List[Tuple[int, int]]): The list of positions (as row, col tuples) representing the knight's path.
    - axs (List[plt.Axes]): A list of matplotlib Axes objects corresponding to each tile of the maze.
    - block (bool): If True, pause the execution to allow the updated plot to be displayed.
    """

    num_columns = int(math.sqrt(len(size)))
    if path:
      for position in path:
          row, col = position
          flat_position = row * num_columns + col
          ax = axs[flat_position]

          # Clear the Axes corresponding to this position
          ax.clear()

          # Redraw the tile at this position without the knight's image
          draw_tile(ax, list(size[flat_position].keys()))

    print_image("crown.png", size, int(math.sqrt(len(size)))-1, axs)
    for location in monster_locations:
        row, col = location
        flat_location = row * num_columns + col
        print_image("goblin.png", size, flat_location, axs)
    for location in items_locations:
        row, col = location
        flat_location = row * num_columns + col
        print_image("key.png", size, flat_location, axs)