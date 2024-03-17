import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from graph import add_exits, determine_potential_exits, dead_end_handling, update_neighbouring_tiles, add_edge, create_maze_graph

class TestMazeGeneration(unittest.TestCase):
    def test_determine_potential_exits(self):
        N = 4
        # Test corners
        self.assertEqual(determine_potential_exits(0, 0, N), {'east', 'south'})
        self.assertEqual(determine_potential_exits(N-1, N-1, N), {'west', 'north'})
        # Test edge
        self.assertEqual(determine_potential_exits(0, 1, N), {'east', 'south', 'west'})
        # Test center
        self.assertEqual(determine_potential_exits(1, 1, N), {'east', 'south', 'west', 'north'})

    def test_add_edge(self):
        graph = {}
        node1 = (0, 0)
        node2 = (0, 1)
        expected_graph = {(0, 0): {(0, 1)}, (0, 1): {(0, 0)}}
        self.assertEqual(add_edge(graph, node1, node2), expected_graph)

    def test_add_exits(self):
        potential_exits = ["north", "south", "east", "west"]
        self.assertEqual(add_exits([[[]]], 0, 0, potential_exits, 1, 1), [])
        #Test that a 1x1 should have no exits by making exit_probability 1 so that it must be inclined to have all four exits if it was allowed to by size.
            
    


    #Test that it's not possible to have a deadend by making sure more than one exit in the list (tile_exit)
if __name__ == '__main__':
    unittest.main()
