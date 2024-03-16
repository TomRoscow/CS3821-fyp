import unittest
import matplotlib.pyplot as plt
from matplotlib.testing.compare import compare_images
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from visualisation import draw_tile, draw_maze, print_image
import numpy as np

class TestMazeDrawing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fig, cls.ax = plt.subplots()

    def test_draw_tile_with_no_exits(self):
        """Test draw_tile with a tile having no exits."""
        draw_tile(self.ax, [])

    def test_draw_tile_with_all_exits(self):
        """Test draw_tile with a tile having exits in all directions."""
        draw_tile(self.ax, ['north', 'south', 'east', 'west'])
        
    def test_draw_maze_with_invalid_input(self):
        """Test draw_maze with an input that's not a perfect square."""
        with self.assertRaises(ValueError):
            draw_maze([['north'], ['south']])

    def test_draw_maze_with_valid_input(self):
        """Test draw_maze with a valid square input."""
        try:
            draw_maze([['north'], ['south'], ['east'], ['west']])
        except Exception as e:
            self.fail(f"draw_maze raised an exception with valid input: {e}")

    def test_print_image_with_nonexistent_file(self):
        """Test print_image with a file name that does not exist."""
        with self.assertRaises(FileNotFoundError):
            print_image("nonexistent_image.png", [['north']], 0, [self.ax])

    @classmethod
    def tearDownClass(cls):
        plt.close('all')

if __name__ == '__main__':
    unittest.main()
